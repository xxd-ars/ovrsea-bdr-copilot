from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from app.models import Lead, LeadCreate, LeadUpdate, LeadStatus
from app.db import load_leads, save_leads

app = FastAPI(title="Ovrsea BDR Tool")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/leads", response_model=List[Lead])
def get_leads():
    return load_leads()

@app.get("/leads/{lead_id}", response_model=Lead)
def get_lead(lead_id: int):
    leads = load_leads()
    for lead in leads:
        if lead.id == lead_id:
            return lead
    raise HTTPException(status_code=404, detail="Lead not found")

@app.post("/leads", response_model=Lead)
def create_lead(lead: LeadCreate):
    leads = load_leads()
    new_id = max([l.id for l in leads], default=0) + 1
    new_lead = Lead(id=new_id, **lead.model_dump())
    leads.append(new_lead)
    save_leads(leads)
    return new_lead

@app.patch("/leads/{lead_id}", response_model=Lead)
def update_lead(lead_id: int, lead_update: LeadUpdate):
    leads = load_leads()
    for i, lead in enumerate(leads):
        if lead.id == lead_id:
            update_data = lead_update.model_dump(exclude_unset=True)
            updated_lead = lead.model_copy(update=update_data)
            leads[i] = updated_lead
            save_leads(leads)
            return updated_lead
    raise HTTPException(status_code=404, detail="Lead not found")

@app.delete("/leads/{lead_id}")
def delete_lead(lead_id: int):
    leads = load_leads()
    leads = [l for l in leads if l.id != lead_id]
    save_leads(leads)
    return {"ok": True}
