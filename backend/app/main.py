from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from app.models import Lead, LeadCreate, LeadUpdate, LeadStatus
from app.db import load_leads, save_leads
from app.agent_service import get_agent_instance
from pydantic import BaseModel

app = FastAPI(title="Ovrsea BDR Tool")

# Global Agent Instance (Simple Memory persistence for demo)
# In production, use Redis or a proper Session Manager
agent_instance = get_agent_instance()

class ChatRequest(BaseModel):
    message: str

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/agent/chat")
def agent_chat(request: ChatRequest):
    """
    Endpoint for the Frontend AI Terminal.
    Passes user message to the AgentRuntime and returns the final text.
    """
    try:
        response_text = agent_instance.run(request.message)
        return {"response": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/agent/reset")
def reset_agent_memory():
    """
    Clears the agent's memory for a new session.
    """
    agent_instance.reset_memory()
    return {"status": "memory_cleared"}

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
