Creation environnement virtuel

pip install -r requirements.txt

<!-- on lance le docker-compose.yml -->
docker-compose up -d

<!-- envoie des données en base -->
python send_token.py

<!-- on recupere kes données -->
python get_token