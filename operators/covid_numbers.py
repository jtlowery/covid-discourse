from datetime import datetime

import pandas as pd
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from pandas.api.types import is_string_dtype, is_numeric_dtype

from geo_vars import countries, state_provinces, us_state_provinces


def initial_clean(df):
    """
    standardize column names and drop unused columns

    :param df: dataframe to perform renames and column drops on
    :return: cleaned dataframe
    """
    df = df.rename(columns={
        'Province/State': 'province',
        'Province_State': 'province',
        'Country/Region': 'country',
        'Country_Region': 'country',
    })

    possible_drop_cols = [
        "UID",
        "iso2",
        "iso3",
        "code3",
        "FIPS",
        "Admin2",
        "Lat",
        "Long",
        "Long_",
        "Combined_Key",
        "Population",
    ]
    drop_cols = [col for col in possible_drop_cols if col in df.columns]

    df = df.drop(drop_cols, axis='columns')
    return df


def convert_wide_to_tidy(df, var_name, value_name):
    """
    standardize country names and convert wide df to long/tidy

    :param df: dataframe in wide format
    :param var_name: name to use for variable column (the column that will contain the dates)
    :param value_name: name to use for the value column (column which contains case number observations)
    :return: dataframe in tidy format
    """
    date_cols = [col for col in df.columns.tolist() if '/' in col]
    tidy = pd.melt(
        df,
        id_vars=['province', 'country'],
        value_vars=date_cols,
        var_name=var_name,
        value_name=value_name,
    )
    tidy['country'] = tidy['country'].str.replace('Taiwan\*', 'Taiwan')
    tidy['country'] = tidy['country'].str.replace('US', 'United States')
    tidy['date'] = tidy['date'].apply(lambda x: datetime.strptime(x, '%m/%d/%y').strftime('%Y-%m-%d'))
    return tidy


def assert_primary_key_is_unique(df, primary_key_cols):
    """
    check that the column(s) that make up primary key are truly unique in dataframe

    :param df: dataframe to check primary key uniqueness
    :param primary_key_cols: columns of dataframe that make up primary key
    :raises: AssertionError
    :return: None
    """
    n_rows = len(df[primary_key_cols])
    n_unique_rows = len(df[primary_key_cols].drop_duplicates())
    assert n_rows == n_unique_rows, 'primary keys are not unique!'


def assert_dtypes_as_expected(df):
    """
    checks that the dataframe has the expected dtypes

    :param df: dataframe, final outputs from LoadCovidNumbersToS3Operator
    :raises: AssertionError
    :return: None
    """
    cols_to_dtype_func = {
        "country": is_string_dtype,
        "province": is_string_dtype,
        "date": is_string_dtype,
        "deaths": is_numeric_dtype,
        "confirmed": is_numeric_dtype,
        "recovered": is_numeric_dtype,
    }
    for col, is_dtype_func in cols_to_dtype_func.items():
        if col in df.columns:
            assert is_dtype_func(df[col]), f'col {col} failed dtype check of {is_dtype_func}'


