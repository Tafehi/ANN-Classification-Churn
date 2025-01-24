import streamlit as st
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
import pickle

model = tf.keras.models.load_model('model.h5')



## load the encoder and scaler
with open('one_hot_encoder_geo.pkl','rb') as file:
    onehot_encode_geo=pickle.load(file)

with open('label_encoder_gender.pkl', 'rb') as file:
    label_encoder_gender = pickle.load(file)

with open('scaler.pkl', 'rb') as file:
    scaler = pickle.load(file)



## Streamlit code
st.title('Customer Churn Prediction')
st.write('This is a simple Customer Churn Prediction App')

geography = st.selectbox('Geography', onehot_encode_geo.categories_[0])
gender = st.selectbox('Gender', label_encoder_gender.classes_)
age = st.slider('Age', 18, 100)
balance = st.number_input('Balance')
credit_score = st.number_input('Credit Score')
estimated_salary = st.number_input('Estimated Salary')
tenure = st.slider('Tenure', 0,10)
num_of_products = st.slider('Number of Products', 1,4)
has_cr_card = st.selectbox('Has Credit Card', [0,1])
is_active_member = st.selectbox('Is Active Member', [0,1])

input_data = {
    'CreditScore': credit_score,
    'Geography': geography,
    'Gender': gender,
    'Age': age,
    'Tenure': tenure,
    'Balance': balance,
    'NumOfProducts': num_of_products,
    'HasCrCard': has_cr_card,
    'IsActiveMember': is_active_member,
    'EstimatedSalary': estimated_salary
}

# One-hot encode 'Geography'
geo_encoded = onehot_encode_geo.transform([[input_data['Geography']]]).toarray()
geo_encoded_df = pd.DataFrame(geo_encoded, columns=onehot_encode_geo.get_feature_names_out(['Geography']))

# Display the updated DataFrame
input_df=pd.DataFrame([input_data])

## Encode categorical variables
input_df['Gender']=label_encoder_gender.transform(input_df['Gender'])

## concatination one hot encoded 
input_df=pd.concat([input_df.drop("Geography",axis=1),geo_encoded_df],axis=1)

## Appy scaling
input_scaled=scaler.transform(input_df)

## Predict the input data

prediction=model.predict(input_scaled)
prediction_proba = prediction[0][0]

if prediction_proba > 0.5:
    st.write(f'Churn Probability is: {prediction_proba}')
    st.write('The customer is likely to churn.')
else:
    st.write(f'Churn Probability is: {prediction_proba}')
    st.write(f'The customer is not likely to churn.')