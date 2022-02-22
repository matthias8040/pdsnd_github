import time
import pandas as pd
import numpy as np
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # print('\n*** Start select Filter ***')
    # user input for city (chicago, new york city, washington)
    city = []
    cities = []
    for key in CITY_DATA:
        cities.append(key)
    while city == []:
        city = input("Which city (Chicago, New York City or Washington) would you like to analyze?\n").lower()
        #city = city.lower()
        #if city not in cities:
        if city not in CITY_DATA:
            print('Please select 1 of the 3 cities.')
            city=[]

    time_filters = ['none','month', 'day']        
    days = ['all','mo','tu','we','th','fr','sa','su']
    months = ['all','january','february','march','april','may','june']
    time_filter = []
    day = []
    month = []   
        
    # user input for time filter (month, day, none)   
    while  time_filter == []:
        time_filter = input('Would you like to filter the data by month, day or not at all? Type "none" for no time filter?\n')
        time_filter = time_filter.lower()
        if time_filter not in time_filters:
            print('Please select 1 of the 3 time_filters ("month","day","none").')
            time_filter=[] 
    
    #  user input for month (all, january, february, ... , june) and for day of week (all, monday, tuesday, ... sunday)
    if time_filter == 'month':
       while month == []:
            day = 'all'
            month = input("Which month? January, February, March, April, May or June? Please type out the full month?\n").lower()
            #month = month.lower()
            if month not in months:
                print('Please select 1 of the 6 month ("January","February","March","April","May","June").')
                month=[]          
    elif time_filter == 'day':
        while day == []:
            month = 'all'
            day = input("Which day? Mo, Tu, We, Th, Fr, Sa or Su? Please select one day?\n").lower()
            #day = daylower()
            if day not in days:
                print('Please select 1 of the 7 days ("Mo","Tu","We","Th","Fr","Sa" or "Su").')
                day=[]                         
    elif time_filter == 'none':
            month = 'all'
            day = 'all'

    """
    print("\n\nSelected city: {}.".format(city))
    print("Selected month: {}.".format(month))
    print("Selected day: {}.".format(day))
    """
    # print('\n*** End select Filter ***')
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # print('_'*40)
    # print('\n*** Start load and filter Data ***')
    print("\nSelected city: {}.".format(city))
    print("Selected month: {}.".format(month))
    print("Selected day: {}.".format(day))
    
    filename = CITY_DATA[city]
    print("\nLoad File: {}.".format(filename))
    df = pd.read_csv(filename)
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['weekday'] = df['Start Time'].dt.weekday
    df['dayofweek'] = df['Start Time'].dt.day_name()
    # print(df.head())  
    
    # Show raw data
    show_rows = input('Want to see first 5 rows raw data? Enter yes or no.\n')
    row_idx = 0
    total_rows = len(df.index)
    while show_rows.lower() == 'yes':
        print(df.iloc[row_idx:row_idx+5,:])
        row_idx += 5
        if row_idx >= total_rows:        
            print('All rows have been shown')
            show_rows = input('Enter any key to continue.\n') 
            break
        else:
            show_rows = input('Want to see 5 more rows raw data? Enter yes or no.\n')            
                     
     # filter by month to create the new dataframe
    if month != 'all':
        print('filter Data by: {}'.format(month))
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    if day != 'all':
        abr_dow= {
            'mo': 'Monday',
            'tu': 'Tuesday',
            'we': 'Wednesday',
            'th': 'Thursday',
            'fr': 'Friday',
            'sa': 'Saturday',
            'su': 'Sunday'
        }
        dayofweek = abr_dow.get(day)
        #print('\nFilter Data by: {}'.format(dayofweek))
        df = df[df['dayofweek'] == dayofweek]


    #print('Filtered Data:')
    #print(df.head())  
    # print('\n*** End load and filter Data ***')
    print('_'*40)
    return df