class LoadCovidNumbersToS3Operator(BaseOperator):
    ui_color = '#936581'

    @apply_defaults
    def __init__(
            self,
            covid_numbers_local_dir,
            covid_numbers_s3_location,
            *args,
            **kwargs
    ):
        """
        Operator to perform ETL on covid numbers and save cleaned numbers at
        country and (province/state, country) aggregation levels to S3. Please note
        this save requires the AWS credentials to be set up on the system.

        :param covid_numbers_local_dir: local path to covid_numbers directory
        :param covid_numbers_s3_location: s3 location to save output country and
               country, province level numbers to
        """
        super(LoadCovidNumbersToS3Operator, self).__init__(*args, **kwargs)
        self.covid_numbers_local_dir = covid_numbers_local_dir
        self.covid_numbers_s3_location = covid_numbers_s3_location

    def execute(self, context):
        """loads csv data from local dir, transforms and saves to s3"""

        # read csv files
        self.log.info('reading csv files...')
        data_dir = self.covid_numbers_local_dir
        global_confirmed = pd.read_csv(f'{data_dir}/time_series_covid19_confirmed_global.csv')
        us_confirmed = pd.read_csv(f'{data_dir}/time_series_covid19_confirmed_US.csv', dtype={'date': str})
        global_deaths = pd.read_csv(f'{data_dir}/time_series_covid19_deaths_global.csv')
        us_deaths = pd.read_csv(f'{data_dir}/time_series_covid19_deaths_US.csv', dtype={'date': str})
        global_recovered = pd.read_csv(f'{data_dir}/time_series_covid19_recovered_global.csv')

        # drop unnecessary columns, standardize names
        self.log.info('cleaning csv files...')
        global_confirmed = initial_clean(global_confirmed)
        global_deaths = initial_clean(global_deaths)
        global_recovered = initial_clean(global_recovered)
        us_confirmed = initial_clean(us_confirmed)
        us_deaths = initial_clean(us_deaths)

        # convert from wide to tidy/long (instead of 1 column per date, 1 row per date)
        self.log.info('transforming csv files...')
        global_confirmed = convert_wide_to_tidy(global_confirmed, var_name='date', value_name='confirmed')
        global_deaths = convert_wide_to_tidy(global_deaths, var_name='date', value_name='deaths')
        global_recovered = convert_wide_to_tidy(global_recovered, var_name='date', value_name='recovered')
        us_confirmed = convert_wide_to_tidy(us_confirmed, var_name='date', value_name='confirmed')
        us_deaths = convert_wide_to_tidy(us_deaths, var_name='date', value_name='deaths')

        # combine the global numbers into one df
        global_df = pd.merge(
            global_confirmed,
            global_deaths,
            how='outer',
            on=['province', 'country', 'date'],
        )
        global_df2 = pd.merge(
            global_df,
            global_recovered,
            how='outer',
            on=['province', 'country', 'date'],
        )

        # combine the us numbers
        us_df = pd.merge(
            us_confirmed,
            us_deaths,
            how='outer',
            on=['province', 'country', 'date'],
        )
        us_df = (
            us_df
            .groupby(['province', 'country', 'date'], as_index=False)
            .agg({'deaths': 'sum', 'confirmed': 'sum'})
        )

        # combine global and us rows
        final_df = pd.concat([us_df, global_df2], sort=False, ignore_index=True)

        # country level aggregation
        final_df_country = final_df.groupby(['country', 'date'], as_index=False).agg({
            'deaths': 'sum',
            'confirmed': 'sum',
            'recovered': 'sum',
        })

        # province, country level aggregation
        final_df = final_df[final_df['province'].notnull()].reset_index(drop=True)

        # check primary keys are truly unique
        self.log.info('checking primary keys uniqueness...')
        assert_primary_key_is_unique(final_df, primary_key_cols=["province", "country", "date"])
        assert_primary_key_is_unique(final_df_country, primary_key_cols=["country", "date"])

        # check dtypes are as expected
        assert_dtypes_as_expected(final_df)
        assert_dtypes_as_expected(final_df_country)

        # save to s3
        self.log.info('saving to output to s3...')
        final_df.to_csv(f'{self.covid_numbers_s3_location}/province_country_covid_numbers.csv', index=False)
        final_df_country.to_csv(f'{self.covid_numbers_s3_location}/country_covid_numbers.csv', index=False)

        self.log.info('task successful!')


class CheckCovidNumbersETL(BaseOperator):
    ui_color = '#430581'

    @apply_defaults
    def __init__(
            self,
            covid_numbers_s3_location,
            *args,
            **kwargs
    ):
        """
        Operator to do a data quality check on covid number output from LoadCovidNumbersToS3Operator

        :param covid_numbers_local_dir: local path to covid_numbers directory
        :param covid_numbers_s3_location: s3 location to save output country and
               country, province level numbers to
        """
        super(CheckCovidNumbersETL, self).__init__(*args, **kwargs)
        self.covid_numbers_s3_location = covid_numbers_s3_location

    def execute(self, context):
        """downloads and checks ETL'd covid numbers data from s3"""

        # read csv files
        self.log.info('downloading csv files from %s...', self.covid_numbers_s3_location)
        country_df = pd.read_csv(f'{self.covid_numbers_s3_location}/country_covid_numbers.csv')
        province_df = pd.read_csv(f'{self.covid_numbers_s3_location}/province_country_covid_numbers.csv')

        # check primary keys are truly unique
        self.log.info('checking primary keys uniqueness...')
        assert_primary_key_is_unique(province_df, primary_key_cols=["province", "country", "date"])
        assert_primary_key_is_unique(country_df, primary_key_cols=["country", "date"])

        # check dtypes are as expected
        assert_dtypes_as_expected(province_df)
        assert_dtypes_as_expected(country_df)

        # check a reasonable amount of data is present for each cleaned dataset
        self.log.info('checking reasonable number of rows in datasets...')
        assert 10_000 < len(country_df) < 500_000, 'abnormal number of rows in country-level dataset'
        assert 10_000 < len(province_df) < 500_000, 'abnormal number of rows in (province, country-level) dataset'

        # check expected number of columns in each
        self.log.info("checking expected number of columns...")
        assert country_df.shape[1] == 5, f'country dataset had {country_df.shape[1]} rows not 5'
        assert province_df.shape[1] == 6, f'country dataset had {province_df.shape[1]} rows not 6'

        # check countries and provinces are the expected ones
        self.log.info('checking countries and provinces are the expected ones...')
        unexpected_countries = set(country_df.country) - set(countries)
        assert len(unexpected_countries) == 0, f'found unexpected countries: {unexpected_countries}'
        unexpected_provinces = set(province_df.province) - set(state_provinces) - set(us_state_provinces)
        assert len(unexpected_countries) == 0, f'found unexpected provinces: {unexpected_provinces}'

        self.log.info('data quality checks passed!')
