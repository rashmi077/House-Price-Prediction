import streamlit as st
import pandas as pd
import statsmodels.api as sm
from joblib import load
import json
import os

st.title("🏠 Housing Price Predictor")
st.write("Enter the values of features to predict housing price:")

# 1️⃣ Load model and columns
model_path = "ols_model_joblib.pkl"
columns_path = "model_columns.json"

if not os.path.exists(model_path) or not os.path.exists(columns_path):
    st.error("❌ Model or columns file not found.")
else:
    model = load(model_path)
    with open(columns_path, "r") as f:
        model_columns = json.load(f)

    # 2️⃣ Input fields
    input_data = {}

    # Yes/No columns
    yes_no_cols = ['mainroad','guestroom','basement','hotwaterheating','airconditioning','prefarea']
    col1, col2 = st.columns(2)
    for idx, col in enumerate(yes_no_cols):
        choice = (col1 if idx % 2 == 0 else col2).selectbox(f"{col.replace('_',' ').title()}", ["No","Yes"])
        input_data[col] = 1 if choice=="Yes" else 0

    # Numeric columns
    st.subheader("House Specifications")
    input_data['area'] = st.slider("Area (sq ft)", 100, 10000, 500, 100)
    input_data['bedrooms'] = st.slider("Bedrooms", 1, 10, 2)
    input_data['bathrooms'] = st.slider("Bathrooms", 1, 10, 2)
    input_data['stories'] = st.slider("Stories", 1, 10, 1)

    # Furnishing status
    st.subheader("Furnishing Status")
    furnishing = st.selectbox("Furnishing Status", ["Unfurnished","Semi-Furnished","Furnished"])
    # Use exact dummy column names as in model_columns
    input_data['furnishingstatus_semi_furnished'] = 1 if furnishing=="Semi-Furnished" else 0
    input_data['furnishingstatus_furnished'] = 1 if furnishing=="Furnished" else 0

    # 3️⃣ Ensure all model columns exist
    # Remove constant if model_columns already has 'const'
    if 'const' in model_columns:
        input_data['const'] = 1  # Add intercept
    for col in model_columns:
        if col not in input_data:
            input_data[col] = 0

    # 4️⃣ Predict
    if st.button("Predict Price"):
        input_df = pd.DataFrame([input_data])
        # Reorder columns exactly as model_columns
        input_df = input_df[model_columns]
        prediction = model.predict(input_df)[0]
        st.success(f"💰 Predicted House Price: ₹ {prediction:,.2f}")

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: right; color: lightblue;'>Created by Rashmi</p>", unsafe_allow_html=True)
