import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style='whitegrid')

# Load the data
hour_data = pd.read_csv("https://raw.githubusercontent.com/apriliadesa/Analisis-Data-dengan-Python/main/dashboard/hour_data.csv")
day_data = pd.read_csv("https://raw.githubusercontent.com/apriliadesa/Analisis-Data-dengan-Python/main/dashboard/day_data.csv")

# Sidebar to select dataset
dataset = st.sidebar.radio("Select Dataset", ("Hourly", "Daily"))

datetime_columns = ["dteday"]
day_data.sort_values(by="dteday", inplace=True)
day_data.reset_index(inplace=True)

for column in datetime_columns:
    day_data[column] = pd.to_datetime(day_data[column])

# Filter data
min_date = day_data["dteday"].min()
max_date = day_data["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT5d8jv89Aazu1BdpobHA9hgNNs7gbU23VbgujfpjcQ39G-o1479mRQDFPBQMQtrW5mr1Y&usqp=CAU")
    st.write("Kredit : vecteezy")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_day = day_data[(day_data["dteday"] >= str(start_date)) & 
                (day_data["dteday"] <= str(end_date))]

main_hour = hour_data[(hour_data["dteday"] >= str(start_date)) & 
                (hour_data["dteday"] <= str(end_date))]

#st.set_option('deprecation.showPyplotGlobalUse', False)

# Display the selected dataset
if dataset == "Hourly":
    st.header("Hourly Bike Sharing Data")
    st.write(main_hour.head())
else:
    st.header("Daily Bike Sharing Data")
    st.write(main_day.head())


# Visualize data
st.subheader("Bike Rental Count Over Time")
if dataset == "Hourly":
    st.write("Visualization for hourly dataset")
    
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=main_hour, x="hr", y="cnt", palette='coolwarm')
    plt.xlabel("Hour")
    plt.ylabel("Bike Rental Count")
    plt.title("Hourly Bike Rental Count Over Time")
    st.pyplot()
    
else:
    st.write("Visualization for daily dataset")
    
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=main_day, x="dteday", y="cnt", palette='coolwarm')
    plt.xlabel("Date")
    plt.ylabel("Bike Rental Count")
    plt.title("Daily Bike Rental Count Over Time")
    st.pyplot()

# Hitung rata-rata jumlah sewa sepeda per jam untuk setiap musim
seasonal_hourly_rentals = main_hour.groupby(['season', 'hr'])['cnt'].mean().reset_index()

# Hitung rata-rata jumlah sewa sepeda per jam untuk setiap musim
seasonal_daily_rentals = main_day.groupby(['season', 'mnth'])['cnt'].mean().reset_index()


st.subheader("Bike Rental Count by Season")
if dataset == "Hourly":
    plt.figure(figsize=(10, 6))
    for season in seasonal_hourly_rentals['season'].unique():
        season_data = seasonal_hourly_rentals[seasonal_hourly_rentals['season'] == season]
        plt.plot(season_data['hr'], season_data['cnt'], label='Season {}'.format(season))
    plt.xlabel('Hour')
    plt.ylabel('Average Rentals')
    plt.title('Hourly Bike Rentals by Season')
    plt.legend()
    plt.grid(True)
    st.pyplot()
    
else:
    year_2011 = main_day[main_day['yr'] == 2011]
    year_2012 = main_day[main_day['yr'] == 2012]

    monthly_rentals_2011 = year_2011.groupby('season')['cnt'].mean().reset_index()
    monthly_rentals_2012 = year_2012.groupby('season')['cnt'].mean().reset_index()
    
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    sns.barplot(data=monthly_rentals_2011, x='season', y='cnt')
    plt.title('Average Season Rentals in 2011')
    plt.xlabel('Season')
    plt.xticks(rotation=45)
    plt.ylabel('Average Rentals')
    
    plt.subplot(1, 2, 2)
    sns.barplot(data=monthly_rentals_2012, x='season', y='cnt')
    plt.title('Average Season Rentals in 2012')
    plt.xlabel('Season')
    plt.xticks(rotation=45)
    plt.ylabel('Average Rentals') 
    plt.tight_layout()
    st.pyplot()

month_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
st.subheader("Bike Rental Count by Month")
if dataset == "Hourly":
    year_2011_hour = main_hour[main_hour['yr'] == 2011]
    year_2012_hour = main_hour[main_hour['yr'] == 2012]
    
    monthly_rentals_2011_hour = year_2011_hour.groupby('mnth')['cnt'].mean().reset_index()
    monthly_rentals_2012_hour = year_2012_hour.groupby('mnth')['cnt'].mean().reset_index()
        
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    sns.barplot(data=monthly_rentals_2011_hour, x='mnth', y='cnt', order=month_order)
    plt.title('Average Monthly Rentals in 2011')
    plt.xlabel('Month')
    plt.xticks(rotation=45)
    plt.ylabel('Average Rentals')
        
    plt.subplot(1, 2, 2)
    sns.barplot(data=monthly_rentals_2012_hour, x='mnth', y='cnt', order=month_order)
    plt.title('Average Monthly Rentals in 2012')
    plt.xlabel('Month')
    plt.xticks(rotation=45)
    plt.ylabel('Average Rentals') 
    plt.tight_layout()
    st.pyplot()
else:
    year_2011_daily = main_day[main_day['yr'] == 2011]
    year_2012_daily = main_day[main_day['yr'] == 2012]
    
    monthly_rentals_2011_daily = year_2011_daily.groupby('mnth')['cnt'].mean().reset_index()
    monthly_rentals_2012_daily = year_2012_daily.groupby('mnth')['cnt'].mean().reset_index()
        
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    sns.barplot(data=monthly_rentals_2011_daily, x='mnth', y='cnt', order=month_order)
    plt.title('Average Monthly Rentals in 2011')
    plt.xlabel('Month')
    plt.xticks(rotation=45)
    plt.ylabel('Average Rentals')
        
    plt.subplot(1, 2, 2)
    sns.barplot(data=monthly_rentals_2012_daily, x='mnth', y='cnt', order=month_order)
    plt.title('Average Monthly Rentals in 2012')
    plt.xlabel('Month')
    plt.xticks(rotation=45)
    plt.ylabel('Average Rentals') 
    plt.tight_layout()
    st.pyplot()
