# Covid Sentiment ETL

## 1 - Data Sources and Project Scope
### Data Sources
1. [COVID-19-TweetIDs](https://github.com/echen102/COVID-19-TweetIDs)
    - Description: This data source collects tweet ids of tweets concerning COVID-19 starting with 1/21/2020. Only the tweet ids are published in the .txt files to comply with Twitter's policies but they can be 'rehydrated' (enriched with full info) as described in the repository. The provided rehydrating script outputs a newline delimited json file (gzipped) for each file of tweet ids. Each line in this resulting file is a json for the [tweet object](https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object).  
    - Data size:  There were 94,671,486 tweet ids when I cloned the above repository on 04/17/2020. After rehydrating, the resulting newline delimited json files (gzipped) took about 61GB of space. 
    - Citation: Emily Chen, Kristina Lerman, and Emilio Ferrara. 2020. #COVID-19: The First Public Coronavirus Twitter Dataset. arXiv:cs.SI/2003.07372, 2020
    - License: [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)
2. [COVID-19](https://github.com/CSSEGISandData/COVID-19)
    - Description: This data source collects numbers of confirmed cases, numbers of deaths, and numbers of recovered patients over time (day by day) and over geography (by country/region, state/province, and county (county only for US)).
    - Data size: There are 5 csv files (in `COVID-19/csse_covid_19_data/csse_covid_19_time_series/`) that collect these values (confirmed, deaths, recovered). The files are separated by value collected and geography (US by county vs global by region and state). In the below files, each row represents a specific geography and most of the columns are devoted to dates for each day the measurement is taken/observed.
        1. time_series_covid19_confirmed_global.csv
            - 264 rows by 92 columns
        2. time_series_covid19_deaths_global.csv
            - 264 rows by 92 columns
        3. time_series_covid19_recovered_global.csv
            - 250 rows by 92 columns
        4. time_series_covid19_confirmed_US.csv
            - 3255 rows by 99 columns
        5. time_series_covid19_deaths_US.csv
            - 3255 rows by 100 columns
    - Citation: Dong, E., Du, H., & Gardner, L. (2020). An interactive web-based dashboard to track COVID-19 in real-time. The Lancet Infectious Diseases. [https://doi.org/10.1016/S1473-3099(20)30120-1](https://doi.org/10.1016/S1473-3099(20)30120-1)

### Project Scope
I was exploring datasets regarding COVID-19 when I encountered the twitter dataset. 
I thought the potential insights into how the pandemic is impacting the public at large and the change in public 
discourse over time made this dataset particularly interesting to work with to me. Combined with the time series data 
from the other dataset that measures the progression of the epidemic across different geographies, we should be able to 
look at tweets as the pandemic progressed across the world and in the particular country or region of a given tweet. 
I'd like to prepare the data so that it can be easily joined on time and geography (i.e. what tweets happened on a 
given day in the US and what were the numbers for cases/deaths/recoveries that day in the US or world). The main use 
case I'd like to support is fairly complex NLP analysis (e.g. change in public sentiment over the course of the 
pandemic). This would likely involve downloading the data and working with it in Python or similar language as the 
analysis would be complex and not well suited to SQL queries. I think cleaning the data to make it easy to pull and 
combine the data by time and geography is the bulk of the work needed to prepare it for this purpose. 


## 2 - Data Exploration and Assessment

1. COVID-19-TweetIDs
    - There are two elements that describe locations in tweet objects. The first is the user location which appears to 
    be a string the user sets as their location and has a lot of variation/inaccuracies (as you would expect for a user input 
    string). This is present (non-null, non-empty) in more than half of the tweets. The second location element appears 
    to be when the user allows twitter to access location data and adds this as a `place` object inside the tweet object 
    which contains a number of fields (`country`, `bounding_box`, `name`, `place_type`, etc.). This is probably a higher 
    fidelity field since it isn't a user input but, unfortunately, it is only available on a small portion of the 
    tweets (< 1%). I wanted to retain both fields since one is higher quantity and the other is higher quality. However, 
    steps needed to be taken to clean it up or extract country and province/region. I put together a dict 
    `abbrvs_or_misspelling` in `geo_vars.py` to help with this. It maps strings that represent likely or common 
    location/place strings to the correct (province/state, country) pairs. These output provinces and countries were 
    selected to match up with the ones used in the second dataset.
    - The date was extracted from the `created_at` field and converted to the simple and handy `YYYY-MM-DD` string format 
    (easy to sort or use for partitioning).
2. COVID-19
    - Needed to apply some standardization to country and province names
        - Converted `US` to `United States`
        - Converted `Taiwan*` to `Taiwan`
    - Standardized date to the `YYYY-MM-DD` string format
    - Converted the data from wide (each observation/day as a new column) to tidy/long 
      (each observation/day as a new row). This tidy format is much easier to join on, query, etc.
    - Combined the US and global datasets into one
    - Created one aggregation at the (province/state, country) level and one rolled up to country level

Please note all the above cleaning steps occur in the ETL code itself.

## 3 - Data Model
Given our above datasets and goal of using the output data to analysis into how public discourse or sentiment changed 
over the progression of the pandemic, we need to process the datasets into a clean data model that would allow for easy 
joins on geography and date. 


The COVID-19 dataset supplies info by day at the country level and some subdivisions of the 
countries as well (province/state) so it would make sense for us to process this into two datasets: one at the 
(day, country) level and a second at the (day, province, counry) level. The steps to process this data into this form 
are mentioned in #2 above.

Please note that these are saved to S3 and not placed into a database so there is not an actual key on these fields,
just that these fields could be keys if they were in a database and have been processed with this in mind.

#### province_country_covid_numbers

| Field      	| Data Type              	| (Acting as) Key 	|
|------------	|------------------------	|-----------------	|
| province   	| string                 	| PK              	|
| country    	| string                 	| PK              	|
| date       	| date (saved as string) 	| PK              	|
| cases      	| int                    	|                 	|
| deaths     	| int                    	|                 	|
| recoveries 	| int                    	|                 	|

#### country_covid_numbers

| Field      	| Data Type              	| (Acting as) Key 	|
|------------	|------------------------	|-----------------	|
| country    	| string                 	| PK              	|
| date       	| date (saved as string) 	| PK              	|
| cases      	| int                    	|                 	|
| deaths     	| int                    	|                 	|
| recoveries 	| int                    	|                 	|

The COVID-19-TweetIDs supplies tweet ids which after rehydrating are become very complex 
[tweet objects](https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object). 
Only a small portion of the fields in the object are of interest to us: the create date string (time), the id, 
place (geography), location (geography), and the text of the tweet. As mentioned above, we need to try to extract and 
clean the province and country names out of the `place` and `location` fields so the names are consistent with the 
province and country names in the other dataset. There is also a need to extract the date from the `created_at` field and 
format it in the same `YYYY-MM-DD` structure. Finally, the tweets can be filtered to only those with `lang='en'` as the 
majority of them are in English and doing an analysis across languages would be an additional, significant challenge 
(however, this filter could certainly be removed at a later time).

#### tweets

| Field                  	| Data Type              	| (Acting as) Key 	|
|------------------------	|------------------------	|-----------------	|
| id                     	| int64                 	| PK              	|
| created_at             	| string                 	|                 	|
| created_date           	| date (saved as string) 	| FK              	|
| place_country          	| string                 	| FK              	|
| place_province         	| string                 	| FK              	|
| user_location_country  	| string                 	| FK              	|
| user_location_province 	| string                 	| FK              	|
| full_text              	| string                 	|                 	|

 Please note that the fields marked with FK would not all be one foreign key (and aren't actually keys as mentioned 
 above). But a combination of 2 or 3 of them could be:
   - (created_date, place_country) -> (date, country) on `country_covid_numbers`
   - (created_date, place_country, place_province) -> (date, country, province) on `province_country_covid_numbers`
   - (created_date, location_country) -> (date, country) on `country_covid_numbers`
   - (created_date, location_country, location_province) -> (date, country, province) on `province_country_covid_numbers`

## 4 - ETL Process, Data Dictionary, and Data Quality Checks

Airflow is used to schedule and execute the pipelines. There are two DAGs - one for each dataset. 

1. The `tweet_etl` DAG processes one day's tweets and appends to the existing output so it needs to run every day and 
needs to backfill (airflow `catchup=True`) to load past days. The first task in the`tweet_etl` DAG processes the 
.jsonl.gz tweet files and loads the output on s3 in the parquet format. The second task, runs a task which performs a 
data quality check on the output by checking that the number of records is at least the size of the first day which 
has the least data.
2. The `covid_numbers` DAG processes all of the covid numbers data (historical and up-to-date - so backfill is not 
needed) into the two outputs at the country and (province, country) levels. Again, the first task processes and loads 
the data while the second performs data quality checks. The first task reads all 5 of the csv files mentioned above, 
cleans and processes them, then loads each of the two outputs as csv files to s3. The quality checking task reads the 
two outputs from the previous task and checks that there is a reasonable number of rows in each, the expected number of 
columns/fields is correct, and that the countries and provinces are the ones (and are formatted) as we expect. 

The output of the above ETL process resembles the traditional star schema - one fact table (tweets) which contains 
records of a specific event/tweet and two dimensions tables which each contain additional info (extra characteristics 
such as count of confirmed cases) about a specific dates and geographies. A main advantage of this schema is it's 
simplicity to work with and join the tables together -- which happens to be the main goal of this project -- making it 
easy to join these datasets by geography and time.  

Please see `data_dictionary.md` for descriptions of fields. 

Data quality checks are performed in the DAGs for each dataset. The below table summarizes each check and where it 
occurs.

| Data Check                                                        	| DAG Location  	| Task Location           	|
|-------------------------------------------------------------------	|---------------	|-------------------------	|
| Tweet output matches with expected data types (schema)            	| tweet_etl     	| load_tweets             	|
| Count of daily’s tweets output >= a minimum (the lowest day’s)    	| tweet_etl     	| count_check_tweets      	|
| Primary key integrity (all tweets have a unique id)               	| tweet_etl     	| check_tweets_uniqueness 	|
| Primary key integrity (PK is unique across rows) – before s3 load 	| covid_numbers 	| load_covid_numbers      	|
| Primary key integrity (PK is unique across rows) – after s3 load  	| covid_numbers 	| check_covid_numbers     	|
| Covid numbers output matches expected data types – before s3 load 	| covid_numbers 	| load_covid_numbers      	|
| Covid numbers output matches expected data types – after s3 load  	| covid_numbers 	| check_covid_numbers     	|
| Count of rows in Covid numbers output is reasonable               	| covid_numbers 	| check_covid_numbers     	|
| Count of columns in Covid numbers output is as expected           	| covid_numbers 	| check_covid_numbers     	|
| Only valid country and province values in Covid numbers output    	| covid_numbers 	| check_covid_numbers     	|


## 5 - Goals, Next Steps, and Other Considerations

The goal of this project was to build a pipeline to process COVID-19 related tweets and COVID-19 case numbers into a 
format that would be easy to work with and combine based on geography and time. The next steps are to actually start 
performing this analysis. One basic analysis would to bring in each tweet, get a sentiment score for the tweet, then 
aggregate these scores up to various geographies (global, country, province) and do multiple stacked plots that share 
the same x-axis (time or days) - one for sentiment score and one for each of the case numbers 
(confirmed/deaths/recoveries).

Airflow has already been incorporated into this project to keep it organized and minimize the need for human 
intervention. There are still a couple more steps that could potentially be automated (pulling the datasets from the sources 
and rehydrating the tweets). I believe both dataset sources are updating daily or close to it, so we could automate pulling 
the data to keep the output of this pipeline totally up-to-date. When doing the intended analysis it would be nice to 
have as much data as is available and Airflow and the design of the pipelines should make it easy to stay up-to-date. 

Spark is used by the Tweets tasks due to the data size already being pretty considerable (>60GB) and this will only 
increase over time. Right now I've only run it on my personal machine with 6 cores but this could certainly be altered 
to use AWS nodes to scale it up to even much larger numbers.

If data size increased by a factor of 10 or 100, this design should hold up reasonably well due to the use of Spark with 
the bigger dataset. As mentioned above, we could use Spark on AWS nodes to scale horizontally to handle a huge increase 
in the tweet data size. We could even convert the Covid numbers portion to use Spark if that dataset increased 
massively as well. In terms of scheduling, the DAGs are both set to run on a daily basis and we could set the time of 
day to be whatever we want (say 7am), or, if we knew what time the sources were updating we could automate that pull and set the 
run time to be shortly after that.

Since we want to bring this data back into Python to do the desired analysis, saving to s3 made a lot of sense (easy to 
access with Python, cheap, able to have heavily compressed data (e.g. parquet)). If we wanted this data to be more 
easily accessible to others that would frequently want to access it, it may make sense to put it in a database like 
Redshift which scales well with datasize and users (horizontal scaling). Another option would be to keep it in s3 and 
use AWS Athena or another database technology that can work on top of s3.

## 6 - Project Installation and Run Steps
- Download the data from source 1 and 2 above (need to rehydrate the tweets)
    - I've supplied the copies I pulled of the csv's from [COVID-19](https://github.com/CSSEGISandData/COVID-19) in 
      the `data/COVID-19/` directory in this project
    - I've also supplied a fake, test dataset that mimics the structure of the rehydrated tweets in 
      `data/fake-test-tweets/`. Please note that this data has an end date of 2020-04-09 so the DAGs will begin to fail
      once running out of the fake data.
- Install 
    - Install conda (https://docs.anaconda.com/anaconda/install/)
    - Run `conda env create -f covid-sentiment.yml` to create environment (can also manually install packages but I had 
        some issues or bugs with certain package versions)
    - Run `conda activate covid-sentiment` to activate conda environment
- Environment setup
    - Fill in the values in `etl.cfg` (AWS key/secret and path to datasets from the first step)
- Run airflow (see https://airflow.apache.org/docs/stable/start.html)
    - Add an AWS connection named 'aws_conn' using the Airflow webui
    - Set the `dags_folder` in the `airflow.cfg` to this project directory
    - Once the scheduler starts the DAGs will start
