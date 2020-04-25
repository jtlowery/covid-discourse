import configparser
import os
from datetime import datetime, timedelta

from airflow import DAG

from operators import (
    LoadTweetsToS3Operator,
    LoadCovidNumbersToS3Operator,
)
from operators.covid_numbers import CheckCovidNumbersETL
from operators.tweets import CheckTweetsCount, CheckTweetsUniqueness

config = configparser.ConfigParser()
config.read('etl.cfg')
os.environ['AWS_ACCESS_KEY_ID'] = config['AWS']['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY'] = config['AWS']['AWS_SECRET_ACCESS_KEY']


# defining the DAG for processing tweets
tweet_args = {
    'owner': 'Joel',
    'start_date': datetime(2020, 1, 21),
    'depends_on_past': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=15),
}
tweets_dag = DAG(
    'tweet_etl',
    default_args=tweet_args,
    description='ETL process to transform tweet data and save to s3',
    schedule_interval='@daily',
    max_active_runs=1,
    catchup=True,
)
tweets_s3_location = config['DATA']['TWEETS_S3_LOCATION']
tweets_local_dir = config['DATA']['TWEETS_LOCAL_ROOT_DIR']
tweets_fp = '{{ execution_date.year }}-{{ execution_date.strftime("%m") }}/coronavirus-tweet-id-{{ ds }}-*.jsonl.gz'
load_tweets = LoadTweetsToS3Operator(
    task_id='load_tweets',
    dag=tweets_dag,
    tweets_day_glob=f'{tweets_local_dir}/{tweets_fp}',
    tweets_s3_location=tweets_s3_location,
    aws_conn_id='aws_conn',
)
daily_tweets_s3_location = os.path.join(tweets_s3_location, 'create_date={{ ds }}/')
tweets_count_check = CheckTweetsCount(
    task_id='count_check_tweets',
    dag=tweets_dag,
    daily_tweets_s3_location=daily_tweets_s3_location,
    aws_conn_id='aws_conn',
)
tweets_uniqueness_check = CheckTweetsUniqueness(
    task_id='check_tweets_uniqueness',
    dag=tweets_dag,
    tweets_s3_location=tweets_s3_location,
    aws_conn_id='aws_conn',
)
load_tweets >> tweets_count_check
load_tweets >> tweets_uniqueness_check


# defining the DAG for processing the covid case numbers
covid_numbers_args = {
    'owner': 'Joel',
    'depends_on_past': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=15),
}
covid_numbers_dag = DAG(
    'covid_numbers',
    default_args=covid_numbers_args,
    description='ETL process to transform covid case numbers and save to s3',
    start_date=datetime(2020, 1, 21),
    schedule_interval='@daily',
    max_active_runs=1,
    catchup=False,
)

covid_numbers_s3_location = config['DATA']['COVID_NUMBERS_S3_LOCATION']
covid_numbers_local_dir = config['DATA']['COVID_NUMBERS_LOCAL_DIR']
load_covid_numbers = LoadCovidNumbersToS3Operator(
    task_id='load_covid_numbers',
    dag=covid_numbers_dag,
    covid_numbers_local_dir=covid_numbers_local_dir,
    covid_numbers_s3_location=covid_numbers_s3_location,
)
covid_numbers_quality_check = CheckCovidNumbersETL(
    task_id='check_covid_numbers',
    dag=covid_numbers_dag,
    covid_numbers_s3_location=covid_numbers_s3_location,
)
load_covid_numbers >> covid_numbers_quality_check
