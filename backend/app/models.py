from typing import List, Optional
from pydantic import BaseModel
from enum import Enum

class LeadStatus(str, Enum):
    NEW = "New"
    QUALIFIED = "Qualified"
    DISQUALIFIED = "Disqualified"
    CONTACTED = "Contacted"
    NEGOTIATING = "Negotiating"

class Lead(BaseModel):
    id: int
    company_name: str
    website_url: str
    location: str
    industry: str
    employee_count: str
    product: Optional[str] = None
    product_type: Optional[str] = None
    transport_modes: List[str] = []
    import_locations: List[str] = []
    export_locations: List[str] = []
    status: LeadStatus = LeadStatus.NEW

class LeadCreate(BaseModel):
    company_name: str
    website_url: str
    location: Optional[str] = ""
    industry: Optional[str] = ""
    employee_count: Optional[str] = ""

class LeadUpdate(BaseModel):
    company_name: Optional[str] = None
    website_url: Optional[str] = None
    location: Optional[str] = None
    industry: Optional[str] = None
    employee_count: Optional[str] = None
    product: Optional[str] = None
    product_type: Optional[str] = None
    transport_modes: Optional[List[str]] = None
    import_locations: Optional[List[str]] = None
    export_locations: Optional[List[str]] = None
    status: Optional[LeadStatus] = None
