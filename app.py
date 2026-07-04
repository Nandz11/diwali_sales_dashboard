import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Diwali Sales Dashboard", page_icon="🪔", layout="wide")

# Custom CSS
st.markdown("""
<style>
.main { background-color: #0e1117; }
.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px; border-radius: 15px; text-align: center; color: white;
}
</style>
""", unsafe_allow_html=True)

# Load data
df = pd.read_csv(r'C:\Users\91744\OneDrive\Desktop\Diwali_sales\Diwali Sales Data.csv', encoding='latin1')
df.drop(columns=['Status', 'unnamed1'], inplace=True)
df.dropna(subset=['Amount'], inplace=True)

# Header
st.title("🪔 Diwali Sales Dashboard")
st.markdown("### Who buys what during Diwali?")
st.markdown("---")

# Sidebar filters
st.sidebar.header("🔍 Filters")
gender = st.sidebar.multiselect("Gender", df['Gender'].unique(), default=df['Gender'].unique())
age = st.sidebar.multiselect("Age Group", df['Age Group'].unique(), default=df['Age Group'].unique())
zone = st.sidebar.multiselect("Zone", df['Zone'].unique(), default=df['Zone'].unique())

filtered = df[(df['Gender'].isin(gender)) & (df['Age Group'].isin(age)) & (df['Zone'].isin(zone))]

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Total Revenue", f"₹{filtered['Amount'].sum()/1e6:.1f}M")
col2.metric("👥 Total Customers", f"{filtered['User_ID'].nunique():,}")
col3.metric("📦 Total Orders", f"{filtered['Orders'].sum():,}")
col4.metric("💳 Avg Spend/Customer", f"₹{filtered['Amount'].mean():,.0f}")

st.markdown("---")

# Row 1
col1, col2 = st.columns(2)
with col1:
    fig1 = px.bar(filtered.groupby('Gender')['Amount'].sum().reset_index(),
                  x='Gender', y='Amount', color='Gender',
                  title='💜 Sales by Gender',
                  color_discrete_map={'F': '#764ba2', 'M': '#667eea'},
                  template='plotly_dark')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.bar(filtered.groupby('Age Group')['Amount'].sum().reset_index().sort_values('Amount', ascending=False),
                  x='Age Group', y='Amount',
                  title='📊 Sales by Age Group',
                  color='Amount', color_continuous_scale='Purples',
                  template='plotly_dark')
    st.plotly_chart(fig2, use_container_width=True)

# Row 2
col1, col2 = st.columns(2)
with col1:
    fig3 = px.bar(filtered.groupby('State')['Amount'].sum().reset_index().sort_values('Amount', ascending=False).head(10),
                  x='Amount', y='State', orientation='h',
                  title='🗺️ Top 10 States by Sales',
                  color='Amount', color_continuous_scale='Viridis',
                  template='plotly_dark')
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    fig4 = px.pie(filtered.groupby('Product_Category')['Amount'].sum().reset_index(),
                  values='Amount', names='Product_Category',
                  title='🛍️ Sales by Product Category',
                  template='plotly_dark', hole=0.4)
    st.plotly_chart(fig4, use_container_width=True)

# Row 3
fig5 = px.bar(filtered.groupby('Occupation')['Amount'].sum().reset_index().sort_values('Amount', ascending=False),
              x='Occupation', y='Amount',
              title='💼 Sales by Occupation',
              color='Amount', color_continuous_scale='Plasma',
              template='plotly_dark')
st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")
st.markdown("**Key Insight:** Women aged 26-35 working in Healthcare & IT are the biggest Diwali shoppers! 🪔")

