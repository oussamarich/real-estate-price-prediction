import pandas as pd  # Pandas for working with dataframes
import re  # Regular expressions for cleaning text

def clean_data(df):  # Function to clean a DataFrame
    # Strip extra whitespace and newlines from string fields
    df = df.applymap(lambda x: re.sub(r"\s+", " ", str(x)).strip() if isinstance(x, str) else x)

    # Remove rows where important fields are missing
    df = df.dropna(subset=["Price", "Location", "Surface", "Rooms", "Bedrooms", "Bathroom"])

    # --- Clean the Price column ---
    def clean_price(p):
        if "EUR" in p:  # Skip prices in EUR
            return None
        p = re.sub(r"[^\d]", "", p)  # Remove all non-digit characters
        return int(p) if p else None  # Convert to integer if not empty

    df["Price"] = df["Price"].apply(clean_price)  # Apply cleaning to Price column

    # --- Clean the Surface column ---
    df["Surface"] = df["Surface"].apply(lambda x: int(re.sub(r"[^\d]", "", str(x))) if pd.notnull(x) else None)

    # --- Extract numbers from text for Rooms, Bedrooms, and Bathroom ---
    def extract_number(text):
        match = re.search(r"\d+(\.\d+)?", str(text))  # Look for a number in the text
        return float(match.group()) if match else None  # Return the number found

    df["Rooms"] = df["Rooms"].apply(extract_number)  # Clean Rooms column
    df["Bedrooms"] = df["Bedrooms"].apply(extract_number)  # Clean Bedrooms column
    df["Bathroom"] = df["Bathroom"].apply(extract_number)  # Clean Bathroom column

    # Drop rows again if any of the cleaned values are missing
    df = df.dropna(subset=["Price", "Surface", "Rooms", "Bedrooms", "Bathroom"]).reset_index(drop=True)

    # Replace the Title column with simple default titles like "Ad 1", "Ad 2", etc.
    df["Title"] = [f"Ad {i+1}" for i in range(len(df))]

    return df  # Return the cleaned DataFrame
