# app.py
import streamlit as st
import pandas as pd

# Function to load data from CSV file
def load_data():
    # Load data from CSV file
    df = pd.read_csv("water.csv")  # Update the path with your CSV file path
    return df

# Function to predict crop based on input parameters
def predict_crop(pH, Hardness, Solids, Chloramines, Sulfate, Conductivity, Organic_carbon, Trihalomethanes, Potability):
    # Your prediction logic goes here
    # For demonstration, let's just return a default crop
    return "Rice"

def main():
    st.title("Crop Prediction App")
    st.image('water.jpeg')

    # Load data
    df = load_data()

    # Sidebar with input fields
    st.sidebar.header("Input Parameters")
    pH = st.sidebar.number_input("pH", min_value=0.0, max_value=14.0, step=0.1)
    Hardness = st.sidebar.number_input("Hardness")
    Solids = st.sidebar.number_input("Solids")
    Chloramines = st.sidebar.number_input("Chloramines")
    Sulfate = st.sidebar.number_input("Sulfate")
    Conductivity = st.sidebar.number_input("Conductivity")
    Organic_carbon = st.sidebar.number_input("Organic Carbon")
    Trihalomethanes = st.sidebar.number_input("Trihalomethanes")
    Potability = st.sidebar.number_input("Potability")

    # Predict crop
    if st.sidebar.button("Predict"):
        crop = predict_crop(pH, Hardness, Solids, Chloramines, Sulfate, Conductivity, Organic_carbon, Trihalomethanes, Potability)
        st.success(f"Predicted Crop: {crop}")

    # Display data table
    st.header("Data")
    st.write(df)

if __name__ == "__main__":
    main()
