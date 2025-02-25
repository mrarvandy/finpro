import streamlit as st
import pickle
import pandas as pd
from scipy.special import inv_boxcox
from used_car_lists import makers, types, origins, colors, options, fuel_types, gear_types, regions

with open('xgb_model.pkl', 'rb') as f:
    model = pickle.load(f)

def calculator(make, type, year, origin, color, option, engine_size, fuel_type, gear_type, mileage, region):
    data = pd.DataFrame({
        'Make': [make],
        'Type': [type],
        'Year': [year],
        'Origin': [origin],
        'Color': [color],
        'Options': [option],
        'Engine_Size': [engine_size],
        'Fuel_Type': [fuel_type],
        'Gear_Type': [gear_type],
        'Mileage': [mileage],
        'Region': [region]
    })
    
    prediction = model.predict(data)
    return prediction[0]

st.title("Saudi Used Car Price Calculator")

st.write("""
    This app will help you to calculate your desired to-be-sold car.
""")

make = st.selectbox('Make', makers)
type = st.selectbox('Type', types[make])
year = st.slider('Year', 1963, 2025, 2016)
origin = st.selectbox('Origin', origins)
color = st.selectbox('Color', colors)
option = st.selectbox('Options', options)
engine_size = st.number_input('Engine_Size', 1.0, 9.0, 3.0)
fuel_type = st.selectbox('Fuel_Type', fuel_types)
gear_type = st.selectbox('Gear_Type', gear_types)
mileage = st.number_input('Mileage', 100, 20000000, 100000)
region = st.selectbox('Region', regions)

if st.button('Calculate'):
    prediction = calculator(make, type, year, origin, color, option, engine_size, fuel_type, gear_type, mileage, region)
    st.success(f'Best price that you can sell is SAR {round(float(inv_boxcox(prediction, 0.30611)), 2)}')