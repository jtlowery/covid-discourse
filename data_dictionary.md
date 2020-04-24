# Data Dictionary

## province_country_covid_numbers

| Field      	| Data Type              	| (Acting as) Key 	| Description                                                        	|
|------------	|------------------------	|-----------------	|--------------------------------------------------------------------	|
| province   	| string                 	| PK              	| Name of the province or state that is a subdivision of the country 	|
| country    	| string                 	| PK              	| Name of the country                                                	|
| date       	| date (saved as string) 	| PK              	| Date of recorded numbers                                           	|
| cases      	| int                    	|                 	| Confirmed cases as of the date in this province, country           	|
| deaths     	| int                    	|                 	| Number of deaths as of the date in this province, country          	|
| recoveries 	| int                    	|                 	| Number of recoveries as of the date in this province, country      	|

## country_covid_numbers

| Field      	| Data Type 	| Key 	| Description                                                   	|
|------------	|-----------	|-----	|---------------------------------------------------------------	|
| country    	| string    	| PK  	| Name of the country                                           	|
| date       	| date      	| PK  	| Date of recorded numbers                                      	|
| cases      	| int       	|     	| Confirmed cases as of the date in this province, country      	|
| deaths     	| int       	|     	| Number of deaths as of the date in this province, country     	|
| recoveries 	| int       	|     	| Number of recoveries as of the date in this province, country 	|

## tweets

| Field                  	| Data Type              	| Key 	| Description                                                                                                 	|
|------------------------	|------------------------	|-----	|-------------------------------------------------------------------------------------------------------------	|
| id                     	| bigint                 	| PK  	| tweet id                                                                                                    	|
| created_at             	| string                 	|     	| unprocessed `created_at` field from tweet object                                                              	|
| created_date           	| date (saved as string) 	|     	| date extracted from `created_at` in YYYY-MM-DD form                                                   	|
| place_country          	| string                 	| FK  	| country the tweet is associated with as best could be found from place attribute in tweet object                	|
| place_province         	| string                 	| FK  	| province/state the tweet is associated with as best could be found from place attribute in tweet object         	|
| user_location_country  	| string                 	| FK  	| country the tweet is associated with as best could be found from user.location attribute in tweet object        	|
| user_location_province 	| string                 	| FK  	| province/state the tweet is associated with as best could be found from user.location attribute in tweet object 	|
| full_text              	| string                 	|     	| the full text of the tweet                                                                           	|
