import datetime as dt
import pandas as pd
import numpy as np
import time

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

months = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December','All')
days = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday','All')

def get_filters():

    print('Hello! Let\'s explore some US bikeshare data!')

    city = ''
    month = ''
    day = ''
    cities = ('Chicago', 'New York City', 'Washington')
    invalid = 'Sorry, not a valid input'

    while city not in cities:
        city = (input('Please enter the city you\'d like to view. Availible cities are Chicago, New York City, and Washington :')).title()
        if city not in cities:
            print(invalid)
    print('You have selected:  {}'.format(city))

    while month not in months:
        month = (input('Enter a month to filter by (for no filter, enter "All"):')).title()
        if month not in months:
            print(invalid)
    print('You have selected: {}'.format(month))

    while day not in days:
        day = (input('Enter a day to filter by (for no filter, enter "All") :')).title()
        if day not in days:
            print(invalid)
    print('You have selected data for: \nCity: {}\nMonth: {}\nDay: {} '.format(city, month, day))
    print('-'*40)
    return city, month, day


def load_data(city, month, day):

    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday_name

    if month != 'All':
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'All':
        df = df[df['day'] == day]

    return df


def time_stats(df):

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    month_mode_index = df['month'].mode() - 1
    month_mode = months[month_mode_index[0]]
    print('Most frequent month: {}'.format(month_mode))

    day_mode = df['day'].mode()
    print('Most frequent day: {}'.format(day_mode[0]))

    df['hour'] = df['Start Time'].dt.hour
    hours = ('1am','2am','3am','4am','5am','6am','7am','8am','9am','10am','11am','12pm','1pm','2pm','3pm','4pm','5pm','6pm','7pm','8pm','9pm','10pm','11pm','12am')
    start_hour_mode_index = df['hour'].mode() - 1
    start_hour_mode = hours[start_hour_mode_index[0]]
    print('Most frequent hour: {}'.format(start_hour_mode))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()


    start_station_mode = df['Start Station'].mode()
    print('most common start station: {}'.format(start_station_mode[0]))

    end_station_mode = df['End Station'].mode()
    print('most common end station: {}'.format(end_station_mode[0]))

    df['start_end'] = 'from ' + df['Start Station'].map(str) + ' to ' + df['End Station']
    trip_mode = df['start_end'].mode()
    print('The most common trip is {}'.format(trip_mode[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#There must be a library with a funtion that could simplify the time conversion here, need to find it
def trip_duration_stats(df):

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    trip_days = sum(df['Trip Duration']) // 86400
    trip_hours = (sum(df['Trip Duration']) % 86400) // 3600
    trip_minutes = ((sum(df['Trip Duration']) % 86400) % 3600) // 60
    print('Total duration of all trips: {} days, {} hours, and {} minutes'.format(trip_days, trip_hours, trip_minutes))

    trip_mean = round(np.mean(df['Trip Duration'])/60,2)
    print('Average trip time: {} minutes'.format(trip_mean))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    customer_count = df[(df['User Type'] == 'Customer')].count()
    subscriber_count = df[(df['User Type'] == 'Subscriber')].count()
    print('Count of Customers: {} \nCount of Subscribers: {}'.format(customer_count[0],subscriber_count[0]))

    if 'Gender' in df.columns:
        male_count = df[(df['Gender'] == 'Male')].count()
        female_count = df[(df['Gender'] == 'Female')].count()
        print('\nCount of Male Users: {}\nCount of Female Users: {}'.format(male_count[0],female_count[0]))

    if 'Birth Year' in df.columns:
        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        most_common_birth_year = int(round(df['Birth Year'].mean()))
        print('\nEarliest Birth Year: {}\nMost Recent Birth Year: {}\nMost Common Birth Year: {}'.format(earliest_birth_year,most_recent_birth_year,most_common_birth_year))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# There's a simpler way to update the indexing here, need to look into it
def display_data(df):
    data_request = input('Would you like to see a sample of the raw data?:')
    start_index = 0
    end_index = 5
    while data_request.title() == 'Yes':
        print(df[start_index:end_index])
        start_index += 5
        end_index += 5
        data_request = input('Display 5 more rows?:')

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
