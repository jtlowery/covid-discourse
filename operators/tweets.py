import pyspark
from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    udf,
    date_format,
    to_date
)
from pyspark.sql.types import (
    StringType,
    ArrayType,
)

from geo_vars import (
    countries, abbrvs_or_misspelling, state_province_to_country
)
from schemas import tweet_output_schema, tweet_schema


def create_spark_context(aws_conn_id):
    """creates the spark session"""
    spark = (
        SparkSession
        .builder
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("INFO")

    sc = spark.sparkContext
    sc = pyspark.SQLContext(sc)

    aws_hook = AwsHook(aws_conn_id)
    credentials = aws_hook.get_credentials()
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.access.key", credentials.access_key)
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.secret.key", credentials.secret_key)

    return sc


@udf(ArrayType(StringType()))
def clean_place(location_str):
    """Spark SQL udf for finding a province/state and country from location str"""
    country, province = None, None
    if location_str is None:
        return country, province
    result = abbrvs_or_misspelling.get(location_str)
    if result is None:
        if "," in location_str:
            splits = location_str.split(",")
            if splits[-1] in countries:
                country = splits[-1]
            if splits[0] in state_province_to_country:
                province = splits[0]
                country = state_province_to_country[province]
        return country, province
    else:
        return result[0], result[1]


class LoadTweetsToS3Operator(BaseOperator):
    ui_color = '#32701e'
    template_fields = ('tweets_day_glob',)

    @apply_defaults
    def __init__(
            self,
            tweets_day_glob,
            tweets_s3_location,
            aws_conn_id,
            *args,
            **kwargs
    ):
        """
        Operator to perform ETL on the daily set of tweets and save them to S3

        :param tweets_day_glob: a string glob that identifies the set of .jsonl.gz files that contain the day's tweets
        :param tweets_s3_location: s3 location to save the processed tweets to
        :param aws_conn_id: aws connection id for saving to s3
        """
        super(LoadTweetsToS3Operator, self).__init__(*args, **kwargs)
        self.tweets_day_glob = tweets_day_glob
        self.tweets_s3_location = tweets_s3_location
        self.aws_conn_id = aws_conn_id

    def execute(self, context):
        """ETL process to transform tweet data and save to s3"""

        self.log.info("creating spark session")
        sc = create_spark_context(self.aws_conn_id)

        # read jsonl files
        self.log.info("reading jsonl files from %s...", self.tweets_day_glob)
        df = sc.read.json(self.tweets_day_glob, schema=tweet_schema)

        # dropping unneeded cols, transforming date and location
        self.log.info("transforming...")
        df = (
            df
            .filter("lang == 'en'")
            .select(
                "id",
                "created_at",
                date_format(to_date(df.created_at, format="EEE MMM d H:mm:ss z yyyy"), "yyyy-MM-dd").alias("create_date"),
                col("place.full_name").alias("place_location"),
                clean_place("place.full_name").alias("place_province_country"),
                clean_place("user.location").alias("user_province_country"),
                col("user.location").alias("user_location"),
                col("full_text")
            )
            .select(
                "id",
                "created_at",
                "create_date",
                "place_location",
                col("place_province_country")[0].alias("place_province"),
                col("place_province_country")[1].alias("place_country"),
                "user_location",
                col("user_province_country")[0].alias("user_province"),
                col("user_province_country")[1].alias("user_country"),
                col("full_text")
            )
        )

        # checking the types are as we expect by comparing df schema to the expected schema
        assert df.schema == tweet_output_schema, f'df.schema not equal to the expected schema! \n{df.printSchema()}'

        self.log.info("saving to s3 at %s...", self.tweets_s3_location)
        (
            df
            .write
            .partitionBy("create_date")
            .parquet(self.tweets_s3_location, mode="append")
        )

        self.log.info("task successful!")


class CheckTweetsCount(BaseOperator):
    ui_color = '#12702e'
    template_fields = ('daily_tweets_s3_location',)

    @apply_defaults
    def __init__(
            self,
            daily_tweets_s3_location,
            aws_conn_id,
            *args,
            **kwargs
    ):
        """
        Operator to do a data quality (count) check on the daily tweet output from LoadTweetsToS3Operator

        :param daily_tweets_s3_location: s3 partition containing the day's tweets
        :param aws_conn_id: aws connection id for saving to s3
        """
        super(CheckTweetsCount, self).__init__(*args, **kwargs)
        self.daily_tweets_s3_location = daily_tweets_s3_location
        self.aws_conn_id = aws_conn_id

    def execute(self, context):
        """downloads and checks ETL'd tweet data from s3"""

        self.log.info("creating spark session")
        sc = create_spark_context(self.aws_conn_id)

        # read jsonl files
        self.log.info("reading parquet file from %s...", self.daily_tweets_s3_location)
        df = sc.read.parquet(self.daily_tweets_s3_location)

        # check count is reasonably high
        n_tweet_records = df.count()
        # the first day in the dataset only has 189
        assert df.count() > 188, f"number of records in tweet data for this day is low at only {n_tweet_records}"

        self.log.info("data quality checks passed!")


class CheckTweetsUniqueness(BaseOperator):
    ui_color = '#48502e'
    template_fields = ('tweets_s3_location',)

    @apply_defaults
    def __init__(
            self,
            tweets_s3_location,
            aws_conn_id,
            *args,
            **kwargs
    ):
        """
        Operator to do a data quality (primary key uniqueness) check on tweet output from LoadTweetsToS3Operator

        :param daily_tweets_s3_location: s3 partition containing the day's tweets
        :param aws_conn_id: aws connection id for saving to s3
        """
        super(CheckTweetsUniqueness, self).__init__(*args, **kwargs)
        self.tweets_s3_location = tweets_s3_location
        self.aws_conn_id = aws_conn_id

    def execute(self, context):
        """checks uniqueness of all tweets from s3 (i.e. primary key integrity)"""

        self.log.info("creating spark session")
        sc = create_spark_context(self.aws_conn_id)

        # read jsonl files
        self.log.info("reading parquet file from %s...", self.tweets_s3_location)
        df = sc.read.parquet(self.tweets_s3_location)

        n_tweet_records = df.count()
        n_distinct_tweets = df.select("id").distinct().count()
        # check the number of tweets and distinct ids are the same (i.e. primary key integrity)
        assert_msg = f"{n_tweet_records} tweet records does not match the {n_distinct_tweets} distinct tweet ids"
        assert n_tweet_records == n_distinct_tweets, assert_msg

        self.log.info("data quality checks passed!")
