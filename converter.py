import ssl
import urllib.request

ssl._create_default_https_context = ssl._create_unverified_context

import pandas as pd
import json

df = pd.read_json("./deployment/models/file.json")

df_formatted = [
    {
        "messages": [
            {
                "role": "user",
                "content": f"""
                Nama kamu adalah MinKA,
                Gunakan bahasa Indonesia,
                Kamu adalah AI assistant yang sangat powerful untuk KiriminAja,
                jangan menjawab apapun selain dengan konteks,
                ### Input:
                {row["question"]}

                ### Context:
                {row["context"]}

                ### Response:
                """,
            },
            {"role": "assistant", "content": row["answer"]},
        ]
    }
    for _, row in df.iterrows()
]

with open("data.jsonl", "w") as f:
    for line in df_formatted:
        json.dump(line, f)
        f.write("\n")