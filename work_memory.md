# 🧠 OVRSEA Technical Test - Work Memory & Progress

## 📅 Context
- **Date:** January 19, 2026
- **Goal:** Prepare for OVRSEA GenAI Technical Test (BDR Automation).
- **Core Requirement:** Light-weight web app + Agentic capabilities.

## 🛠️ Technical Stack
*   **Backend:** **Python + FastAPI** (API & Agent Logic).
*   **Storage:** **JSON File (`leads.json`)** managed via **Pydantic**.
*   **Frontend:** **React (Vite) + Ant Design** (Professional B2B UI).
*   **Agent:** **OpenAI SDK** (Backbone prepared for live coding).

## 🚀 Development Journey (Summary for Presentation)

### Phase 1: Architecture & Setup
*   **Decision:** Chose **FastAPI + React** over Streamlit to demonstrate "Real-Life Impact" and engineering maturity while keeping it lightweight (no heavy DB).
*   **Structure:** Clean separation of concerns (`backend/` vs `frontend/`).
*   **Security:** Implemented `.env` for API keys and proper `.gitignore`.

### Phase 2: Data Engineering (The "BDR" Context)
*   **Strategy:** Created a dataset of **10 Real Companies** (e.g., Sézane, Devialet) with specific logistics characteristics (e.g., "Import from China", "Physical Goods" vs "SaaS").
*   **Schema Design:** Added specific fields like `product_type` and `transport_modes` to enable future Agent reasoning (Shippability checks).

### Phase 3: Web App Implementation (The "Productivity Hack")
*   **UI/UX Design:** 
    *   **Single-View Dashboard:** Combined List View + Detail Panel to minimize clicks.
    *   **Global AI Console:** A terminal-style interface occupying **55%** of the screen, emphasizing the tool's AI-first nature.
    *   **Real-time Search:** Implemented global filtering for Company and Location to speed up BDR workflow.
*   **Tech Highlights:**
    *   Used `Ant Design` for rapid, professional component scaffolding.
    *   Implemented full CRUD (Create, Read, Update, Delete) connected to the JSON backend.

### Phase 4: Agent Preparation (Ready for Live Coding)
*   **Concept:** Designed the AI interaction as a "CLI / Terminal" stream, mimicking tools like Claude Code.
*   **Status:** Backend `Agent` class skeleton is the final step to bridge the UI to the LLM.

## 📋 Task Breakdown & Status

### 1. Technology & Architecture ✅
- [x] Finalize Tech Stack.
- [x] Initialize Git Repository & Project Structure.

### 2. Data Preparation (Leads) ✅
- [x] Define Schema with "BDR Utility" focus.
- [x] Generate 10 real companies data (`leads.json`).

### 3. Web App Design & UI ✅
- [x] **Layout:** Split View (Table + 35% Width Side Panel).
- [x] **AI Console:** **55vh Height**, Light Theme, CLI-style raw text stream, Session Sidebar.
- [x] **Search:** Real-time global inputs for Company/Location above the table.
- [x] **Sorting/Filtering:** Industry sorter, Status/Employee dropdowns.

### 4. Agentic Capabilities 🚧
- [ ] **Backend Implementation:** Create `backend/app/agent.py` with `Agent` class, Pydantic models for structured output, and mock tool registry.

## 📝 Presentation Key Points
*   "I built a **Qualification Engine**, not just a database."
*   "The UI is designed to be an **Agent Cockpit**, where the human oversees the AI's work (Human-in-the-loop)."
*   "The architecture is simple (JSON) but scalable (Pydantic/FastAPI)."
