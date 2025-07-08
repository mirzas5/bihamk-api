from fastapi import FastAPI, Query
from typing import List, Dict, Optional
import re, httpx         # add "httpx" to requirements.txt if it's not there
import uvicorn

app = FastAPI()

# ----------------------------------------------------------------------
# 1.  Fetch the radar list dynamically
#    – Option A: pull JSON directly from BIHAMK (example URL below)
#    – Option B: import your own scraper function instead of httpx
# ----------------------------------------------------------------------
BIHAMK_JSON_URL = "https://bihamk.ba/spi/radari/json"      # ← change if needed

async def fetch_radars() -> List[Dict]:
    """
    Return a list like:
    [
      {"id":"412","title":"…","text":"KANTON SARAJEVO\n…"},
      …
    ]
    """
    async with httpx.AsyncClient() as client:
        resp = await client.get(BIHAMK_JSON_URL, timeout=15)
        resp.raise_for_status()
        return resp.json()

# ----------------------------------------------------------------------
# 2.  Routes
# ----------------------------------------------------------------------
@app.get("/")
def root():
    return {
        "msg": "Radar API – try /radars or /radars?route=Novi-Travnik-Jajce"
    }

@app.get("/radars")
async def get_radars(
    route: Optional[str] = Query(
        None, description="Route string, e.g. Zenica-Sarajevo"
    )
):
    radars = await fetch_radars()          # live data every call

    # No route supplied → return everything
    if not route:
        return radars

    # Split “Zenica-Sarajevo” → ["Zenica", "Sarajevo"]
    tokens = [t.strip() for t in re.split(r"[-,/]", route) if t.strip()]

    # Any token match (= OR logic).  Change `any`→`all` for AND logic
    return [
        r for r in radars
        if any(tok.lower() in r["text"].lower() for tok in tokens)
    ]

# ----------------------------------------------------------------------
# 3.  Local dev server
# ----------------------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)