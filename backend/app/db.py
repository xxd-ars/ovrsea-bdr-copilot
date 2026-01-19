import json
import os
from typing import List
from app.models import Lead

DATA_FILE = "data/leads.json"

def load_leads() -> List[Lead]:
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
        return [Lead(**item) for item in data]

def save_leads(leads: List[Lead]):
    with open(DATA_FILE, "w") as f:
        json.dump([lead.model_dump() for lead in leads], f, indent=2)
