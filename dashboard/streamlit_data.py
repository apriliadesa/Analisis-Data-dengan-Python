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

# Pastikan kolom dteday jadi datetime
day_data["dteday"] = pd.to_datetime(day_data["dteday"])
hour_data["dteday"] = pd.to_datetime(hour_data["dteday"])

# Filter date range
min_date = day_data["dteday"].min().date()
max_date = day_data["dteday"].max().date()

with st.sidebar:
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT5d8jv89Aazu1BdpobHA9hgNNs7gbU23VbgujfpjcQ39G-o1479mRQDFPBQMQtrW5mr1Y&usqp=CAU")
    st.write("Img Source : vecteezy")
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Ubah ke datetime64 untuk filtering
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

main_day = day_data[(day_data["dteday"] >= start_date) & 
                    (day_data["dteday"] <= end_date)]

main_hour = hour_data[(hour_data["dteday"] >= start_date) & 
                      (hour_data["dteday"] <= end_date)]


# Display the selected dataset
# Display the selected dataset
if dataset == "Hourly":
    st.header("Hourly Bike Sharing Data")
    st.write(main_hour.head())
else:
    st.header("Daily Bike Sharing Data")
    st.write(main_day.head())
# if dataset == "Hourly":
#     st.header("Hourly Bike Sharing Data")
#     st.write(main_hour.head())

#     # --- RFM Analysis (tanpa Frequency) ---
#     main_hour["dteday"] = pd.to_datetime(main_hour["dteday"])
#     snapshot_date = main_hour["dteday"].max() + pd.Timedelta(days=1)

#     rfm = main_hour.groupby("dteday").agg({
#         "cnt": "sum"
#     }).reset_index()

#     rfm["Recency"] = (snapshot_date - rfm["dteday"]).dt.days
#     rfm["Monetary"] = rfm["cnt"]

#     rfm["R_Score"] = pd.qcut(rfm["Recency"], 4, labels=[4,3,2,1])
#     rfm["M_Score"] = pd.qcut(rfm["Monetary"], 4, labels=[1,2,3,4])

#     rfm["RFM_Segment"] = rfm["R_Score"].astype(str) + rfm["M_Score"].astype(str)
#     rfm["RFM_Score"] = rfm[["R_Score","M_Score"]].astype(int).sum(axis=1)

#     st.subheader("RFM Analysis (Hourly)")
#     st.dataframe(rfm.head(10))

# else:
#     st.header("Daily Bike Sharing Data")
#     st.write(main_day.head())

#     # --- RFM Analysis (tanpa Frequency) ---
#     main_day["dteday"] = pd.to_datetime(main_day["dteday"])
#     snapshot_date = main_day["dteday"].max() + pd.Timedelta(days=1)

#     rfm = main_day.groupby("dteday").agg({
#         "cnt": "sum"
#     }).reset_index()

#     rfm["Recency"] = (snapshot_date - rfm["dteday"]).dt.days
#     rfm["Monetary"] = rfm["cnt"]

#     rfm["R_Score"] = pd.qcut(rfm["Recency"], 4, labels=[4,3,2,1])
#     rfm["M_Score"] = pd.qcut(rfm["Monetary"], 4, labels=[1,2,3,4])

#     rfm["RFM_Segment"] = rfm["R_Score"].astype(str) + rfm["M_Score"].astype(str)
#     rfm["RFM_Score"] = rfm[["R_Score","M_Score"]].astype(int).sum(axis=1)

#     st.subheader("RFM Analysis (Daily)")
#     st.dataframe(rfm.head(10))


# --- Visualization 1 ---
st.subheader("Bike Rental Count Over Time")
if dataset == "Hourly":
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=main_hour, x="hr", y="cnt", ax=ax, palette='coolwarm')
    ax.set_xlabel("Hour")
    ax.set_ylabel("Bike Rental Count")
    ax.set_title("Hourly Bike Rental Count Over Time")
    st.pyplot(fig)
else:
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=main_day, x="dteday", y="cnt", ax=ax, palette='coolwarm')
    ax.set_xlabel("Date")
    ax.set_ylabel("Bike Rental Count")
    ax.set_title("Daily Bike Rental Count Over Time")
    st.pyplot(fig)

# --- Visualization 2 ---
seasonal_hourly_rentals = main_hour.groupby(['season', 'hr'])['cnt'].mean().reset_index()
seasonal_daily_rentals = main_day.groupby(['season', 'mnth'])['cnt'].mean().reset_index()

st.subheader("Bike Rental Count by Season")
if dataset == "Hourly":
    fig, ax = plt.subplots(figsize=(10, 4))
    for season in seasonal_hourly_rentals['season'].unique():
        season_data = seasonal_hourly_rentals[seasonal_hourly_rentals['season'] == season]
        ax.plot(season_data['hr'], season_data['cnt'], label=f'Season {season}')
    ax.set_xlabel('Hour')
    ax.set_ylabel('Average Rentals')
    ax.set_title('Hourly Bike Rentals by Season')
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
else:
    year_2011 = main_day[main_day['yr'] == 2011]
    year_2012 = main_day[main_day['yr'] == 2012]

    monthly_rentals_2011 = year_2011.groupby('season')['cnt'].mean().reset_index()
    monthly_rentals_2012 = year_2012.groupby('season')['cnt'].mean().reset_index()
    
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    sns.barplot(data=monthly_rentals_2011, x='season', y='cnt', ax=axes[0])
    axes[0].set_title('Average Season Rentals in 2011')
    axes[0].set_xlabel('Season')
    axes[0].set_ylabel('Average Rentals')

    sns.barplot(data=monthly_rentals_2012, x='season', y='cnt', ax=axes[1])
    axes[1].set_title('Average Season Rentals in 2012')
    axes[1].set_xlabel('Season')
    axes[1].set_ylabel('Average Rentals')

    fig.tight_layout()
    st.pyplot(fig)

