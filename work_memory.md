# 🧠 OVRSEA Technical Test - Work Memory & Progress

## 📅 Context
- **Date:** January 19, 2026
- **Goal:** Prepare for OVRSEA GenAI Technical Test (BDR Automation).
- **Time Limit:** 3-4 hours preparation.
- **Core Requirement:** Light-weight web app + Agentic capabilities.

## 🛠️ Technical Stack (Finalized)
*   **Backend:** **Python + FastAPI**.
    *   *Role:* API & Agent Logic.
*   **Storage:** **JSON File (`leads.json`) + Pydantic**.
    *   *Why:* Maximum portability & speed. Easy to edit manually.
    *   *Scalability Answer:* "For production (1M+ rows), I'd switch to PostgreSQL (Relational for ID/Name + JSONB for AI insights)."
*   **Frontend:** **TypeScript + React (Vite)**.
    *   *Role:* Client-side logic.
*   **UI Framework:** **Ant Design (antd)**.
    *   *Why:*
        *   **Table:** Best-in-class for listing data (Task 2).
        *   **Drawer:** Perfect for "Quick View" / Agent Interaction without page jumps.
        *   **Aesthetic:** Fits the "Professional B2B SaaS" look (Ovrsea style).
*   **Agent/LLM:** **OpenAI SDK** + **Pydantic** (Structured Outputs).

## 📋 Task Breakdown & Status

### 1. Technology & Architecture ✅
- [x] Finalize Tech Stack.
- [x] Initialize Git Repository & Project Structure.
- [x] Setup `.env` and `.gitignore` for security.

### 2. Data Preparation (Leads) ✅
- [x] Define Schema with "BDR Utility" focus (Shippability, Markets, Product Type).
- [x] Generate 10 real companies data (`leads.json`) with specialized fields.

### 3. Web App Implementation 🚧 (In Progress)
- [ ] **Backend:** Pydantic Models & API for GET/POST leads.
- [ ] **Frontend:** Dashboard with `antd` Table & Drawer for details.

### 4. Agentic Capabilities (Strategic Planning) 🚧
- [x] **Brainstormed Use Cases:**
    - **Qualifier Agent:** Analyze website/product to determine if the lead needs logistics (Physical goods vs. Software).
    - **Researcher Agent:** Find latest news on supply chain expansions or funding.
    - **Personalized Outreach:** Draft cold emails based on specific import/export routes.

### 5. Lead Data Verification (Web Research) ⏳
- [ ] **Verify each company field** in `backend/data/leads.json` against credible sources (official site, press kit, reputable directories).
- [ ] **Document corrections** (employee ranges, locations, product focus, markets, shipping relevance).
- [ ] **Flag uncertain fields** for manual confirmation.

## 🗂️ Lead Schema (Design Decision)
To maximize Agent effectiveness, each lead includes:
- `id`, `company_name`, `website_url`, `location`, `industry`.
- `employee_count`: Qualification criteria.
- `product` & `product_type`: Critical for "Shippability" logic.
- `transport_modes`: Sea, Air, Road, etc.
- `import_locations` & `export_locations`: Key for route-based personalization.

## 📝 Notes
- **Key Strategy:** The app isn't just a table; it's a "Qualification Engine".
- **Interview Hook:** Show how an Agent can filter out "Alan" (SaaS) and prioritize "Devialet" (High-value electronics).
- **Agent Integration:** Ensure the Backend can easily "inject" AI-generated fields into the JSON store.
- **Current Focus:** Deep-verify lead data accuracy; requires web research before finalizing fields.
