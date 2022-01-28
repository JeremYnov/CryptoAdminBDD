# CryptoAdminBDD

### Architecture du projet :
- hadoop/namenode : configuration du container docker hadoop master (namenode) pour envoyer les csv de text_data dans hdfs toutes les heures

- interface : contient l'interface utilisateur réaliser en streamlit
    - apps : contient les différentes pages de l'interface
    - scripts : contient les différents script ou l'on recupere une donnée sans base de donnée (ex: scrapping)
    - app.py et multiapp.py : permette de changer de page et de lancer streamlit

- numeric_data : contient un producer et un consumer qui vont récuperer les données numerique en streaming (temps réel)
    - producer/ccxt_producer : recupere les datas des crypto BTC, ETH et SOL en temps réel grâce à la librairie ccxt
    - consumer/ccxt_consumer : normalise les données et les insere en base de données

- scripts : contient les 3 protocole : [1er deploiement](https://github.com/JeremYnov/CryptoAdminBDD/blob/main/scritps/first_deployment.md), [reinitialisation](https://github.com/JeremYnov/CryptoAdminBDD/blob/main/scritps/reset.md), [redémarrage](https://github.com/JeremYnov/CryptoAdminBDD/blob/main/scritps/restart.md)
    - sender_token.py : permet d'envoyer les différents token pour recuperer les datas en base (1er deploiement et reinitialisation)
    - requirements.txt : contient les dependances à installer (pip install -r requirements.txt) qu'il faudra installer dans son venv

- sentiment_analysis : contient un scheduler qui va réaliser une analyse de sentiment sur des données textuel provenant de twitter, reddit et cryptopanic par rapport à une crypto
    - producer
        - csv : contient les datas textuel supprimer de la collection text_data apres avoir été analyser. ces csv seront envoyer dans hadoop
        - sentiment_producer.py : réalise l'analyse de sentiment, puis les stockent en base et supprime les datas textuel de la collection text_data et écris dans le csv les datas supprimer
        - function_sentiment.py : contient 3 fonctions qui permette d'aherer le code de sentiment_producer.py : recuperer la polarity du texte, recuperer la subjectivity du texte, et ecrire les datas dans le csv (creer le dossier csv si il n'existe pas)

- text_data : contient un producer et un consumer qui vont récuperer les données textuel en streaming (twitter, reddit, cryptopanic)
    - consumer/ccxt_consumer : normalise les données et les insere en base de données
    - producer
        - config_redis.py : contient la connexion à la base redis pour recuperer les tokens ainsi que la fonction pour recuperer les tokens
        - cryptoPanicData.py, redditData.py, twitterData.py : ces 3 scripts retourne les datas que l'ont veut récuperer 
        - text_producer.py : récupere les 3 types de données avec les scripts au dessus, et les envoies au consumer

- .env : contient toutes les variables d'environnement qui reste static, tel le réseau kafka, les tokens ou les accés de connexion pour mongo (il y'en a un dans chaque sous dossier)

- .gitignore : contient les fichiers qu'on ne veut pas envoyer sur git (le dossier csv, les pycaches, le dossier data de mongo ou le venv)

- docker.compose.yml : contient notre réseau docker avec toutes ces images
    - mongodb
    - redis

    - namenode
    - datanode
    - ressourcemanager
    - nodemanager1
    - historyserver

    - kafka
    - zookeeper

    - ccxt-producer
    - text-producer
    - sentiment-producer
    - ccxt-consumer
    - text_consumer
    - sentiment-analysis (commenter mais peut etre decommenter si l'on veut faire des tests -> sentiment_analysis/sentiment_analysis.py)

    - streamlit

    - volume
        - redis
        - hadoop_namenode
         -hadoop_datanode
         -hadoop_historyserver
         -mongodb

    - networks
        - kafka
            -driver: "bridge"

- Dockerfile_python : lancer les différentes commande dans les container qui execute des scripts python

- hadoop.env : variable d'environnement hadoop

- mld.vuerd.json : contient les différentes collection avec leurs colonnes


### Collection base de donnée :

- numeric_data : contient les données numérique (ccxt)
- text_data : collection qui conserve les données temporairement avant de faire une analyse de sentiment, puis les données sont stocké dans un csv qui sera envoyer à hadoop (twitter, reddit, cryptopanic)
- sentiment_analysis : contient l'analyse de sentiment des données textuel
