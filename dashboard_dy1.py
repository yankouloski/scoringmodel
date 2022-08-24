import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import shap
import json
import plotly.express as px
from zipfile import ZipFile
from sklearn.cluster import KMeans
plt.style.use('fivethirtyeight')
sns.set_style('darkgrid')
import requests
import sys
sys.path.append("..")
from functions import load_data, load_age_population, load_income_population, load_knn,knn_training, identite_client, load_model




def main() :
    #Loading data……
    data, sample, target, description = load_data()
#    data_age = load_age_population(data)
#    df_income = load_income_population()

    #######################################
    # SIDEBAR
    #######################################

    #Title display
    html_temp = """
    <div style="background-color: tomato; padding:10px; border-radius:10px">
    <h1 style="color: white; text-align:center">Dashboard Scoring Credit</h1>
    </div>
    <p style="font-size: 20px; font-weight: bold; text-align:center">Credit decision support…</p>
    """
    st.markdown(html_temp, unsafe_allow_html=True)

    #Customer ID selection
    st.sidebar.header("**General Info**")

    #Loading selectbox
    client_id = sample.index.values
    chk_id = st.sidebar.selectbox("Client ID", client_id)

    #Loading general info
#    nb_credits, rev_moy, credits_moy, targets = load_infos_gen(data)

    response =json.loads(requests.get("https://flask-heroku-app-dy2.herokuapp.com//infos_gen").content)
#    print(response)
#    response =json.loads(requests.get("/infos_gen").content)
    nb_credits=response["nb_credits"]
    credits_moy=response["credits_moy"]
    rev_moy=response["rev_moy"]
        
    ### Display of information in the sidebar ###
    #Number of loans in the sample
    st.sidebar.markdown("<u>Number of loans in the sample :</u>", unsafe_allow_html=True)
    st.sidebar.text(nb_credits)

    #Average income
    st.sidebar.markdown("<u>Average income (USD) :</u>", unsafe_allow_html=True)
    st.sidebar.text(rev_moy)

    #AMT CREDIT
    st.sidebar.markdown("<u>Average loan amount (USD) :</u>", unsafe_allow_html=True)
    st.sidebar.text(credits_moy)
    
    #PieChart
    targets = data.TARGET.value_counts()
    st.sidebar.markdown("<u>......</u>", unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(5,5))
    plt.pie(targets, explode=[0, 0.1], labels=['No default', 'Default'], autopct='%1.1f%%', startangle=90)
    st.sidebar.pyplot(fig)

#    response =json.loads(requests.get("http://127.0.0.1:1080/graph_gen").content)

    #######################################
    # HOME PAGE - MAIN CONTENT
    #######################################
    #Display Customer ID from Sidebar
    st.write("Customer ID selection :", chk_id)


    #Customer information display : Customer Gender, Age, Family status, Children, …
    st.header("**Customer information display**")
    
############"   
    if st.checkbox("Show customer information ?"): 
        response =json.loads(requests.get("https://flask-heroku-app-dy2.herokuapp.com/client_identite?client_id={}".format(chk_id)).content)  
        Gender=response["Gender"]
        age=response["age"]
        family_status=response["family status"] 
        nbr_children=response["nbr children"]
        income=response["income"]
        annuity=response["annuity"]
        price=response["price"]
        credit=response["credit"]

#client_id=100014

        #print(infos_client["CODE_GENDER"].values)
        st.write("Gender : ", Gender)
        #print(infos_client.columns)
        st.write("Age :", age)
        st.write("Family status :", family_status)
        st.write("Number of children :", nbr_children)
        

        #Age distribution plot
#        data_age = load_age_population(data)
        data_age = round((data["DAYS_BIRTH"]/365), 2)
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.histplot(data_age, edgecolor = 'k', color="goldenrod", bins=20)
        ax.axvline(int(age), color="green", linestyle='--')
        ax.set(title='Customer age', xlabel='Age(Year)', ylabel='')
        st.pyplot(fig)
    
#        st.write("**Income total : **{:.0f}".format(infos_client["AMT_INCOME_TOTAL"].values[0]))
        
        st.subheader("*Income (USD)*")
        st.write("Income total :",income)
        st.write("Credit amount :",credit)
        st.write("Credit annuities :", annuity)
        st.write("Amount of property for credit :",price)
        
        #Income distribution plot
