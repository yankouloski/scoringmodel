<<<<<<< HEAD
=======
# Implémentez un modèle de scoring


## Presentation du projet du parcours

Une entreprise souhaite développer un modèle de scoring basé sur la probabilité de défaut de paiement des clients et ce afin d'éclairer la décision d'accorder ou non un prêt à un client potentiel en s’appuyant sur des sources de données variées (données comportementales, données provenant d'autres institutions financières, etc.).

## Compétences évaluées

    Présenter son travail de modélisation à l'oral
    Déployer un modèle via une API dans le Web
    Utiliser un logiciel de version de code pour assurer l’intégration du modèle
    Rédiger une note méthodologique afin de communiquer sa démarche de modélisation
    Réaliser un dashboard pour présenter son travail de modélisation



## **Fonctionalitées du Dashboard Scoring Credit**

L'application est déployé ici **Lien à incruster**


L'application répond au cahier des charges suivant :

  - Permettre de visualiser le score et l’interprétation de ce score pour chaque client pour une personne non experte en data science.
  - Permettre de visualiser des informations descriptives relatives à un client (via un système de filtre).
  - Permettre de comparer les informations descriptives relatives à un client à l’ensemble des clients ou à un groupe de clients similaires.
  

## Conception

La manipulation des données et l'entrainement (en exécution CPU) du modèle ont été fait en Python sur support Jupyter Notebook avec développement de l'app Streamlit.

## Les données

Données Kaggle : https://www.kaggle.com/c/home-credit-default-risk/data


## Prérequis techniques

Si vous n'avez jamais installé Python, alors autant installer directement la distribution Anaconda. Anaconda est vraiment une distribution Python, faite pour la Data Science.

De cette manière on peut installer Python et ses librairies de Data Science Pandas, Matplotlib, Seaborn, Scipy, Numpy etc… Mais aussi le notebook Jupyter, qui reste incontournable et vivement recommandé! 

Pour Anaconda c'est par ici : **https://docs.anaconda.com/anaconda/navigator/**

Si vous souhaitez lancer le projet, il sera nécessaire d'installer Jupyter Notebook sur votre machine.

La documentation sur Jupyter est accessible ici: **https://jupyter.org/**

**Il sera egalement necessaire d'installer les principales librairie de Python**

pip install pandas
pip install matplotlib
pip install numpy
pip install scipy

## Heroku Git

Pour l'installation de Heroku Command Line Interface (CLI), voir ici:
      **https://devcenter.heroku.com/articles/heroku-cli**
      
Lorsque vous aurez installé Heroku sur votre machine et créé un compte, il sera temps de vous connecter à votre compte Heroku depuis le terminal. Pour ce faire, exécutez la commande suivante dans votre terminal :

$ heroku login

Pour la mise à jour des modifications utilisez les commandes suivantes

$ git add .
$ git commit -am "make it better"
$ git push heroku master


## Ressources Streamlit 

La présentation des ressources est disponible ici:  **https://streamlit.io/**

D'autres ressources utiles sont disponible ici:  https://share.streamlit.io/daniellewisdl/streamlit-cheat-sheet/app.py

## Ressouces graphique

Pour réaliser des graphiques claire et pertinent c'est par ici: 
https://www.psiweb.org/docs/default-source/2018-psi-conference-posters/48-julie-jones.pdf


## Auteur

Yankouloski (Yankou DIASSO) - https://github.com/yankouloski -
>>>>>>> 1d0da45edabb76bf272cde2f5b5f0ef15923ce9a
