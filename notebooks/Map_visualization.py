import pandas as pd

import plotly.express as px

#Load final datset
df = pd.read_csv("C:/Users/piyal/OneDrive/Desktop/Climate Risk Intelligence System/data_real/final_risk_data.csv")


fig = px.choropleth(
    df,
    locations="ISO_Code",
    locationmode="country names",
    color="Risk_Score",
    color_continuous_scale="Reds",
hover_name="Country",
    hover_data={
        "Rainfall": True,
        "Temperature": True,
        "Population": True,
        "Risk_Score": True
    },
    title="🌍 Global Climate Risk Map"
)


fig.update_layout(
    title_x=0.5,
    geo=dict(showframe=False, showcoastlines=True)
)

fig.show()