# --- Visualization 3 ---
month_order = ["January", "February", "March", "April", "May", "June", "July",
               "August", "September", "October", "November", "December"]

# Mapping angka bulan -> nama bulan
month_map = {
    1: "January", 2: "February", 3: "March", 4: "April",
    5: "May", 6: "June", 7: "July", 8: "August",
    9: "September", 10: "October", 11: "November", 12: "December"
}

st.subheader("Bike Rental Count by Month")

if dataset == "Hourly":
    year_2011_hour = main_hour[main_hour['yr'] == 2011]
    year_2012_hour = main_hour[main_hour['yr'] == 2012]
    
    monthly_rentals_2011_hour = year_2011_hour.groupby('mnth')['cnt'].mean().reset_index()
    monthly_rentals_2012_hour = year_2012_hour.groupby('mnth')['cnt'].mean().reset_index()

    # Buat palette highlight
    palette_2011 = ["C0"] * 12
    palette_2012 = ["C0"] * 12
    palette_2011[5] = "orange"   # Juli (7) -> index 6
    palette_2012[8] = "red"      # Juni (6) -> index 5

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    sns.barplot(data=monthly_rentals_2011_hour, x='mnth', y='cnt', ax=axes[0], order=month_order, palette=palette_2011)
    axes[0].set_title('Average Monthly Rentals in 2011')
    axes[0].set_xlabel('Month')
    axes[0].set_ylabel('Average Rentals')
    axes[0].tick_params(axis='x', rotation=45)
    
    sns.barplot(data=monthly_rentals_2012_hour, x='mnth', y='cnt', ax=axes[1], order=month_order, palette=palette_2012)
    axes[1].set_title('Average Monthly Rentals in 2012')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Average Rentals')
    axes[1].tick_params(axis='x', rotation=45)

    fig.tight_layout()
    st.pyplot(fig)

else:
    year_2011_daily = main_day[main_day['yr'] == 2011]
    year_2012_daily = main_day[main_day['yr'] == 2012]
    
    monthly_rentals_2011_daily = year_2011_daily.groupby('mnth')['cnt'].mean().reset_index()
    monthly_rentals_2012_daily = year_2012_daily.groupby('mnth')['cnt'].mean().reset_index()

    # Buat palette highlight
    palette_2011 = ["C0"] * 12
    palette_2012 = ["C0"] * 12
    palette_2011[5] = "orange"   # Juli (7) -> index 6
    palette_2012[8] = "red"      # Juni (6) -> index 5

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    sns.barplot(data=monthly_rentals_2011_daily, x='mnth', y='cnt', ax=axes[0], order=month_order, palette=palette_2011)
    axes[0].set_title('Average Monthly Rentals in 2011')
    axes[0].set_xlabel('Month')
    axes[0].set_ylabel('Average Rentals')
    axes[0].tick_params(axis='x', rotation=45)
    
    sns.barplot(data=monthly_rentals_2012_daily, x='mnth', y='cnt', ax=axes[1], order=month_order, palette=palette_2012)
    axes[1].set_title('Average Monthly Rentals in 2012')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Average Rentals')
    axes[1].tick_params(axis='x', rotation=45)

    fig.tight_layout()
    st.pyplot(fig)



# --- Clustering Manual ---
st.subheader("Clustering : Time Group & Demand Group")
if dataset == "Hourly":
    # Group jam menjadi kategori waktu
    def time_group(hour):
        if 0 <= hour < 7:
            return "Dini Hari"
        elif 7 <= hour < 13:
            return "Pagi"
        elif 13 <= hour < 19:
            return "Siang"
        else:
            return "Malam"

    main_hour["time_group"] = main_hour["hr"].apply(time_group)

    # Binning demand (cnt)
    bins = [0, 100, 500, main_hour["cnt"].max()]
    labels = ["Low", "Medium", "High"]
    main_hour["demand_group"] = pd.cut(main_hour["cnt"], bins=bins, labels=labels, include_lowest=True)

    # st.write("Preview dengan Clustering Manual:")
    # st.write(main_hour[["hr", "cnt", "time_group", "demand_group"]].head())

    # Visualisasi clustering
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(data=main_hour, x="time_group", hue="demand_group", ax=ax)
    ax.set_title("Distribusi Demand berdasarkan Kelompok Waktu")
    ax.set_xlabel("Kelompok Waktu")
    ax.set_ylabel("Jumlah")
    st.pyplot(fig)

else:
    # Binning demand untuk data harian
    bins = [0, 1000, 4000, main_day["cnt"].max()]
    labels = ["Low", "Medium", "High"]
    main_day["demand_group"] = pd.cut(main_day["cnt"], bins=bins, labels=labels, include_lowest=True)

    # st.write("Preview dengan Clustering Manual:")
    # st.write(main_day[["dteday", "cnt", "demand_group"]].head())

    # Visualisasi clustering
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(data=main_day, x="demand_group", ax=ax)
    ax.set_title("Distribusi Demand Harian")
    ax.set_xlabel("Kelompok Demand")
    ax.set_ylabel("Jumlah Hari")
    st.pyplot(fig)
