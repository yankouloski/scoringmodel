import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import shap
import plotly.express as px
from zipfile import ZipFile
from sklearn.cluster import KMeans
plt.style.use('fivethirtyeight')
sns.set_style('darkgrid')
import requests



def load_data():
    z = ZipFile("data/X_default.zip")
    data = pd.read_csv(z.open('X_default.csv'), index_col='SK_ID_CURR', encoding ='utf-8')

    z = ZipFile("data/X_sample.zip")
    sample = pd.read_csv(z.open('X_sample.csv'), index_col='SK_ID_CURR', encoding ='utf-8')
        
    description = pd.read_csv("data/features_description.csv", 
                                  usecols=['Row', 'Description'], index_col=0, encoding= 'unicode_escape')

    target = sample.iloc[:, -1:]

    return data, sample, target, description

def load_age_population():
    data_age = round((data["DAYS_BIRTH"]/365), 2)
    return data_age


def load_income_population():
    df_income = pd.DataFrame(data["AMT_INCOME_TOTAL"])
    df_income = df_income.loc[df_income['AMT_INCOME_TOTAL'] < 200000, :]
    return df_income

def load_model():
    pickle_in = open('model/LGBMClassifier.pkl', 'rb') 
    clf = pickle.load(pickle_in)
    return clf


def load_knn(sample):
    knn = knn_training(sample)
    return knn

def knn_training(sample):
    knn = KMeans(n_clusters=2).fit(sample)
    return knn
     

def identite_client(data, id):
    data_client = data[data.index == int(id)]
    return data_client