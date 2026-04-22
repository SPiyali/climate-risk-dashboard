import pandas as pd

# Load data
rainfall = pd.read_csv(r"C:\Users\piyal\OneDrive\Desktop\Climate Risk Intelligence System\data_real\rainfall.csv", skiprows=4)

temperature = pd.read_csv(r"C:\Users\piyal\OneDrive\Desktop\Climate Risk Intelligence System\data_real\temperature.csv")

population = pd.read_csv(r"C:\Users\piyal\OneDrive\Desktop\Climate Risk Intelligence System\data_real\population.csv", skiprows=4)


# Show columns
print("Rainfall Columns:", rainfall.columns)
print("Temperature Columns:", temperature.columns)
print("Population Columns:", population.columns)


# Rename columns (World Bank format)
rainfall = rainfall.rename(columns={"Country Name": "Country"})
temperature = temperature.rename(columns={"Country Name": "Country"})
population = population.rename(columns={"Country Name": "Country"})


# Take required columns
temperature = temperature[["Country", "Avg Temperature (°C)"]]

# Convert to numeric
temperature["Avg Temperature (°C)"] = pd.to_numeric(
    temperature["Avg Temperature (°C)"], errors='coerce'
)

# Group by country 
temperature = temperature.groupby("Country").mean().reset_index()

# Rename
temperature.columns = ["Country", "Temperature"]



# NEW (use real available year)

YEAR = "2020"   # safe year

rainfall = rainfall[["Country", YEAR]]
rainfall.columns = ["Country", "Rainfall"]

population = population[["Country", YEAR]]
population.columns = ["Country", "Population"]




# Clean country names

for df in [rainfall, temperature, population]:
    df["Country"] = df["Country"].str.strip().str.lower()

print(set(rainfall["Country"]).intersection(set(temperature["Country"])))


#mapping
mapping = {
    "united states": "usa",
    "russian federation": "russia",
    "united kingdom": "uk",
    "south africa":"south africa",
}


for df in [rainfall, temperature, population]:
    df["Country"] = df["Country"].replace(mapping)



rainfall = rainfall.reset_index(drop=True)
temperature = temperature.reset_index(drop=True)
population = population.reset_index(drop=True)


# Merge datasets
df = rainfall.merge(temperature, on="Country", how="left") \
             .merge(population, on="Country",how="left")


print(df.head())
print("Rows:", len(df))



# REMOVE NON-COUNTRIES 
invalid_keywords = [
    "income", "world", "europe", "asia", "africa",
    "union", "countries", "area", "arab", "caribbean"
]

df = df[~df["Country"].str.contains("|".join(invalid_keywords), na=False, case=False)]


# Drop missing values
df["Temperature"] = df["Temperature"].fillna(df["Temperature"].median())
df["Rainfall"] = df["Rainfall"].fillna(df["Rainfall"].median())
df["Population"] = df["Population"].fillna(df["Population"].median())

df = df[(df["Rainfall"] > 0) & (df["Temperature"] > 0) & (df["Population"] > 0)]



print(df[df["Country"] == "india"])

# Normalize
df["Rainfall"] = df["Rainfall"] / df["Rainfall"].max()
df["Temperature"] = df["Temperature"] / df["Temperature"].max()
df["Population"] = df["Population"] / df["Population"].max()


# Risk Score
df["Risk_Score"] = (
    df["Rainfall"] * 0.5 +
    df["Temperature"] * 0.3 +
    df["Population"] * 0.2
)


print("Total Countries:", len(df))
df = df.sort_values(by="Risk_Score", ascending=False)

# Save final
df.to_csv(r"C:\Users\piyal\OneDrive\Desktop\Climate Risk Intelligence System\data_real\final_risk_data.csv", index=False)

print("✅ DONE! Final dataset created")
print(df.head(30))

print("\nTop 10 High Risk Countries:")
print(df[["Country", "Risk_Score"]].head(10))
























