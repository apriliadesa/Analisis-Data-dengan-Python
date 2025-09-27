import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
#import folium
#from streamlit_folium import st_folium

sns.set(style='whitegrid')

# =============================
# Load the data
# =============================
hour_data = pd.read_csv("https://raw.githubusercontent.com/apriliadesa/Analisis-Data-dengan-Python/main/dashboard/hour_data.csv")
day_data = pd.read_csv("https://raw.githubusercontent.com/apriliadesa/Analisis-Data-dengan-Python/main/dashboard/day_data.csv")

# Sidebar select dataset
dataset = st.sidebar.radio("Select Dataset", ("Hourly", "Daily"))

# Preprocessing datetime
day_data["dteday"] = pd.to_datetime(day_data["dteday"])
day_data.sort_values(by="dteday", inplace=True)
day_data.reset_index(drop=True, inplace=True)

# Filter rentang waktu
min_date = day_data["dteday"].min()
max_date = day_data["dteday"].max()

with st.sidebar:
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT5d8jv89Aazu1BdpobHA9hgNNs7gbU23VbgujfpjcQ39G-o1479mRQDFPBQMQtrW5mr1Y&usqp=CAU")
    st.write("Kredit : vecteezy")

    start_date, end_date = st.date_input(
        label="Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_day = day_data[(day_data["dteday"] >= str(start_date)) & (day_data["dteday"] <= str(end_date))]
main_hour = hour_data[(hour_data["dteday"] >= str(start_date)) & (hour_data["dteday"] <= str(end_date))]

# =============================
# Dataset Preview
# =============================
if dataset == "Hourly":
    st.header("Hourly Bike Sharing Data")
    st.write(main_hour.head())
else:
    st.header("Daily Bike Sharing Data")
    st.write(main_day.head())

# =============================
# Visualization: Bike Rental Count Over Time
# =============================
st.subheader("Bike Rental Count Over Time")
if dataset == "Hourly":
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=main_hour, x="hr", y="cnt", ax=ax, palette="coolwarm")
    ax.set_xlabel("Hour")
    ax.set_ylabel("Bike Rental Count")
    ax.set_title("Hourly Bike Rental Count Over Time")
    st.pyplot(fig)
else:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=main_day, x="dteday", y="cnt", ax=ax, palette="coolwarm")
    ax.set_xlabel("Date")
    ax.set_ylabel("Bike Rental Count")
    ax.set_title("Daily Bike Rental Count Over Time")
    st.pyplot(fig)

# =============================
# Advanced Analysis Section
# =============================
st.header("Advanced Analytics")

# --- 1. RFM Analysis (dummy customer data) ---
st.subheader("RFM Analysis (Dummy Example)")
dummy_df = pd.DataFrame({
    "customer_id": [1,1,2,2,3,3,3],
    "order_date": pd.to_datetime([
        "2021-07-01","2021-07-20","2021-07-05",
        "2021-08-10","2021-07-02","2021-07-15","2021-08-01"
    ]),
    "amount": [200, 150, 300, 250, 100, 200, 150]
})
ref_date = dummy_df["order_date"].max()
rfm = dummy_df.groupby("customer_id").agg({
    "order_date": lambda x: (ref_date - x.max()).days,  # Recency
    "customer_id": "count",  # Frequency
    "amount": "sum"          # Monetary
}).rename(columns={"order_date": "Recency", "customer_id": "Frequency", "amount": "Monetary"})
st.write(rfm)

# # --- 2. Geospatial Analysis ---
# st.subheader("Geospatial Analysis (Dummy Example)")
# locations = [(-6.2, 106.8), (-7.8, 110.4), (-6.9, 107.6)]  # Jakarta, Jogja, Bandung
# m = folium.Map(location=[-6.5, 107], zoom_start=6)
# for loc in locations:
#     folium.Marker(location=loc, popup="Bike Rental Station").add_to(m)
# st_folium(m, width=700, height=450)

# --- 3. Clustering (Manual Grouping + Binning) ---
st.subheader("Clustering tanpa ML")

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

st.write("Preview dengan Clustering Manual:")
st.write(main_hour[["hr", "cnt", "time_group", "demand_group"]].head())

# Visualisasi clustering
fig, ax = plt.subplots(figsize=(10, 6))
sns.countplot(data=main_hour, x="time_group", hue="demand_group", ax=ax)
ax.set_title("Distribusi Demand berdasarkan Kelompok Waktu")
st.pyplot(fig)
