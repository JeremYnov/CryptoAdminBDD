Lancer les containers
```
docker-compose up 
```

être à la racine du projet
```
cd scripts
```

Creation et activation du virtual environnement:

-Windows
```
py -3 -m venv venv
venv\Scripts\activate
```

-Linux/Mac
```
python3 -m venv venv
. venv/bin/activate
```

Installation des dependances
```
pip install -r requirements.txt
```

Insertion des token en base pour récuperer les différentes source de donnée
```
python sender_token.py
```
