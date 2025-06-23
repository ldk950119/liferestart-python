
from pathlib import Path
import json
from typing import List, Dict
from .models import Talent, Event, Ending, LifeLog, LifeResult

BASE_ATTR = {"int": 10, "hp": 100, "money": 10, "luck": 0}

def _load(model, fname: str):
    path = Path(__file__).parent / "data" / fname
    return [model(**obj) for obj in json.loads(path.read_text(encoding="utf-8"))]

TALENTS: Dict[int, Talent] = {t.id: t for t in _load(Talent, "talent.json")}
EVENTS: Dict[int, Event]   = {e.id: e for e in _load(Event, "event.json")}
ENDINGS: List[Ending]      = _load(Ending, "ending.json")

class LifeEngine:
    def __init__(self, talent_ids: List[int]):
        self.attr = BASE_ATTR.copy()
        for tid in talent_ids:
            for k, v in TALENTS[tid].effect.items():
                self.attr[k] = self.attr.get(k, 0) + v
        self.log: List[LifeLog] = []

    def run(self) -> LifeResult:
        for age in sorted({e.age for e in EVENTS.values()}):
            self._apply_event(age)
            if self.attr['hp'] <= 0:
                break
        ending = self._pick_ending()
        return LifeResult(log=self.log, final_age=self.log[-1].age, ending=ending)

    def _apply_event(self, age: int):
        ev = next(e for e in EVENTS.values() if e.age == age)
        for k, v in ev.effect.items():
            self.attr[k] = self.attr.get(k, 0) + v
        self.log.append(LifeLog(age=age, event_id=ev.id, desc=ev.desc))

    def _pick_ending(self) -> Ending:
        age = self.log[-1].age
        for ed in ENDINGS:
            lo = ed.cond.get("age_min", 0)
            hi = ed.cond.get("age_max", 999)
            if lo <= age < hi:
                return ed
        return ENDINGS[-1]
