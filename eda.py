import streamlit as st  # Streamlit for building web apps
import pandas as pd  # Pandas for handling CSV and DataFrame
import seaborn as sns  # Seaborn for visualizations
import matplotlib.pyplot as plt  # Matplotlib for plotting

# Function to run all EDA (Exploratory Data Analysis) charts and interaction

def run_eda_interface():
    st.subheader("📊 Step 3: Exploratory Data Analysis (EDA)")  # Section title for EDA section

    # Try to load the cleaned data
    try:
        df = pd.read_csv("mubawab_cleaned.csv")  # Load the cleaned CSV file
    except:
        st.warning("⚠️ Please clean the data first.")  # Show warning if file not found
        return  # Exit the function if loading fails

    # Initialize session state toggles for each type of chart if not already present
    if "show_price_dist" not in st.session_state:
        st.session_state.show_price_dist = False  # Control visibility of price distribution chart
    if "show_surface" not in st.session_state:
        st.session_state.show_surface = False  # Control visibility of price vs surface chart
    if "show_rooms" not in st.session_state:
        st.session_state.show_rooms = False  # Control visibility of price vs rooms chart
    if "show_corr" not in st.session_state:
        st.session_state.show_corr = False  # Control visibility of correlation heatmap
    if "show_city_avg" not in st.session_state:
        st.session_state.show_city_avg = False  # Control visibility of average price by city

    # --- Price Distribution Chart ---
    if st.button("📈 Price Distribution"):  # Toggle visibility of price distribution section
        st.session_state.show_price_dist = not st.session_state.show_price_dist

    # Show both histogram and boxplot if toggled
    if st.session_state.show_price_dist:
        col1, col2 = st.columns(2)  # Two columns for two charts

        # Histogram with KDE
        with col1:
            fig1, ax1 = plt.subplots(figsize=(4, 2))  # Create figure with size
            sns.histplot(df["Price"], bins=30, kde=True, ax=ax1)  # Plot price histogram
            ax1.set_title("Distribution of Prices", fontsize=10)  # Set chart title
            ax1.tick_params(labelsize=8)  # Smaller font size for ticks
            st.pyplot(fig1)  # Render chart in Streamlit

        # Boxplot for prices
        with col2:
            fig2, ax2 = plt.subplots(figsize=(4, 2))  # Create figure with size
            sns.boxplot(x=df["Price"], ax=ax2)  # Plot boxplot for price
            ax2.set_title("Boxplot of Prices", fontsize=10)  # Title
            ax2.tick_params(labelsize=8)  # Smaller tick size
            st.pyplot(fig2)  # Show chart

    # --- Price vs Surface Scatterplot ---
    if st.button("📏 Price(M) vs Surface(m²)"):  # Toggle button
        st.session_state.show_surface = not st.session_state.show_surface  # Flip the toggle

    # Show scatterplot if toggled on
    if st.session_state.show_surface:
        col1, col2 = st.columns([1, 1])  # Two columns
        with col1:
            fig, ax = plt.subplots(figsize=(4, 2))  # Create figure
            sns.scatterplot(data=df, x="Surface", y="Price", ax=ax, s=15)  # Scatter: surface vs price
            ax.set_title("Price vs Surface", fontsize=10)  # Title
            ax.tick_params(labelsize=8)  # Smaller ticks
            st.pyplot(fig)  # Display chart

    # --- Price vs Rooms Scatterplot ---
    if st.button("🚪 Price vs Rooms"):  # Toggle visibility
        st.session_state.show_rooms = not st.session_state.show_rooms

    # Show scatterplot if toggled on
    if st.session_state.show_rooms:
        col1, col2 = st.columns([1, 1])  # Two columns
        with col1:
            fig, ax = plt.subplots(figsize=(4, 2))  # Create figure
            sns.scatterplot(data=df, x="Rooms", y="Price", ax=ax, s=15)  # Scatter: rooms vs price
            ax.set_title("Price vs Number of Rooms", fontsize=10)  # Title
            ax.tick_params(labelsize=8)  # Tick settings
            st.pyplot(fig)  # Show chart

    # --- Correlation Heatmap ---
    if st.button("🔗 Correlation Heatmap"):  # Toggle button
        st.session_state.show_corr = not st.session_state.show_corr  # Toggle visibility

    # Show heatmap if toggled on
    if st.session_state.show_corr:
        col1, col2 = st.columns([1, 1])  # Columns
        with col1:
            fig, ax = plt.subplots(figsize=(4, 2.5))  # Create chart
            sns.heatmap(
                df[["Price", "Surface", "Rooms", "Bedrooms", "Bathroom"]].corr(),  # Correlation matrix
                annot=True, cmap="coolwarm", ax=ax  # Show values, use color map
            )
            ax.set_title("Correlation Heatmap", fontsize=10)  # Title
            ax.tick_params(labelsize=8)  # Small ticks
            st.pyplot(fig)  # Display

    # --- Average Price by City Bar Chart ---
    if st.button("🌍 Average Price by City"):  # Toggle view
        st.session_state.show_city_avg = not st.session_state.show_city_avg  # Flip toggle

    # Show chart if toggled
    if st.session_state.show_city_avg:
        df["City"] = df["Location"].apply(lambda x: x.split(",")[-1].strip() if pd.notnull(x) else "Unknown")  # Extract city
        city_avg = df.groupby("City")["Price"].mean().sort_values(ascending=False)  # Compute average price

        col1, col2 = st.columns([1, 1])  # Layout
        with col1:
            fig, ax = plt.subplots(figsize=(4.5, 3))  # Chart figure
            sns.barplot(x=city_avg.values, y=city_avg.index, ax=ax)  # Horizontal bar chart
            ax.set_title("Avg Price by City", fontsize=10)  # Title
            ax.tick_params(labelsize=8)  # Smaller ticks
            st.pyplot(fig)  # Display chart
