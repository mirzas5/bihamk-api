# main.py
from fastapi import FastAPI, Query
from typing import List, Optional
import uvicorn, re, json, pathlib

app = FastAPI()

# pretend you’re loading from DB; you already return this in /radars
DATA_PATH = pathlib.Path(__file__).with_name("radars.json")
with DATA_PATH.open(encoding="utf-8") as f:
    RADARS = json.load(f)

@app.get("/")
def read_root():
    return {
        "message": "Radar API – GET /radars or /radars?route=Zenica-Sarajevo"
    }

@app.get("/radars")
def get_radars(route: Optional[str] = Query(None, description="e.g. Zenica-Sarajevo")):
    """
    If ?route=Zenica-Sarajevo is supplied, return only the entries whose `text`
    contains *all* tokens (case‑insensitive). You can loosen logic if you like.
    """
    if not route:
        return RADARS

    # Split on dash, comma, space… → ['Zenica', 'Sarajevo']
    tokens: List[str] = [t.strip() for t in re.split(r"[-,/]", route) if t.strip()]
    pattern = re.compile("|".join(map(re.escape, tokens)), re.I)

    return [r for r in RADARS if pattern.search(r["text"])]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
