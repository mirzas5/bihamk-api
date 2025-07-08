from fastapi import FastAPI, Query
from typing import List, Dict, Optional
import re, uvicorn, asyncio

from scraper import scrape_radars   # ← import your own code

app = FastAPI()

@app.get("/")
def root():
    return {"msg": "Radar API – try /radars?route=Zenica-Sarajevo"}

@app.get("/radars")
async def get_radars(
    route: Optional[str] = Query(None, description="e.g. Zenica-Sarajevo")
):
    # Run Playwright scraper (IO‑bound → run in threadpool so FastAPI stays async)
    radars: List[Dict] = await asyncio.to_thread(asyncio.run, scrape_radars())

    if not route:
        return radars

    tokens = [t.strip() for t in re.split(r"[-,/]", route) if t.strip()]
    return [
        r for r in radars
        if any(tok.lower() in r["text"].lower() for tok in tokens)
    ]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)