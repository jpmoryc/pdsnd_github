import time
import pandas as pd
import numpy as np

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Get user input for city
    while True:
        city = input("Enter the city name (Chicago, New York City, Washington): ").strip().lower()
        if city in CITY_DATA:
            break
        else:
            print("Invalid input. Please choose from Chicago, New York City, or Washington.")

    # Get user input for month
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        month = input("Enter the month (January to June) or 'all' for no filter: ").strip().lower()
        if month in months:
            break
        else:
            print("Invalid input. Please enter a valid month name or 'all'.")

    # Get user input for day of week
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while True:
        day = input("Enter the day of the week (Monday to Sunday) or 'all' for no filter: ").strip().lower()
        if day in days:
            break
        else:
            print("Invalid input. Please enter a valid day or 'all'.")

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    """
    df = pd.read_csv(CITY_DATA[city])

    # Convert Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month, day of week, and hour from Start Time
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    df['hour'] = df['Start Time'].dt.hour

    # Filter by month
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_index = months.index(month) + 1
        df = df[df['month'] == month_index]

    # Filter by day
    if day != 'all':
        df = df[df['day_of_week'] == day.lower()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Most common month
    popular_month = df['month'].mode()[0]
    print(f"Most Common Month: {popular_month}")

    # Most common day of week
    popular_day = df['day_of_week'].mode()[0].title()
    print(f"Most Common Day of Week: {popular_day}")

    # Most common hour of day
    popular_hour = df['hour'].mode()[0]
    print(f"Most Common Hour of Day: {popular_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Most common start station
    start_station = df['Start Station'].mode()[0]
    print(f"Most Common Start Station: {start_station}")

    # Most common end station
    end_station = df['End Station'].mode()[0]
    print(f"Most Common End Station: {end_station}")

    # Most common trip from start to end 
    df['trip'] = df['Start Station'] + " to " + df['End Station']
    most_common_trip = df['trip'].mode()[0]
    print(f"Most Common Trip: {most_common_trip}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Total travel time in seconds
    total_travel_time = df['Trip Duration'].sum()
    
    # Convert total travel time to hours, minutes, seconds
    total_hours = int(total_travel_time // 3600)
    total_minutes = int((total_travel_time % 3600) // 60)
    total_seconds = int(total_travel_time % 60)
    print(f"Total Travel Time: {total_hours} hours, {total_minutes} minutes, {total_seconds} seconds")

    # Mean travel time in seconds
    mean_travel_time = df['Trip Duration'].mean()
   
    # Convert mean travel time to minutes and seconds
    mean_minutes = int(mean_travel_time // 60)
    mean_seconds = int(mean_travel_time % 60)
    print(f"Average Travel Time: {mean_minutes} minutes, {mean_seconds} seconds")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Counts of user types
    print("User Types:")
    print(df['User Type'].value_counts())

    # Counts of gender
    if 'Gender' in df.columns:
        print("\nGender Distribution:")
        print(df['Gender'].value_counts())
    else:
        print("\nNo gender data available for this city.")

    # Birth year
    if 'Birth Year' in df.columns:
        earliest = int(df['Birth Year'].min())
        most_recent = int(df['Birth Year'].max())
        most_common = int(df['Birth Year'].mode()[0])
        print(f"\nEarliest Birth Year: {earliest}")
        print(f"Most Recent Birth Year: {most_recent}")
        print(f"Most Common Birth Year: {most_common}")
    else:
        print("\nNo birth year data available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """Displays 5 rows of raw data upon request from user."""
    index = 0
    while True:
        raw_input = input("Would you like to see 5 lines of raw data? Enter yes or no: ").lower()
        if raw_input != 'yes':
            break
        print(df.iloc[index:index+5])
        index += 5
        if index >= len(df):
            print("No more data to display.")
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no: ').lower()
        if restart != 'yes':
            print("Thanks for using the Bikeshare Data Explorer!")
            break

if __name__ == "__main__":
    main()