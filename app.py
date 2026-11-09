import streamlit as st  # Streamlit for creating the web interface
import pandas as pd  # Pandas for data handling
import os  # OS module for checking file existence
import base64  # For encoding the background image

# Import custom modules for scraping, cleaning, visualization, and prediction
from scraping import scrape_ads  # Import scraping function
from cleaning import clean_data  # Import cleaning function
from eda import run_eda_interface  # Import EDA interface function
from modeling import run_modeling_interface  # Import modeling interface function

# Function to set background image
def set_background(image_file):
    with open(image_file, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()  # Encode image to base64
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

st.markdown("""
<style>
/* Expander header (opened) */
details[open] > summary {
    border: 2px solid #004466;
    border-radius: 10px;
    padding: 10px;
    font-weight: bold;
    background-color: #e0f2f1;
    color: #003344;
    transition: all 0.3s ease;
}

/* Expander header (closed) */
details > summary {
    border: 2px solid #004466;
    border-radius: 10px;
    padding: 10px;
    background-color: #f0fdfc;
    color: #004455;
    font-weight: bold;
    transition: all 0.3s ease;
}

/* Expander content box */
details[open] > div {
    border: 2px solid #cfd8dc;
    border-radius: 10px;
    padding: 1.5rem;
    background-color: #ffffffcc;  /* Slightly transparent white */
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)


# --- Initialize Streamlit session state (first run setup) ---
if "data" not in st.session_state:
    st.session_state.data = None  # Initialize data container in session state

if "show_scraped" not in st.session_state:
    st.session_state.show_scraped = False  # Flag to show/hide scraped data section

if "show_cleaned" not in st.session_state:
    st.session_state.show_cleaned = False  # Flag to show/hide cleaned data section

# Set Streamlit app layout and page title
st.set_page_config(page_title="Housing Data Scraper", layout="wide")

set_background("bk.jpg")  # Make sure 'bk.png' is in the same folder as app.py

# Display main app title and instructions
st.title("🏨📡 Housing Data Scraper")  # Page title
st.markdown("""
This tool allows you to:
- Scrape apartment listings from **Mubawab**
- Clean and prepare the data
- Visualize or export for modeling
""")  # Description of app features

# --- Step 1: Scrape Section ---
with st.expander("🔍 Step 1: Scrape Ads", expanded=False):  # Expandable panel for scraping step
    col1, col2 = st.columns([2, 1])  # Split layout into two columns

    with col1:  # Left column for scraping input and trigger
        ads_to_scrape = st.number_input(
            "How many ads to scrape?",  # Input label for number of ads
            min_value=10,  # Minimum allowed value
            max_value=500,  # Maximum allowed value
            value=200,  # Default value
            step=10  # Increment step
        )

        # Button to trigger scraping action
        if st.button("Scrape Ads"):
            st.info(f"Scraping {ads_to_scrape} ads...")  # Show scraping status
            df = scrape_ads(max_ads=ads_to_scrape)  # Run scraping function
            df.to_csv("Scraped_data_ads.csv", index=False, encoding="utf-8")  # Save scraped data to CSV
            st.session_state.data = df  # Store result in session state
            st.success(f"✅ Scraping complete! {len(df)} ads saved.")  # Notify user

    with col2:  # Right column for toggling scraped data preview
        if st.button("👁️ Show Scraped"):  # Button to show scraped data
            st.session_state.show_scraped = True
        if st.button("👁️ Hide Scraped"):  # Button to hide scraped data
            st.session_state.show_scraped = False

    # Display scraped data if toggled on and file exists
    if st.session_state.show_scraped and os.path.exists("Scraped_data_ads.csv"):
        scraped_df = pd.read_csv("Scraped_data_ads.csv")  # Load scraped data from CSV
        st.subheader("📄 Scraped Data Preview")  # Section subtitle
        st.write(f"Total ads scraped: {len(scraped_df)}")  # Display row count
        st.dataframe(scraped_df, use_container_width=True, height=600)  # Show full table

# --- Step 2: Clean Section ---
with st.expander("🧼 Step 2: Clean Data", expanded=False):  # Expandable panel for cleaning step
    col1, col2 = st.columns([2, 1])  # Two-column layout again

    with col1:  # Column for cleaning logic
        if st.button("Clean Data"):  # Button to start cleaning process
            if st.session_state.data is None:  # If no data in memory, try loading from file
                try:
                    df = pd.read_csv("Scraped_data_ads.csv")  # Attempt to load scraped file
                except:
                    st.error("No scraped data found.")  # Show error if file missing
                    st.stop()  # Stop further execution
            else:
                df = st.session_state.data  # Use in-memory data if available

            df = clean_data(df)  # Call cleaning function
            df.to_csv("mubawab_cleaned.csv", index=False, encoding="utf-8")  # Save cleaned data
            st.session_state.data = df  # Update session state
            st.success("✅ Data cleaned and saved as 'mubawab_cleaned.csv'")  # Notify user

    with col2:  # Column for toggling cleaned data preview
        if st.button("👁️ Show Cleaned"):  # Button to show cleaned data
            st.session_state.show_cleaned = True
        if st.button("👁️ Hide Cleaned"):  # Button to hide cleaned data
            st.session_state.show_cleaned = False

    # Display cleaned data preview if toggled and file exists
    if st.session_state.show_cleaned and os.path.exists("mubawab_cleaned.csv"):
        cleaned_df = pd.read_csv("mubawab_cleaned.csv")  # Load cleaned data
        st.subheader("📄 Cleaned Data Preview")  # Section subtitle
        st.write("Price(DH), Surface(m²)")  
        st.write(f"Total ads cleaned: {len(cleaned_df)}")  # Row count
        st.dataframe(cleaned_df, use_container_width=True, height=600)  # Display dataframe

# --- Step 3: EDA (Exploratory Data Analysis) ---
with st.expander("📊 Step 3: EDA", expanded=False):  # Expandable panel for visualizations
    run_eda_interface()  # Call EDA module to display visual charts and stats

# --- Step 4: Modeling (Prediction) ---
with st.expander("🤖 Step 4: Modeling", expanded=False):  # Expandable panel for ML model
    run_modeling_interface()  # Call modeling interface for prediction input
