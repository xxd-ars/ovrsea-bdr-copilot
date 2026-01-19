# 🧠 OVRSEA Technical Test - Work Memory & Progress

## 📅 Context
- **Date:** January 19, 2026
- **Goal:** Prepare for OVRSEA GenAI Technical Test (BDR Automation).
- **Core Requirement:** Light-weight web app + Agentic capabilities.

## 🛠️ Technical Stack
*   **Backend:** **Python + FastAPI** (API & Agent Logic).
*   **Storage:** **JSON File (`leads.json`)** managed via **Pydantic**.
*   **Frontend:** **React (Vite) + Ant Design** (Professional B2B UI).
*   **Agent:** **OpenAI SDK + Custom Tool Registry** (ReAct Engine).

## 🚀 Development Journey (Summary for Presentation)

### Phase 1: Architecture & Setup
*   **Decision:** Chose **FastAPI + React** to simulate a real production environment.
*   **Structure:** Clean separation of concerns (`backend/` vs `frontend/`).
*   **Security:** Implemented `.env` for API keys and `.gitignore` for safety.

### Phase 2: Data Engineering (The "BDR" Context)
*   **Strategy:** Created a dataset of **10 Real Companies** (e.g., Sézane, Devialet) with logistics-specific fields (`transport_modes`, `import_locations`) to test Agent reasoning.

### Phase 3: Web App Implementation (The "Productivity Hack")
*   **UI/UX Design:** 
    *   **Single-View Dashboard:** List View + 35% Detail Panel + **55% AI Terminal**.
    *   **Real-time Search:** Global filtering for instant data access.
*   **Tech Highlights:**
    *   Full CRUD connected to JSON backend.
    *   Real-time UI updates when Agent modifies data.

### Phase 4: Agentic Capabilities (The "Brain") ✅
We built a robust **Agent Runtime** from scratch, designed to ace the interview's "speed & utility" requirements.

*   **Architecture (Core vs Service):**
    *   `agent_core.py`: A reusable **ReAct Engine** that handles the LLM loop, tool execution, and memory management.
    *   `agent_service.py`: The **Business Logic** layer where we inject OVRSEA-specific prompts and register BDR tools.
*   **Key Features Implemented:**
    1.  **Tool Registry**: A decorator-based system (`@registry.register`) to turn any Python function into an LLM-ready tool instantly.
    2.  **Mock Tools**: Pre-built `web_search_mock`, `update_lead_status`, `get_database_summary` to demonstrate capability without external dependencies.
    3.  **Context Management**: Full conversation history support with a **"New Session"** reset feature (backend memory + frontend UI sync).
    4.  **OpenRouter Support**: Configured to work seamlessly with `openai/gpt-4o-mini` and custom base URLs.

## 📋 Task Breakdown & Status

### 1. Technology & Architecture ✅
- [x] Finalize Tech Stack.
- [x] Initialize Git Repository.

### 2. Data Preparation (Leads) ✅
- [x] Define Schema with "BDR Utility" focus.
- [x] Generate 10 real companies data.

### 3. Web App Design & UI ✅
- [x] **Layout:** Split View (Table + Detail Panel).
- [x] **AI Console:** **55vh Height**, CLI-style stream, Session Sidebar.
- [x] **Interactive:** Real-time search, sorting, filtering.

### 4. Agentic Capabilities ✅
- [x] **Core Engine:** Implemented `AgentRuntime` with ReAct loop.
- [x] **Tool System:** Created `ToolRegistry` for easy tool addition.
- [x] **BDR Tools:** Implemented `update_status`, `search` (mock), `get_details`.
- [x] **API Integration:** Connected Frontend Terminal to Backend Agent.
- [x] **Session Management:** Implemented "Reset Memory" functionality.

## 📝 Presentation Key Points
*   **"I built an Agent Runtime, not just a Chatbot."** (Mention the ReAct loop and Tool Registry).
*   **"Designed for Live Coding."** (Show how easily you can add a new tool in `agent_service.py`).
*   **"Human-in-the-loop."** (The UI allows the BDR to verify the Agent's work immediately).
