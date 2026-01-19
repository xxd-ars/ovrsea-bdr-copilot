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

### 1. Technology & Architecture 🚧 (In Progress)
- [x] Finalize Tech Stack.
- [ ] Initialize Git Repository.
- [ ] **Backend Setup:** FastAPI + Pydantic Models + JSON Manager.
- [ ] **Frontend Setup:** Vite + React + Ant Design.

### 2. Data Preparation (Leads) ⏳
- [ ] Define the 5 characteristics (Schema).
- [ ] Generate 10 real companies data (`leads.json`).

### 3. Web App Implementation ⏳
- [ ] **Backend:** API for GET/POST leads (Reading/Writing `leads.json`).
- [ ] **Frontend:** Dashboard with `antd` Table.
- [ ] **Frontend:** Lead Detail view (Drawer/Sidepanel).

### 4. Agentic Capabilities (Preparation for Live Coding) ⏳
- [ ] Setup LLM Client (Env variables management).
- [ ] Create `Agent` class/helper.
- [ ] **Tooling:** Prepare `Tool` decorators/structure for live coding.

## 📝 Notes
- **Focus:** Utility and Speed.
- **Key Strategy:** Use `antd` components to avoid writing CSS.
- **Agent Integration:** Ensure the Backend can easily "inject" AI-generated fields into the JSON store.