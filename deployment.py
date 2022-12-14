# -*- coding: utf-8 -*-
"""deployment.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cenZ-akRnY3NiiWZj1f6BxsBowDduIqe
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df=pd.read_csv("clean_data.csv")
df.head()

df.isna().sum()

Data=df.copy()

Data.head()

Data.describe()

Data["location"].value_counts()

Data["location"]=Data["location"].apply(lambda x: x.strip())
location_counts=Data["location"].value_counts()

location_counts

location_10_counts=location_counts[location_counts<=10]
location_10_counts

Data["location"]=Data["location"].apply(lambda x: "other" if x in location_10_counts else x)

Data["location"].value_counts()

Data["price_per_sqft"]=(Data["price"]/Data["total_sqft"])*100000

Data["price_per_sqft"].describe()

def sqft_outlier_removal(df):
    op_df=pd.DataFrame()
    for location,subdf in df.groupby("location"):
        m=np.mean(subdf.price_per_sqft)
        sd=np.std(subdf.price_per_sqft)
        
        gen_df=subdf[(subdf.price_per_sqft>(m-sd)) & (subdf.price_per_sqft<=(m+sd))]
        op_df=pd.concat([op_df,gen_df], ignore_index=True)
    return op_df
Data=sqft_outlier_removal(Data)
Data.describe()

Data

from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()



Data['location'] = le.fit_transform(Data['location'].values)

Data.drop("price_per_sqft",axis=1,inplace=True)

Data.to_csv("Clean1_data.csv",index=False)

x=Data.drop("price",axis=1)

y=Data["price"]

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression,Lasso,Ridge
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.metrics import r2_score

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.10,random_state=16)

x_train.shape,y_train.shape,x_test.shape,y_test.shape

"""# Linear Regression"""

model = LinearRegression()

"""model.fit(x_train,y_train)"""

model.fit(x_train,y_train)

y_pred = model.predict(x_test)

y_pred

x_test.info()

pred = model.predict([[0,1200,2,0,1,0,1,0]])
print(pred)

print('Traning accuracy :',model.score(x_train,y_train))
print('Test accuracy :',model.score(x_test,y_test))

"""# lasso"""

lasso = Lasso()

lasso.fit(x_train,y_train)

y_pred = lasso.predict(x_test)

y_pred

print('Traning accuracy :',lasso.score(x_train,y_train))
print('Test accuracy :',lasso.score(x_test,y_test))

pred = lasso.predict([[0,1200,2,0,1,0,1,0]])
print(pred)

import xgboost as xgb
xgb1 = xgb.XGBRegressor()

xgb1.fit(x_train,y_train)
xgb_pred = xgb1.predict(x_test)

xgb1.save_model("lasso.json")

import streamlit as  st

st.header("House price prediction")

np.save('classes.npy',le.classes_)

le.classes_ = np.load('classes.npy',allow_pickle = True)

xgb_best = xgb.XGBRegressor()

xgb_best.load_model("lasso.json")

if st.checkbox('Show Training Dataframe'):
    Data

st.subheader("please select relevant features of house")
left_column, right_column = st.columns(2)
with left_column:
    inp_species = st.radio('Location: ',np.unique(df['location']))

Data.head()

Data.info()

input_sqft = st.slider('Total sqft(sqft)',0,max(Data["total_sqft"]))
input_bed = st.slider('No.of bedrooms',0,max(Data["No. of Bedrooms"]))
input_school = st.slider('school availabl',0,1)
input_security = st.slider('24X7Security',0,1)
input_car = st.slider('Car',0,1)
input_hospital = st.slider('hospital',0,1)
input_lift = st.slider('lift',0,1)

if st.button('Make Prediction'):
    input_loc = le.transform(np.expand_dims(inp_species,-1))
    inputs = np.expand_dims(
                            [int(input_species),input_sqft,input_bed,input_school,input_security,input_car,input_hospital,input_lift])
    prediction = xbg_best.predict(inputs)
    print("final pred :",np.squeeze(prediction,-1))
    st.write(f"your house price: {np.squeeze(prediction, -1):.2f}g")

