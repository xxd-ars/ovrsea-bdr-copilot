export interface Lead {
  id: number;
  company_name: string;
  website_url: string;
  location: string;
  industry: string;
  employee_count: string;
  product?: string;
  product_type?: string;
  transport_modes: string[];
  import_locations: string[];
  export_locations: string[];
  status: 'New' | 'Qualified' | 'Disqualified' | 'Contacted' | 'Negotiating';
}

export type LeadUpdate = Partial<Lead>;

export interface LeadCreate {
    company_name: string;
    website_url: string;
    location?: string;
    industry?: string;
    employee_count?: string;
}
