# Real Estate Price Prediction

A Python-based project for real estate data collection, exploratory data analysis, and price prediction using Machine Learning.

## Project Overview

This project aims to collect and analyze real estate listings from [Mubawab.ma](https://www.mubawab.ma/) and develop a Machine Learning model capable of estimating property prices based on property characteristics and location.

## Features

- **Web Scraping:** Collect real estate listings using Requests and BeautifulSoup.
- **Data Cleaning:** Handle missing values, clean prices, and extract numerical features using Pandas and Regular Expressions.
- **Exploratory Data Analysis (EDA):** Analyze data distributions, relationships, and correlations using Matplotlib and Seaborn.
- **Machine Learning:** Develop a Linear Regression model using Scikit-learn.
- **Interactive Application:** Build a Streamlit interface for property price estimation.

## Technologies Used

- Python
- Pandas & NumPy
- Requests & BeautifulSoup
- Matplotlib & Seaborn
- Scikit-learn
- Streamlit

## Project Structure

```text
Real-Estate-Price-Prediction/
│
├── scraping.py
├── cleaning.py
├── eda.py
├── modeling.py
├── app.py
├── mubawab_cleaned.csv
├── requirements.txt
└── README.md
```

## Machine Learning Model

The project uses a **Linear Regression** algorithm to estimate property prices based on the following features:

- Surface area
- Number of rooms
- Number of bedrooms
- Number of bathrooms
- City (categorical feature encoded using OneHotEncoder)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/oussamarich/real-estate-price-prediction.git
```

2. Navigate to the project directory:

```bash
cd real-estate-price-prediction
```

3. Install the required dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run the Application

Launch the Streamlit application:

```bash
python -m streamlit run app.py
```

Open the local URL displayed in your terminal:

```text
http://localhost:8501
```

## Author

**Oussama Rich**

GitHub: [@oussamarich](https://github.com/oussamarich)