def time_stats(df,city, month, day):
    """Displays statistics on the most frequent times of travel."""
    
    # print('\nCalculating The Most Frequent Times of Travel...\n')    
    start_time = time.time()      
    print('Selectetd Filter:  - city: "{}"    - month: "{}"   - day: "{}".\n'.format(city, month, day))
    
    # display the most common month
    popular_month = df['month'].mode()[0]
    #print('Most Popular Month:', popular_month)    
    print('Most Popular Month:', calendar.month_name[popular_month])
    #popular_months = df['month'].value_counts()
    #print('month:')
    #print(popular_months)
    

    # display the most common day of week
    popular_dow = df['dayofweek'].mode()[0]
    print('Most Popular Day:', popular_dow)
    #popular_dows = df['dayofweek'].value_counts()
    #print('Days of week:')
    #print(popular_dows)
    

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)
    #popular_hours = df['hour'].value_counts()
    #print('Start Hour´s:')
    #print(popular_hours)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df,city, month, day):
    """Displays statistics on the most popular stations and trip."""

    # print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    print('Selectetd Filter:  - city: "{}"    - month: "{}"   - day: "{}"".\n'.format(city, month, day))

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most commonly used Start Station:', popular_start_station)
    #popular_start_stations = df['Start Station'].value_counts()
    #print('Start Stations:')
    #print(popular_start_stations)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most commonly used End Station:', popular_end_station)
    #popular_end_stations = df['End Station'].value_counts()
    #print('End Stations:')
    #print(popular_end_stations)


    # display most frequent combination of start station and end station trip
    df_station = df.groupby(['Start Station','End Station']) ['Start Station'].count().reset_index(name='count').sort_values(['count'], ascending=False)    
    print('Most frequent combination of start station and end station: ', df_station['Start Station'].iloc[0], ' and ', df_station['End Station'].iloc[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df,city, month, day):
    """Displays statistics on the total and average trip duration."""

    # print('\nCalculating Trip Duration...\n')    
    start_time = time.time()    
    print('Selectetd Filter:  - city: "{}"    - month: "{}"   - day: "{}"".\n'.format(city, month, day))

    # display total travel time
    Total = sum(df['Trip Duration'])
    hours = int(Total // (60 * 60))
    mins = int((Total // 60) % 60)
    secs = int(Total % 60)
    print('Total travel times: ', Total, 'sec')
    print('   or hours: ', hours)
    print('      minutes: ', mins)
    print('      seconds: ', secs)


    # display mean travel time    
    Total = df['Trip Duration'].mean()
    hours = int(Total // (60 * 60))
    mins = int((Total // 60) % 60)
    secs = int(Total % 60)
    print('Mean travel time: ', Total, 'sec')
    print('   or hours: ', hours)
    print('      minutes: ', mins)
    print('      seconds: ', secs)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city, month, day):
    """Displays statistics on bikeshare users."""

    # print('\nCalculating User Stats...\n')
    start_time = time.time()
    print('Selectetd Filter:  - city: "{}"    - month: "{}"   - day: "{}"".\n'.format(city, month, day))

    # Display counts of user types
    if 'User Type' in df.columns:
        user_types = df['User Type'].value_counts()
        print('User types:')
        print(user_types)
    else:
       print('no information about the user type.')

    # Display counts of gender
    if 'Gender' in df.columns:
        countGender   = df['Gender'].value_counts()
        print(countGender)
    else:
       print('no information about the gender.')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('earliest year of birth:', int(df['Birth Year'].min()))
        print('most recent year of birth:',int(df['Birth Year'].max()))    
        print('most common year of birth:', int(df['Birth Year'].mode()))
    else:
       print('no information about the Birth Year.')
        
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        """
        #print("City: {}".format(city))
        #city='chicago'        
        #month='all'
        #day='mo'        
        #month='june'
        #day='all'        
        print("\n\nSelected city: {}.".format(city))
        print("Selected month: {}.".format(month))
        print("Selected day: {}.".format(day))
        """
        df = load_data(city, month, day)

        time_stats(df,city, month, day)
        
        station_stats(df,city, month, day)
        
        trip_duration_stats(df,city, month, day)
        
        user_stats(df,city, month, day)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
