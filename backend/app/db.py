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

def create_lead(lead_data: Any) -> Lead:
    leads = load_leads()
    new_id = max([l.id for l in leads], default=0) + 1
    
    # Handle dict or Pydantic model
    if hasattr(lead_data, 'model_dump'):
        data = lead_data.model_dump()
    else:
        data = lead_data
        
    new_lead = Lead(id=new_id, **data)
    leads.append(new_lead)
    save_leads(leads)
    return new_lead

def update_lead(lead_id: int, update_data: Any) -> Optional[Lead]:
    leads = load_leads()
    for i, lead in enumerate(leads):
        if lead.id == lead_id:
            # Handle both Pydantic model and dict
            data = update_data.model_dump(exclude_unset=True) if hasattr(update_data, 'model_dump') else update_data
            updated_lead = lead.model_copy(update=data)
            leads[i] = updated_lead
            save_leads(leads)
            return updated_lead
    return None

def delete_lead(lead_id: int) -> bool:
    leads = load_leads()
    initial_count = len(leads)
    leads = [l for l in leads if l.id != lead_id]
    if len(leads) < initial_count:
        save_leads(leads)
        return True
    return False