#        data_income = load_income_population(data)
        data_income = pd.DataFrame(data["AMT_INCOME_TOTAL"])
        data_income = data_income.loc[data_income['AMT_INCOME_TOTAL'] < 200000, :]
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.histplot(data_income["AMT_INCOME_TOTAL"], edgecolor = 'k', color="goldenrod", bins=10)
        ax.axvline(income, color="green", linestyle='--')
        ax.set(title='Customer income', xlabel='Income (USD)', ylabel='')
        st.pyplot(fig)
        
        #Relationship Age / Income Total interactive plot 
        data_sk = data.reset_index(drop=False)
        data_sk.DAYS_BIRTH = (data_sk['DAYS_BIRTH']/365).round(1)
        fig, ax = plt.subplots(figsize=(10, 10))
        fig = px.scatter(data_sk, x='DAYS_BIRTH', y="AMT_INCOME_TOTAL", 
                         size="AMT_INCOME_TOTAL", color='CODE_GENDER',
                         hover_data=['NAME_FAMILY_STATUS', 'CNT_CHILDREN', 'NAME_CONTRACT_TYPE', 'SK_ID_CURR'])

        fig.update_layout({'plot_bgcolor':'#f0f0f0'}, 
                          title={'text':"Relationship Age / Income Total", 'x':0.5, 'xanchor': 'center'}, 
                          title_font=dict(size=20, family='Verdana'), legend=dict(y=1.1, orientation='h'))


        fig.update_traces(marker=dict(line=dict(width=0.5, color='#3a352a')), selector=dict(mode='markers'))
        fig.update_xaxes(showline=True, linewidth=2, linecolor='#f0f0f0', gridcolor='#cbcbcb',
                         title="Age", title_font=dict(size=18, family='Verdana'))
        fig.update_yaxes(showline=True, linewidth=2, linecolor='#f0f0f0', gridcolor='#cbcbcb',
                         title="Income Total", title_font=dict(size=18, family='Verdana'))

        st.plotly_chart(fig)
    
    else:
        st.markdown("<i>…</i>", unsafe_allow_html=True)

########### Customer solvability display
    st.header("**Customer file analysis**")
#    prediction = load_prediction(sample, chk_id, clf)
    response = json.loads(requests.get("https://flask-heroku-app-dy2.herokuapp.com/predict?client_id={}".format(chk_id)).content)
    prediction=response["Default probability"]
    st.write("**Default probability** : {:.0f} %".format(round(float(prediction)*100, 2)))


########Compute decision according to the best threshold
    if prediction <= 0.5 :
        decision = "<font color='green'>**LOAN GRANTED**</font>" 
    else:
        decision = "<font color='red'>**LOAN REJECTED**</font>"

    st.write("**Decision** *(with threshold 50%)* :", decision, unsafe_allow_html=True)
    

#################### Customer data
    st.markdown("<u>Customer Data :</u>", unsafe_allow_html=True)
#    st.write(identite_client(data, chk_id))
    infos_client = data[data.index == chk_id]
    st.write(infos_client)

    
#        X = X[X.index == chk_id]
#    infos_client = data[data.index == chk_id]
#   response =json.loads(requests.get("http://127.0.0.1:1080/client_identite?client_id=", chk_id).content)
    #response = json.loads(requests.get("http://127.0.0.1:1080/client_identite?client_id={}".format(chk_id)).content)
    #st.write(response)
    #    st.write(identite_client(data, chk_id))
   
    
############### Feature importance / description
    if st.checkbox("Customer ID {:.0f} feature importance ?".format(chk_id)):
        shap.initjs()
        X = sample.iloc[:, :-1]
        X = X[X.index == chk_id]
        number = st.slider("Pick a number of features…", 0, 20, 5)

        fig, ax = plt.subplots(figsize=(10, 10))
        explainer = shap.TreeExplainer(load_model())
        shap_values = explainer.shap_values(X)
        shap.summary_plot(shap_values[0], X, plot_type ="bar", max_display=number, color_bar=False, plot_size=(5, 5))
        st.pyplot(fig)
        
        if st.checkbox("Need help about feature description ?") :
            list_features = description.index.to_list()
            feature = st.selectbox('Feature checklist…', list_features)
            st.table(description.loc[description.index == feature][:1])
        
    else:
        st.markdown("<i>…</i>", unsafe_allow_html=True)
            
    

    #Similar customer files display
    chk_voisins = st.checkbox("Show similar customer files ?")

    if chk_voisins:
#        knn = load_knn()
        st.markdown("<u>List of the 10 files closest to this Customer :</u>", unsafe_allow_html=True)
        index = sample[sample.index == chk_id].index.values
        index = index[0]
        data_client = pd.DataFrame(sample.loc[sample.index, :])
        knn = KMeans(n_clusters=2).fit(sample)
        df_neighbors = pd.DataFrame(knn.fit_predict(data_client), index=data_client.index)
        df_neighbors = pd.concat([df_neighbors, data], axis=1)
#        st.dataframe(load_kmeans(sample, chk_id, knn))
        st.dataframe(df_neighbors.iloc[:,1:].sample(10))
        st.markdown("<i>Target 1 = Customer with default</i>", unsafe_allow_html=True)
    else:
        st.markdown("<i>…</i>", unsafe_allow_html=True)
        
        
    st.markdown('***')
    st.markdown("Thanks for going through this Web App with me! I'd love feedback on this")


if __name__ == '__main__':
    main()