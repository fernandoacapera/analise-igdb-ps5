from request import token
from igdb.wrapper import IGDBWrapper
from dotenv import load_dotenv
import os
from rich import print
import json
import pandas as pd
from sqlalchemy import create_engine
load_dotenv()

wrapper = IGDBWrapper(
    client_id=os.getenv("CLIENT_ID"),
    auth_token=token())

import time

def fetch_ps5_games():
    all_data = []
    offset = 0
    while True:
        query = f"fields *; where platforms = (167); limit 500; offset {offset};"
        byte_array = wrapper.api_request('games', query)
        data = json.loads(byte_array.decode("utf-8"))
        if not data:
            break
        all_data.extend(data)
        offset += 500
        time.sleep(0.3)  
    return all_data

jogos_ps5 = fetch_ps5_games()

def extract_to_sql(data):
    df = pd.DataFrame(data)

    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, (list, dict))).any():
            df[col] = df[col].apply(
                lambda x: json.dumps(x) if isinstance(x, (list, dict)) else x
            )

    engine = create_engine('sqlite://', echo=False)
    df.to_sql('jogos_ps5', engine, index=False, if_exists='replace')

    with open("ps5_jogos.sql", "w", encoding="utf-8") as f:
        conn = engine.raw_connection()
        for linha in conn.iterdump():
            if 'INSERT INTO' in linha:
                f.write(f"{linha}\n")

    return "gerado com sucesso"

extract_to_sql(jogos_ps5)

