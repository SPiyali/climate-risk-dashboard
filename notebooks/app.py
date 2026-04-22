import streamlit as st
import pandas as pd
import plotly.express as px
import time
import os


st.set_page_config(
    page_title="Climate Risk Intelligence",

    page_icon="🌍",
    layout="wide"
)
# with st.spinner("Analyzing global climate data..."):
#     time.sleep(1)


# Load data
df = pd.read_csv("../data_real/final_risk_data.csv")
df_original = df.copy()



# df = pd.read_csv("data_real/final_risk_data.csv")

df["Temperature"] = df["Temperature"].fillna(df["Temperature"].mean())
df["Rainfall"] = df["Rainfall"].fillna(df["Rainfall"].mean())
df["Population"] = df["Population"].fillna(df["Population"].median())



st.title("🌍 Climate Risk Intelligence Dashboard")

# st.title("🌍 Climate Risk Intelligence System (AI Powered)")
st.caption("Real-time Climate Risk Analysis for Global Decision Making")

col1, col2, col3 = st.columns(3)

col1.metric("🌍 Total Countries", len(df))
col2.metric("🔥 Highest Risk", round(df["Risk_Score"].max(), 2))
col3.metric("📉 Avg Risk", round(df["Risk_Score"].mean(), 2))

# Sidebar filter
country = st.sidebar.multiselect(
    "Select Countries",
    options=df["Country"].unique(),
    default=df["Country"].unique()[:10]
)


filtered_df = df[df["Country"].isin(country)]

# st.info("⚠️ This risk score is based on normalized indicators and should be used for comparative analysis only.")

st.markdown("""
<div style="background-color:#E3F2FD; padding:12px; border-radius:10px">
⚠️ <b>Note:</b> This risk score is based on normalized indicators and is intended for comparison only.
</div>
""", unsafe_allow_html=True)


st.markdown("## 🧠 Smart Insights")

# Remove invalid countries
df = df[df["Country"] != "not classified"]
df = df[df["Country"].notna()]

# 1. Highest Risk Country
highest = df.loc[df["Risk_Score"].idxmax()]

# 2. Lowest Risk Country
lowest = df.loc[df["Risk_Score"].idxmin()]

# 3. Average Risk
avg_risk = df["Risk_Score"].mean()

# 4. Correlation
corr_temp = df["Temperature"].corr(df["Risk_Score"])
# corr_temp = df["Temperature"].corr(df)
corr_rain = df["Rainfall"].corr(df["Risk_Score"])

# Display
st.success(f"🔥 Highest Risk Country: {highest['Country']} (Score: {round(highest['Risk_Score'],3)})")

st.info(f"🟢 Lowest Risk Country: {lowest['Country']} (Score: {round(lowest['Risk_Score'],3)})")

st.warning(f"📊 Average Global Risk Score: {round(avg_risk,3)}")

# Correlation Insights
if abs(corr_temp)<0.1:
    st.write("Temperature has a weak impact on risk")

elif corr_temp > 0:
    st.write(f"🌡 Temperature increases risk ({round(corr_temp,2)})")
else:
    st.write(f"🌡 Temperature decreases risk ({round(corr_temp,2)})")


if corr_rain > 0:
    st.write(f"🌧 Rainfall increases climate risk ({round(corr_rain,2)})")
else:
    st.write(f"🌧 Rainfall decreases climate risk ({round(corr_rain,2)})")


st.markdown("---")


# Map
st.subheader("🌍 Global Risk Map")

fig = px.choropleth(
    filtered_df,
    locations="Country",
    locationmode="country names",
    color="Risk_Score",
    color_continuous_scale="Reds"
)

st.plotly_chart(fig)

st.markdown("---")

# Top risky countries
st.subheader("🔥 Top 10 High Risk Countries")

# top10 = df.sort_values(by="Risk_Score", ascending=False).head(10)
# st.dataframe(top10)

st.dataframe(df.sort_values(by="Risk_Score", ascending=False), use_container_width=True)

top_country = df.sort_values(by="Risk_Score", ascending=False).iloc[0]

st.success(f"""
🚨 Highest Risk Country: {top_country['Country']}

Reason:
- High Temperature 🌡️
- High Rainfall 🌧️
- Population Pressure 👥
""")

# Get top row
top_row = df_original.sort_values(by="Risk_Score", ascending=False).iloc[0]

# Extract values
country_name = top_row["Country"]
rainfall = top_row["Rainfall"]
temperature = top_row["Temperature"]
population = top_row["Population"]

# Show insight
st.subheader("🌍 Key Insight")


st.write(f"📌 {country_name} shows highest climate risk based on current dataset.")

st.write("Main Reasons:")

st.write(f"🌧 Rainfall: {round(rainfall)} ")
st.write(f"🌡 Temperature: {round(temperature,4)}")
st.write(f"👥 Population: {round(population,4)}")

st.markdown("---")

# Bar chart
st.subheader("📊 Risk Score Comparison")

fig2 = px.bar(
    filtered_df.sort_values(by="Risk_Score", ascending=False),
    x="Country",
    y="Risk_Score",
    color="Risk_Score",
    color_continuous_scale="Blues"
)

st.plotly_chart(fig2)

st.markdown("---")
st.caption("Developed by Piyali | Climate Analytics Project")