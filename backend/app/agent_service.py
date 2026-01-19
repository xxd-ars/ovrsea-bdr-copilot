import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from app.agent_core import AgentRuntime, ToolRegistry
from app import db, models

load_dotenv()

# --- 1. Define Tools ---

registry = ToolRegistry()

@registry.register
def get_database_summary():
    """
    Reads the current leads database and returns a summary of all leads.
    Use this to understand the current state of the CRM.
    """
    leads = db.get_leads()
    # Serialize to simple string to save tokens
    summary = []
    for l in leads:
        summary.append(f"ID {l.id}: {l.company_name} ({l.location}) - Status: {l.status}")
    return {"total": len(leads), "leads": summary}

@registry.register
def get_lead_details(lead_id: int):
    """
    Get full details for a specific lead by ID.
    Includes product type, transport modes, etc.
    """
    leads = db.get_leads()
    for l in leads:
        if l.id == lead_id:
            return l.model_dump()
    return {"error": "Lead not found"}

@registry.register
def update_lead_status(lead_id: int, new_status: str):
    """
    Updates the status of a lead.
    Allowed statuses: "New", "Qualified", "Disqualified", "Contacted", "Negotiating", "Closed".
    """
    try:
        # Validate status against Enum
        valid_statuses = [s.value for s in models.LeadStatus]
        if new_status not in valid_statuses:
            return {"error": f"Invalid status. Must be one of {valid_statuses}"}
            
        lead = db.update_lead(lead_id, models.LeadUpdate(status=new_status))
        if lead:
            return {"success": True, "new_status": lead.status}
        return {"error": "Lead not found"}
    except Exception as e:
        return {"error": str(e)}

@registry.register
def delete_lead_by_id(lead_id: int):
    """
    Permanently deletes a lead from the database.
    """
    success = db.delete_lead(lead_id)
    return {"success": success}

@registry.register
def web_search_google(query: str):
    """
    Performs a real web search using OpenAI's native web_search capability.
    Use this to find location, industry, or news about a company to qualify leads.
    """
    print(f"[SEARCH] Searching OpenAI Native for: {query}")
    try:
        # Initialize a dedicated client for this specific experimental call
        # We rely on the environment variables for configuration
        client = OpenAI() 
        
        # Using the experimental 'responses' endpoint as requested
        # Note: Model is hardcoded to "gpt-4o" as "gpt-5" is not generally available yet
        response = client.responses.create(
            model="gpt-4o", 
            tools=[{"type": "web_search"}],
            input=f"Search results for: {query}"
        )
        
        # Assuming the attribute is .output_text based on user input
        return {"results": response.output_text}
    except Exception as e:
        print(f"[SEARCH ERROR] {str(e)}")
        return {"error": f"Search failed: {str(e)}"}

# --- 2. Initialize Agent ---

BDR_SYSTEM_PROMPT = """
You are an expert BDR (Business Development Representative) Agent for OVRSEA.
OVRSEA is a digital freight forwarder coordinating international transport.

Your Mission:
1. Qualify leads: Look for companies shipping PHYSICAL GOODS internationally.
2. Disqualify leads: Pure SaaS, local services (hairdressers, consulting), or non-shipping companies.
3. Manage CRM: You have full access to the database to update statuses or delete bad leads.

Rules:
- ALWAYS check the database summary first if the user asks about "all leads".
- If a user asks to "cleanup" or "qualify" leads, iterate through them, check their details/search, and update their status.
- Be concise and professional.
"""

def get_agent_instance():
    """
    Factory to get a fresh agent instance.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1") 
    model = os.getenv("OPENAI_MODEL", "openai/gpt-4o-mini")
    
    if not api_key:
        print("[WARNING] No OpenAI API Key found.")
        
    client = OpenAI(api_key=api_key, base_url=base_url)
    agent = AgentRuntime(client=client, system_prompt=BDR_SYSTEM_PROMPT, model=model)
    agent.set_tools(registry)
    return agent
