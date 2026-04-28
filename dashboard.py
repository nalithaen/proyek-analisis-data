import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='darkgrid')

# ========================
# LOAD DATA
# ========================
df = pd.read_csv("main_data.csv")

# Convert datetime
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
df['order_delivered_customer_date'] = pd.to_datetime(df['order_delivered_customer_date'])
df['order_estimated_delivery_date'] = pd.to_datetime(df['order_estimated_delivery_date'])

# ========================
# SIDEBAR
# ========================
with st.sidebar:
    st.title("📊 Olist Dashboard")
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png")

    min_date = df['order_purchase_timestamp'].min()
    max_date = df['order_purchase_timestamp'].max()

    start_date, end_date = st.date_input(
        label="Pilih Rentang Tanggal",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter data
main_df = df[
    (df['order_purchase_timestamp'] >= str(start_date)) &
    (df['order_purchase_timestamp'] <= str(end_date))
]

# ========================
# HELPER FUNCTION
# ========================

def create_rfm(df):
    snapshot_date = df['order_purchase_timestamp'].max()

    rfm = df.groupby('customer_unique_id').agg({
        'order_purchase_timestamp': lambda x: (snapshot_date - x.max()).days,
        'order_id': 'nunique',
        'price': 'sum'
    }).reset_index()

    rfm.columns = ['customer_id', 'recency', 'frequency', 'monetary']
    return rfm


def create_city_summary(df):
    snapshot_date = df['order_purchase_timestamp'].max()

    rfm = df.groupby(['customer_unique_id', 'customer_city']).agg({
        'order_purchase_timestamp': lambda x: (snapshot_date - x.max()).days,
        'order_id': 'nunique',
        'price': 'sum'
    }).reset_index()

    rfm.columns = ['customer_id', 'city', 'recency', 'frequency', 'monetary']

    top_cities = rfm['city'].value_counts().head(10).index
    rfm_top = rfm[rfm['city'].isin(top_cities)]

    summary = rfm_top.groupby('city').agg({
        'recency': 'mean',
        'frequency': 'mean',
        'monetary': 'mean',
        'customer_id': 'count'
    }).reset_index()

    summary.rename(columns={'customer_id': 'num_customers'}, inplace=True)
    return summary


def create_delay_analysis(df):
    df['delivery_delay'] = (
        df['order_delivered_customer_date'] -
        df['order_estimated_delivery_date']
    ).dt.days

    category = df.groupby('product_category_name_english').agg({
        'review_score': 'mean',
        'delivery_delay': 'mean'
    }).reset_index()

    return category


# ========================
# DASHBOARD
# ========================

st.header("📦 Olist E-Commerce Dashboard")

# ========================
# KPI
# ========================
col1, col2, col3 = st.columns(3)

with col1:
    total_orders = main_df['order_id'].nunique()
    st.metric("Total Orders", total_orders)

with col2:
    total_revenue = format_currency(main_df['price'].sum(), "R$", locale='es_CO')
    st.metric("Total Revenue", total_revenue)

with col3:
    avg_review = round(main_df['review_score'].mean(), 2)
    st.metric("Avg Review Score", avg_review)

# ========================
# GEOSPATIAL ANALYSIS
# ========================
st.subheader("🌍 Top 10 Cities Customer Distribution (Geospatial)")

# Load geolocation dataset
geo = pd.read_csv("../data/geolocation_dataset.csv")

# Preprocessing
geo['geolocation_city'] = geo['geolocation_city'].str.lower()
main_df['customer_city'] = main_df['customer_city'].str.lower()

geo_city = geo.groupby('geolocation_city').agg({
    'geolocation_lat': 'mean',
    'geolocation_lng': 'mean'
}).reset_index()

# Merge dengan data utama
map_df = main_df.merge(
    geo_city,
    left_on='customer_city',
    right_on='geolocation_city',
    how='left'
)

# Ambil top 10 kota
top_cities = map_df['customer_city'].value_counts().head(10).index
map_df = map_df[map_df['customer_city'].isin(top_cities)]

# Agregasi
map_plot = map_df.groupby('customer_city').agg({
    'geolocation_lat': 'mean',
    'geolocation_lng': 'mean',
    'price': 'sum'
}).reset_index()

# Rename untuk streamlit
map_plot.rename(columns={
    'geolocation_lat': 'lat',
    'geolocation_lng': 'lon'
}, inplace=True)

# Tampilkan map
st.map(map_plot)

top_city_rev = map_plot.sort_values(by="price", ascending=False)

fig, ax = plt.subplots(figsize=(10,6))
sns.barplot(
    x='price',
    y='customer_city',
    data=top_city_rev,
    ax=ax
)

ax.set_xlabel("Revenue (R$)")
ax.set_ylabel("City")

st.pyplot(fig)

# ========================
# RFM ANALYSIS
# ========================
st.subheader("📊 RFM Analysis per City")

city_summary = create_city_summary(main_df)

fig, ax = plt.subplots(figsize=(12,6))
sns.barplot(x='monetary', y='city', data=city_summary, ax=ax)
ax.set_title("Average Monetary by City")
st.pyplot(fig)

# ========================
# DELIVERY vs REVIEW
# ========================
st.subheader("🚚 Delivery Delay vs Review Score")

category = create_delay_analysis(main_df)

fig, ax = plt.subplots(figsize=(10,6))
sns.scatterplot(
    x='delivery_delay',
    y='review_score',
    data=category,
    ax=ax
)
ax.set_title("Delivery Delay vs Review Score")
st.pyplot(fig)

# ========================
# LOWEST REVIEW
# ========================
st.subheader("⚠️ Lowest Review Categories")

st.dataframe(category.sort_values(by='review_score').head(10))

# ========================
# RFM DISTRIBUTION
# ========================
st.subheader("👥 Customer RFM Distribution")

rfm = create_rfm(main_df)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Avg Recency", round(rfm.recency.mean(),1))

with col2:
    st.metric("Avg Frequency", round(rfm.frequency.mean(),2))

with col3:
    st.metric("Avg Monetary", round(rfm.monetary.mean(),2))

# ========================
# FOOTER
# ========================
st.caption("© Olist Data Analysis Project 2026 - Nalitha Eka Naswadyna")