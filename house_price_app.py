import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# ==========================================
# 1. DATA GENERATION (Synthetic Dataset)
# ==========================================
@st.cache_data
def load_data():
    np.random.seed(42)
    n_samples = 1000
    
    data = {
        'area': np.random.randint(500, 5000, n_samples),
        'bedrooms': np.random.randint(1, 6, n_samples),
        'bathrooms': np.random.randint(1, 4, n_samples),
        'location': np.random.choice(['Downtown', 'Suburb', 'Rural', 'Airport Area'], n_samples),
        'age': np.random.randint(0, 50, n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Generate Price with some logic (Base price + coefficients + noise)
    # Price = (Area * 150) + (Bed * 10000) + (Bath * 5000) - (Age * 500) + Location_Premium
    location_map = {'Downtown': 50000, 'Suburb': 20000, 'Rural': -10000, 'Airport Area': 5000}
    df['price'] = (df['area'] * 150) + (df['bedrooms'] * 12000) + \
                  (df['bathrooms'] * 7000) - (df['age'] * 800) + \
                  df['location'].map(location_map) + np.random.normal(0, 5000, n_samples)
    
    return df

df = load_data()

# ==========================================
# 2. DATA PREPROCESSING & MODEL BUILDING
# ==========================================
# Features and Target
X = df.drop('price', axis=1)
y = df['price']

# Split Data (80/20)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define Preprocessing for Numeric and Categorical data
numeric_features = ['area', 'bedrooms', 'bathrooms', 'age']
categorical_features = ['location']

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(), categorical_features)
    ])

# Create Pipelines for both models
lr_model = Pipeline(steps=[('preprocessor', preprocessor),
                           ('regressor', LinearRegression())])

dt_model = Pipeline(steps=[('preprocessor', preprocessor),
                           ('regressor', DecisionTreeRegressor(random_state=42))])

# Train Models
lr_model.fit(X_train, y_train)
dt_model.fit(X_train, y_train)

# ==========================================
# 3. STREAMLIT GUI
# ==========================================
st.set_page_config(page_title="House Price Predictor", layout="wide")

st.title("🏡 House Price Prediction System")
st.write("Predicting property values based on location, size, and features.")

# Sidebar for Navigation
menu = st.sidebar.selectbox("Menu", ["Exploratory Data Analysis", "Model Evaluation", "Price Predictor"])

if menu == "Exploratory Data Analysis":
    st.header("📊 Dataset Overview")
    st.write(df.head())
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Price vs Area")
        fig, ax = plt.subplots()
        sns.scatterplot(data=df, x='area', y='price', hue='location', ax=ax)
        st.pyplot(fig)
        
    with col2:
        st.subheader("Price Distribution")
        fig, ax = plt.subplots()
        sns.histplot(df['price'], kde=True, ax=ax, color='green')
        st.pyplot(fig)

elif menu == "Model Evaluation":
    st.header("📈 Model Performance Comparison")
    
    def evaluate(model, X_t, y_t):
        preds = model.predict(X_t)
        return {
            "MAE": mean_absolute_error(y_t, preds),
            "MSE": mean_squared_error(y_t, preds),
            "R2": r2_score(y_t, preds)
        }

    lr_results = evaluate(lr_model, X_test, y_test)
    dt_results = evaluate(dt_model, X_test, y_test)
    
    res_df = pd.DataFrame([lr_results, dt_results], index=["Linear Regression", "Decision Tree"])
    st.table(res_df)
    
    # Visualization: Actual vs Predicted
    lr_preds = lr_model.predict(X_test)
    fig, ax = plt.subplots()
    plt.scatter(y_test, lr_preds, alpha=0.5, color='blue', label='Linear Regression')
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
    plt.xlabel("Actual Prices")
    plt.ylabel("Predicted Prices")
    plt.title("Actual vs Predicted (Linear Regression)")
    st.pyplot(fig)

elif menu == "Price Predictor":
    st.header("🔍 Predict Your House Price")
    
    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        with col1:
            area = st.number_input("Area (sq ft)", min_value=500, max_value=10000, value=1500)
            bedrooms = st.slider("Bedrooms", 1, 6, 3)
            bathrooms = st.slider("Bathrooms", 1, 4, 2)
        with col2:
            location = st.selectbox("Location", df['location'].unique())
            age = st.number_input("Property Age (Years)", 0, 100, 5)
            model_choice = st.radio("Choose Model", ["Linear Regression", "Decision Tree"])
        
        submit = st.form_submit_button("Calculate Price")
    
    if submit:
        # Prepare input data
        input_data = pd.DataFrame([[area, bedrooms, bathrooms, location, age]], 
                                  columns=['area', 'bedrooms', 'bathrooms', 'location', 'age'])
        
        # Predict
        if model_choice == "Linear Regression":
            prediction = lr_model.predict(input_data)[0]
        else:
            prediction = dt_model.predict(input_data)[0]
            
        st.success(f"### Predicted Market Price: ${prediction:,.2f}")
        st.balloons()

# Footer
st.sidebar.info("This project uses Scikit-Learn for ML and Streamlit for the Web Interface.")