"""
Enables the automation of multiple autotrader searches.

Based on the autotrader-scraper package:
https://github.com/suhailidrees/autotrader_scraper
"""

from autotrader_scraper import get_cars
import pandas as pd

criteria = {
    "postcode": "SW1A 0AA", 
    "min_year": 2008,
    "max_year": 2014,
    "radius": 40,
    "min_price": 2000,
    "max_price": 6000,
    "fuel": "Petrol",
    "transmission": "Manual",
    "max_mileage": 100000,
    "max_attempts_per_page": 3,
    "verbose": False
}

civic = get_cars(
    make = "Honda",
    model = "Civic",
    postcode = criteria["postcode"],
    radius = criteria["radius"],
    min_year = criteria["min_year"],
    max_year = criteria["max_year"],
    include_writeoff = "exclude",
    max_attempts_per_page = criteria["max_attempts_per_page"],
    verbose = criteria["verbose"]
)

print("Civic search done.")

jazz = get_cars(
    make = "Honda",
    model = "Jazz",
    postcode=criteria["postcode"],
    radius = criteria["radius"],
    min_year = criteria["min_year"],
    max_year = criteria["max_year"],
    include_writeoff = "exclude",
    max_attempts_per_page = criteria["max_attempts_per_page"],
    verbose = criteria["verbose"]
)

print("Jazz search done.")

auris = get_cars(
    make = "Toyota",
    model = "Auris",
    postcode=criteria["postcode"],
    radius = criteria["radius"],
    min_year = criteria["min_year"],
    max_year = criteria["max_year"],
    include_writeoff = "exclude",
    max_attempts_per_page = criteria["max_attempts_per_page"],
    verbose = criteria["verbose"]
)

print("Auris search done.")

corolla = get_cars(
    make = "Toyota",
    model = "Corolla",
    postcode=criteria["postcode"],
    radius = criteria["radius"],
    min_year = 2000,
    max_year = criteria["max_year"],
    include_writeoff = "exclude",
    max_attempts_per_page = criteria["max_attempts_per_page"],
    verbose = criteria["verbose"]
)

print("Corolla search done.")

yaris = get_cars(
    make = "Toyota",
    model = "Yaris",
    postcode=criteria["postcode"],
    radius = criteria["radius"],
    min_year = criteria["min_year"],
    max_year = criteria["max_year"],
    include_writeoff = "exclude",
    max_attempts_per_page = criteria["max_attempts_per_page"],
    verbose = criteria["verbose"]
)

print("Yaris search done.")

mazda3 = get_cars(
    make="Mazda",
    model="Mazda3",
    postcode=criteria["postcode"],
    radius=criteria["radius"],
    min_year=criteria["min_year"],
    max_year=criteria["max_year"],
    include_writeoff="exclude",
    max_attempts_per_page=criteria["max_attempts_per_page"],
    verbose=criteria["verbose"]
)

print("Mazda3 search done.")

swift = get_cars(
    make="Suzuki",
    model="Swift",
    postcode=criteria["postcode"],
    radius=criteria["radius"],
    min_year=criteria["min_year"],
    max_year=criteria["max_year"],
    include_writeoff="exclude",
    max_attempts_per_page=criteria["max_attempts_per_page"],
    verbose=criteria["verbose"]
)

print("Swift search done.")

results = (
    civic + 
    jazz +
    auris + 
    corolla +
    yaris + 
    mazda3 + 
    swift
)

print(f"Found {len(results)} total results.")

df = pd.DataFrame.from_records(results)

df["price"] = df["price"] \
    .str.replace("£", "") \
    .str.replace(",", "") \
    .astype(int)

df["distance"] = df["seller"].str.extract(r'(\d+ mile)', expand=False)
df["distance"] = df["distance"].str.replace(" mile", "")
df["distance"] = pd.to_numeric(df["distance"], errors="coerce").astype("Int64")

df["year"] = df["year"].str.replace(r"\s(\(\d\d reg\))", "", regex=True)
df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")

shortlist = df[
  (df["price"] >= criteria["min_price"]) & 
  (df["price"] <= criteria["max_price"]) &
  (df["fuel"] == criteria["fuel"]) &
  (df["mileage"] <= criteria["max_mileage"]) &
  (df["transmission"] == criteria["transmission"]) &
  (df["engine"] != "1.0L") &
  (df["engine"] != "1.2L")
]

print(f"{len(shortlist)} cars met the criteria. Saving to 'autotrader-shortlist.csv'")

shortlist = shortlist.sort_values(by="distance")
shortlist.to_csv("autotrader-shortlist.csv")