import base64
import os
from dotenv import load_dotenv
from config_redis import create_key_value, var_env

load_dotenv()

if __name__ == "__main__":
    for env in var_env:
        create_key_value(env, os.getenv(env))
