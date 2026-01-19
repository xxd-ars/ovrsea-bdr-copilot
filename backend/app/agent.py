import os
import json
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# --- Structured Output Models ---

class LeadAnalysis(BaseModel):
    is_qualified: bool = Field(description="Whether the company is a good lead for OVRSEA (Digital Freight Forwarding)")
    reasoning: str = Field(description="Explanation for the qualification status")
    suggested_strategy: str = Field(description="How a BDR should approach this lead")
    estimated_volume_priority: str = Field(description="High, Medium, or Low based on product type and size")

class AgentResponse(BaseModel):
    thought: str = Field(description="The agent's internal reasoning process")
    action_taken: str = Field(description="Description of tools used or steps performed")
    output_text: str = Field(description="The raw text to be displayed in the terminal")
    data: Optional[Dict[str, Any]] = None

# --- Agent Core ---

BDR_SYSTEM_PROMPT = """
You are the OVRSEA BDR AI Assistant. OVRSEA is a digital freight forwarder.
Your goal is to help Sales Reps (BDRs) automate lead research, qualification, and outreach.

Target Profile:
- Companies that ship PHYSICAL GOODS (e.g., Fashion, Electronics, Manufacturing).
- Companies with INTERNATIONAL import/export needs (e.g., shipping from China to Europe).
- Avoid: Pure SaaS, Software, or local service companies (e.g., Insurance, Booking platforms).

Capabilities:
1. Qualify leads based on product type and website info.
2. Draft highly personalized cold emails focused on supply chain pain points (visibility, carbon tracking).
3. Extract shipping patterns from context clues.

Always be concise, professional, and data-driven in the terminal output.
"""

class BDRAgent:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key) if api_key else None
        self.model = "gpt-4o" # Recommended for complex reasoning

    def run(self, command: str, lead_context: Optional[Dict] = None) -> AgentResponse:
        """
        Executes a command. In a real interview, you would implement 
        actual Tool Calling or multi-step logic here.
        """
        if not self.client:
            return AgentResponse(
                thought="No API key found.",
                action_taken="Error check",
                output_text="[ERROR] OpenAI API Key is missing. Please check your .env file."
            )

        # Basic implementation of a chat completion for the interview
        try:
            # Preparing context
            lead_info = f"Context Lead: {json.dumps(lead_context)}" if lead_context else "No specific lead selected."
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": BDR_SYSTEM_PROMPT},
                    {"role": "user", "content": f"{lead_info}\n\nUser Instruction: {command}"}
                ]
            )
            
            answer = response.choices[0].message.content
            
            return AgentResponse(
                thought="Interpreting user command and analyzing lead context...",
                action_taken="LLM_PROCESSING",
                output_text=answer
            )
        except Exception as e:
            return AgentResponse(
                thought="An error occurred during API call.",
                action_taken="EXCEPTION_HANDLING",
                output_text=f"[FATAL] Error: {str(e)}"
            )

    async def stream_run(self, command: str, lead_context: Optional[Dict] = None):
        """
        Generator for streaming responses (Advanced for interview).
        """
        # Placeholder for streaming logic
        yield "[THOUGHT] Initializing agentic workflow..."
        yield "[ACTION] Processing command: {command}"
        # Real streaming implementation would go here
