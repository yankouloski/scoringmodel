import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from flask import Flask, request, jsonify
from flask import render_template, make_response, session, redirect
from flask_restful import Api
#from flask_restful import Ressource, Api
from flask_cors import CORS
import seaborn as sns
import pickle
import shap
import plotly.express as px
from zipfile import ZipFile
from sklearn.cluster import KMeans
plt.style.use('fivethirtyeight')
sns.set_style('darkgrid')
import requests
from functions import load_data,load_model,load_knn,knn_training, identite_client


app = Flask(__name__)
api = Api(app)
CORS(app)    


#Loading data……
data, sample, target, description = load_data()
client_id = sample.index.values
#id_client = sample.index.values vvv
clf = load_model()


#######   Initialisation   #######

@app.route('/', methods=['GET'])
def home():
   return "<h1>Credit Scoring</h1><p>Ce site est le prototype d’une API permettant de calculer la probabilité de défaut des clients d'un établissement de crédit.</p>"

######  Info generales sur l'échantillon   #####

@app.route('/infos_gen')
def load_infos_gen():
    lst_infos = [data.shape[0],round(data["AMT_INCOME_TOTAL"].mean(), 2),round(data["AMT_CREDIT"].mean(), 2)]
    targets = data.TARGET.value_counts()
    nb_credits = lst_infos[0]
    rev_moy = lst_infos[1]
    credits_moy = lst_infos[2]
    prop_default = targets
    return jsonify({"nb_credits":nb_credits, "rev_moy": rev_moy, "credits_moy": credits_moy})

@app.route('/graph_gen')
def load_graph_gen():
    targets = data.TARGET.value_counts()
    # ... création du graphique à partir de targets
    #fig = Figure()
    plt.pie(targets, explode=[0, 0.1], labels=['No default', 'Default'], autopct='%1.1f%%', startangle=90)
    b = BytesIO()
    plt.savefig(b, format="png")
    resp = make_response(b.getvalue())
    resp.headers['content-type'] = 'image/png'
    return resp

###### Information generale sur le client  #####
@app.route('/client_identite')
def get_client_identite():
    client_id = request.args.get('client_id')
    infos_client = data[data.index == int(client_id)]
    print(infos_client.to_dict(orient='records'))
    client_age = round(infos_client["DAYS_BIRTH"].values[0]/365, 2)
    client_statut = infos_client["NAME_FAMILY_STATUS"].values[0]
    client_children = infos_client["CNT_CHILDREN"].values[0] 
    client_gender =infos_client["CODE_GENDER"].values[0]
    client_income =infos_client["AMT_INCOME_TOTAL"].values[0]
    client_credit =infos_client["AMT_CREDIT"].values[0]
    client_annuity =infos_client["AMT_ANNUITY"].values[0]
    client_price =infos_client["AMT_GOODS_PRICE"].values[0]  
#    print(client_age)
#    print(client_statut)
#    print(client_children)
    return jsonify({"age":client_age, "family status":str(client_statut), "nbr children":str(client_children), "Gender":str(client_gender), "income":str(client_income), "credit":str(client_credit), "annuity":str(client_credit), "price":str(client_price)})


#######    Solvabilité du client   #######
@app.route('/predict', methods=['GET', 'POST'])
def load_prediction():
    client_id = request.args.get('client_id')
    X=sample.iloc[:, :-1]
    score = clf.predict_proba(X[X.index == int(client_id)])[:,1]
   #score = clf.predict_proba(X[X.index == int(client_id)])[:,1]
    return jsonify({"Default probability": score[0]})



if __name__ == '__main__': 
    app.run()
                