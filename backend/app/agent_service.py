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
    leads = db.load_leads()
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
    leads = db.load_leads()
    for l in leads:
        if l.id == lead_id:
            return l.model_dump()
    return {"error": "Lead not found"}

@registry.register
def update_lead(lead_id: int, 
                status: str = None,
                location: str = None,
                industry: str = None,
                employee_count: str = None,
                company_name: str = None,
                website_url: str = None,
                product_type: str = None,
                transport_modes: str = None):
    """
    Updates ANY field of a lead. 
    Use this to change status, correct location, update industry, etc.
    
    Args:
        lead_id: ID of the lead
        status: One of "New", "Qualified", "Disqualified", "Contacted", "Negotiating"
        location: e.g. "Paris, France"
        industry: e.g. "Fashion"
        employee_count: e.g. "50-100"
        product_type: "Physical Goods" or "Software / Service"
        transport_modes: Comma-separated string, e.g. "Air, Sea"
    """
    try:
        # Construct update object
        update_data = {}
        if status:
            valid_statuses = [s.value for s in models.LeadStatus]
            if status not in valid_statuses:
                return {"error": f"Invalid status. Must be one of {valid_statuses}"}
            update_data['status'] = status
            
        if location: update_data['location'] = location
        if industry: update_data['industry'] = industry
        if employee_count: update_data['employee_count'] = employee_count
        if company_name: update_data['company_name'] = company_name
        if website_url: update_data['website_url'] = website_url
        if product_type: update_data['product_type'] = product_type
        if transport_modes: 
            # Convert string input back to list for model
            update_data['transport_modes'] = [m.strip() for m in transport_modes.split(',')]

        if not update_data:
            return {"warning": "No fields provided to update."}

        # Call DB update
        # We use model_validate to handle the Pydantic conversion safely if needed, 
        # but here we pass a dict directly to our db.update_lead which we upgraded to handle it.
        lead = db.update_lead(lead_id, models.LeadUpdate(**update_data))
        
        if lead:
            return {"success": True, "updated_fields": list(update_data.keys())}
        return {"error": "Lead not found"}
    except Exception as e:
        return {"error": str(e)}

@registry.register
def add_lead(company_name: str, website_url: str, location: str = "Unknown", industry: str = "Unknown"):
    """
    Adds a NEW lead to the database.
    Use this when the user asks to add a company or when you find a promising company during search.
    
    Args:
        company_name: Name of the company
        website_url: URL (e.g. https://example.com) - REQUIRED
        location: HQ location
        industry: Business sector
    """
    try:
        new_lead = db.create_lead({
            "company_name": company_name,
            "website_url": website_url,
            "location": location,
            "industry": industry,
            "employee_count": "Unknown" # Default
        })
        return {"success": True, "new_id": new_lead.id, "company": new_lead.company_name}
    except Exception as e:
        return {"error": f"Failed to add lead: {str(e)}"}

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
        # Re-use the same configuration logic as the main agent to ensure consistency
        # or separate logic if specifically intended for native features.
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1")
        
        client = OpenAI(api_key=api_key, base_url=base_url)
        
        # Using the experimental 'responses' endpoint
        response = client.responses.create(
            model="gpt-4o", 
            tools=[{"type": "web_search"}],
            input=f"Search results for: {query}"
        )
        
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
