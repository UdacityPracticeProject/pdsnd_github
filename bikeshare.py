import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_LIST = ['january', 'february', 'march', 'april', 'may', 'june']
DAY_LIST = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']

def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')

    while True:
        city = input("Would you like to see data for Chicago, New York, or Washington? ")
        city = city.lower()
        if city not in CITY_DATA:
            print("Invalid Input! (Please enter 'chicago', 'new york city' or 'washington')\n")
            continue
        else:
            break

    while True:
        month = input("Which month? January, February, March, April, May, or June? or not at all? Type 'all' for no month filter. ")
        month = month.lower()
        if month == 'all' or month in MONTH_LIST:
            break
        print("Invalid Input!\n")

    while True:
        day = input("Which day? Monday, Tuesday, ... Sunday? or not at all? Type 'all' for no day filter. ")
        day = day.lower()
        if day == 'all' or day in DAY_LIST:
            break
        print("Invalid Input!\n")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day_of_Week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        month = MONTH_LIST.index(month) + 1
        df = df[df['Month'] == month]

    if day != 'all':
        df = df[df['Day_of_Week'] == day.title()]

    return df

def time_stats(df):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    common_month = df['Month'].mode()[0]

    print("Most Common Month: ", MONTH_LIST[common_month-1].title())

    common_day = df['Day_of_Week'].mode()[0]

    print("Most Common Day of Week: ", common_day)

    df['Start Hour'] = df['Start Time'].dt.hour
    common_start_hour = df['Start Hour'].mode()[0]

    print("Most Common Start Hour: ", common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))

    print('-'*40)


def station_stats(df):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    common_start_station = df['Start Station'].mode()[0]
    print("Most Popular Start Station: ", common_start_station)

    common_end_station = df['End Station'].mode()[0]
    print("Most Popular End Station: ", common_end_station)

    df['Trip'] = df['Start Station'] + "to" + df['End Station']
    print("\nThe most frequent combination of start and end station trip is {}.\n".format(df['Trip'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    print("Total Travel Time: ", df['Trip Duration'].sum())

    print("Mean of Travel Time: ", df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    print("Count of User Types:")
    print(user_types)

    if ('Birth Year' not in df.columns) or ('Gender' not in df.columns):
        print("\nWashington doesn't have columns of 'Gender' and 'Birth Year' ")
        return

    gender_types = df['Gender'].value_counts()
    print("\nCount of Gender: ")
    print(gender_types)

    print("\nThe Earliest Year of Birth: ", df['Birth Year'].min())
    print("The Most Recent Year of Birth: ", df['Birth Year'].max())
    print("The Most Common Year of Birth: ", df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
