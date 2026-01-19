# 🧠 OVRSEA Technical Test - Work Memory & Progress

## 📅 Context
- **Date:** January 19, 2026
- **Goal:** Prepare for OVRSEA GenAI Technical Test (BDR Automation).
- **Time Limit:** 3-4 hours preparation.
- **Core Requirement:** Light-weight web app + Agentic capabilities.

## 🛠️ Technical Stack (Finalized)
*   **Backend:** **Python + FastAPI**.
*   **Storage:** **JSON File (`leads.json`) + Pydantic**.
*   **Frontend:** **TypeScript + React (Vite) + Ant Design**.
*   **Agent/LLM:** **OpenAI SDK** + **Pydantic** (Structured Outputs).

## 📋 Task Breakdown & Status

### 1. Technology & Architecture ✅
- [x] Finalize Tech Stack.
- [x] Initialize Git Repository & Project Structure.
- [x] Setup `.env` and `.gitignore` for security.

### 2. Data Preparation (Leads) ✅
- [x] Define Schema with "BDR Utility" focus.
- [x] Generate 10 real companies data (`leads.json`).

### 3. Web App Design (Product Spec) 📝
- **Core Philosophy:** "Container for Agents" - Simple CRM wrapper around AI capabilities.
- **Pipeline Stages (Status):**
    - `New`: Freshly added.
    - `Qualified`: Passed AI/Manual check.
    - `Disqualified`: Not a fit (e.g., pure SaaS).
    - `Contacted`: Outreach initiated.
    - `Negotiating`: Deep in sales cycle.
- **UI Structure:**
    1.  **Lead List (Main View):**
        - Antd `Table`. Columns: Name, Industry, Country, Employees, **Status (Tag)**, Actions (Delete).
        - **Global Controls:** "Refresh List", "Add Lead" (Modal).
        - **Agent Placeholder (Layer 1):** A reserved **"AI Chat/Action Dialog"** space above or beside the table for global commands (e.g., "Find leads similar to Sezane").
    2.  **Lead Detail (Drawer):**
        - Opens on row click.
        - **Read/Write:** All fields editable via inputs or "Edit Mode".
        - **No "Per-Lead" AI Buttons:** Keep the drawer strictly for data viewing/editing to avoid clutter.
- **CRUD Requirements:**
    - [ ] List all leads.
    - [ ] View single lead details.
    - [ ] Create new lead (Modal).
    - [ ] Update lead info (Drawer).
    - [ ] Delete lead (Table Action).

### 4. Web App Implementation 🚧
- [ ] **Backend:** Pydantic Models & API for GET/POST/PATCH/DELETE.
- [ ] **Frontend:** Dashboard with `antd` Table & Drawer.

### 5. Agentic Capabilities (Strategic Planning) 🚧
- [x] **Brainstormed Use Cases.**
- [ ] **Tooling Preparation:** Setup minimal `Agent` class in Python.

## 📝 Notes
- **Simplification:** Removed complex "Enriching" state and per-lead AI buttons. Focus on a clean, manual CRM first, with a single "Global AI Entry Point" reserved.