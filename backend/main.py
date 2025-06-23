
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, conlist
from typing import List
from .engine import LifeEngine, TALENTS, LifeResult

app = FastAPI(title="LifeRestart API")

class Req(BaseModel):
    talent_ids: conlist(int, min_length=1, max_length=3) # type: ignore

@app.post("/run", response_model=LifeResult)
def run(req: Req):
    if any(tid not in TALENTS for tid in req.talent_ids):
        raise HTTPException(status_code=400, detail="invalid talent id")
    engine = LifeEngine(req.talent_ids)
    return engine.run()
