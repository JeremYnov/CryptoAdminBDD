import base64
import csv
from config_redis import create_key_value

if __name__ == "__main__":
    with open('../csv/token.csv') as csvfile:
        content_csv = csv.reader(csvfile)
        for row in content_csv:
            try:
                create_key_value(row[0], base64.b64encode(row[1].encode()))
                print("Token enregistré en bdd")
            except :
                print(f"Erreur d'enregistrement du token {row[1]} avec la key {row[0]}")