import streamlit as st  # Streamlit library for building the web interface
import pandas as pd  # pandas for data manipulation
import numpy as np  # numpy for numerical operations
from sklearn.linear_model import LinearRegression  # linear regression model from scikit-learn
from sklearn.preprocessing import OneHotEncoder  # one-hot encoding for categorical data

# Main function to run the modeling interface

def run_modeling_interface():
    # Display section title
    st.subheader("🤖 Step 4: Predict Price with Regression")

    # Try to read the cleaned dataset CSV file
    try:
        df = pd.read_csv("mubawab_cleaned.csv")  # Load cleaned data
    except:
        st.warning("⚠️ Please clean the data first.")  # Show warning if file not found
        return  # Stop function execution

    # Extract the city name from the Location column (after comma)
    df["City"] = df["Location"].apply(lambda x: x.split(",")[-1].strip() if pd.notnull(x) else "Unknown")

    # Remove rows that are missing any of the required fields
    df = df.dropna(subset=["Surface", "Rooms", "Bedrooms", "Bathroom", "Price", "City"])

    # Initialize one-hot encoder (output as dense matrix)
    encoder = OneHotEncoder(sparse_output=False)

    # Apply one-hot encoding to the City column
    city_encoded = encoder.fit_transform(df[["City"]])  # Convert city to binary matrix

    # Get new column names created by the encoder
    city_labels = encoder.get_feature_names_out(["City"])

    # Create the feature matrix X:
    # Combine numeric features with the one-hot encoded city columns
    X = pd.concat([
        df[["Surface", "Rooms", "Bedrooms", "Bathroom"]].reset_index(drop=True),  # reset index to align
        pd.DataFrame(city_encoded, columns=city_labels)  # convert encoded data to DataFrame
    ], axis=1)

    # Create the target array y (price values)
    y = df["Price"].values

    # Create and train the linear regression model using X and y
    model = LinearRegression()
    model.fit(X, y)  # Fit model to the data

    # Display section for user input to make predictions
    st.markdown("### 🧪 Estimate Price")

    # Create two columns for input layout
    col1, col2 = st.columns(2)

    # Get user inputs for numeric features in column 1
    with col1:
        surface = st.number_input("Surface (m²)", min_value=10, max_value=1000, value=100)  # input surface
        rooms = st.slider("Rooms", 1, 10, 3)  # input number of rooms
        bedrooms = st.slider("Bedrooms", 0, 10, 2)  # input number of bedrooms
        bathrooms = st.slider("Bathrooms", 1, 5, 1)  # input number of bathrooms

    # Get city input from dropdown in column 2
    with col2:
        selected_city = st.selectbox("Choose a City", sorted(df["City"].unique()))  # dropdown of city names

    # When user clicks Predict Price button
    if st.button("🔍 Predict Price"):
        # Create a DataFrame for the user input values
        input_base = pd.DataFrame({
            "Surface": [surface],
            "Rooms": [rooms],
            "Bedrooms": [bedrooms],
            "Bathroom": [bathrooms]
        })

        # One-hot encode the selected city from dropdown
        city_row = encoder.transform([[selected_city]])[0]  # encoded city vector

        # Combine numeric inputs with one-hot encoded city
        row = pd.concat([input_base, pd.DataFrame([city_row], columns=city_labels)], axis=1)

        # Use the model to predict the price
        price_pred = model.predict(row)[0]

        # Show the predicted price to the user in a success box
        st.success(f"💰 Estimated price in {selected_city}: {round(price_pred):,} DH")
