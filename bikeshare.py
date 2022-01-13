## This Project was created by Olga Cebrian on January 12th 2022 as part of the Programming for Data Science with Python

import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_DATA = ['all','january', 'february', 'march', 'april', 'may', 'june']

DAY_DATA = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_input = ''
    while city_input.lower() not in CITY_DATA:
        city_input = input('What city do you want to see data for? i.e Chicago, New York City, Washington): ')
        if city_input.lower() in CITY_DATA:
            city = CITY_DATA[city_input.lower()]
        else:
            print('Sorry, I didn\'t understand that.')

    # get user input for month (all, january, february, ... , june)
    month_input = ''
    while month_input.lower() not in MONTH_DATA:
        month_input = input('What month do you want to see data for? i.e All, January, February...: ')
        if month_input.lower() in MONTH_DATA:
            month = month_input.lower()
        else:
            print('Sorry, that is not a valid month. Please choose again.')


    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_input = ''
    while day_input.lower() not in DAY_DATA:
        day_input = input('What day do you want to see data for? i.e All, Monday, Tuesday...: ')
        if day_input.lower() in DAY_DATA:
            day = day_input.lower()
        else:
            print('Sorry, that is not a valid day. Please choose again.')


    print('-'*50)
    print('-'*50)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(city)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTH_DATA.index(month)

        # filter by month to create the new dataframe
        df = df.loc[df['month']== month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week']== day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('\nThe Most Common Month is:\n',popular_month)

    # display the most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]
    print('\n The Most Common Day of Week is:\n',popular_day_of_week)

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('\nThe Most Common Hour of the Day is:\n',popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)
    print('-'*50)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_stat = df['Start Station'].mode()[0]
    print('\nThe Most Common Start Station is:\n',common_start_stat)

    # display most commonly used end station
    common_end_stat = df['End Station'].mode()[0]
    print('\nThe Most Common End Station is:\n',common_end_stat)

    # display most frequent combination of start station and end station trip
    df['Start to End Stations'] = df['Start Station'] + df['End Station']
    start_end_stations = df['Start to End Stations'].mode()[0]
    print('\nThe Most Frequent Combination Start to End Station are:\n',start_end_stations)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)
    print('-'*50)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    m,s = divmod(total_travel_time,60)
    h,m = divmod(m,60)
    print('\nThe total Travel Time is:\n {} hour(s) {} minute(s) and {} second(s)\n'.format(h,m,s))

    # display mean travel time
    mean_travel_time = round(df['Trip Duration'].mean())
    m,s = divmod(mean_travel_time,60)

    if m > 60:
        h,m = divmod(m,60)
        print('\nThe total Travel Time is:\n {} hour(s) {} minute(s) and {} second(s)'.format(h,m,s))
    else:
        print('\nThe total Travel Time is:\n {} minute(s) and {} second(s)'.format(m,s))

    print("\nThis took %s seconds." % (time.time() - start_time))

    print('-'*50)
    print('-'*50)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_counts = df['User Type'].value_counts()
    print('\nUser Types are:\n',user_type_counts)

    # Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print('\nGender split is:\n',gender)
    except:
        print('\nNo gender split\n')

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_year_birth = int(df['Birth Year'].min())
        recent_year_birth = int(df['Birth Year'].max())
        common_year_birth = int(df['Birth Year'].mode()[0])
        print('\nThe earliest year of birth is:\n',earliest_year_birth)
        print('\nThe most recent year of birth is:\n',recent_year_birth)
        print('\nThe most common year of birth is:\n',common_year_birth)
    except:
        print('\nSorry, there is no Birth Year column\n')

    print("\nThis took %s seconds." % (time.time() - start_time))

    print('-'*50)
    print('-'*50)


def display_raw_data(df):
    """ Ask user if they want to see raw data with the filters selected."""
    i = 0
    raw = input("n\Would you like to see raw data?. Answer yes or no.\n").lower() # TO DO: convert the user input to lower case using lower() function
    pd.set_option('display.max_columns',200)

    while True:
        if raw == 'no':
            break
        elif raw == 'yes':
            print(df[i:i + 5]) # TO DO: appropriately subset/slice your dataframe to display next five rows
            raw = input("\nWould you want to see 5 more rows? Please write yes or no.\n").lower() # TO DO: convert the user input to lower case using lower() function
            i += 5
        else:
            raw = input("\nYour input is invalid. Please enter only 'yes' or 'no'\n").lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
