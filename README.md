# 🌌 SEO Polaris

SEO Polaris is a premium SEO intelligence and search analytics platform built for internal company use, modeled after modern tools like SEO Gets. 

The platform leverages Google Search Console (GSC) and Google Analytics 4 (GA4) data to separate branded traffic bias, pinpoint high-value striking distance ranking opportunities, and track page performance decay over time.

---

## 🚀 Key Features

### 1. Interactive Core Dashboard (PoC Frontend)
*   **KPI Metrics**: Tracks Clicks, Impressions, CTR, and Position with period-over-period (PoP) comparison rates.
*   **Dual-Axis Trends**: Interactively plots Daily Clicks vs. Average Rank Position (using Plotly graph overlays).
*   **Device & Regional Share**: Displays click segments and traffic country leaderboards.

### 2. Search Intelligence Hub
*   **Striking Distance Optimizer**: Identifies queries ranking in positions 4–15 (page 2 or bottom of page 1) and calculates estimated **Click Potential** uplift.
*   **Content Decay Alert Engine**: Highlights decaying landing pages experiencing systematic drops in traffic over time.
*   **Device CTR Discrepancies**: Maps Device CTR side-by-side with Position to identify mobile viewport display issues or layout truncations.

### 3. Production Architecture Foundations (Phase 1 Backend)
*   **FastAPI Engine**: Scalable REST API backend with health checks and OpenAPI docs.
*   **SQLAlchemy DB Modeling**: Structured schema tracking sites, queries, pages, daily charts, and GA4 page conversion analytics.

---

## 📁 Repository Structure

```text
seo-polaris/
├── App/                        # Streamlit PoC Frontend Application
│   └── dashboard.py            # Dashboard UI and visual charts
├── backend/                    # FastAPI Backend Application (Phase 1)
│   ├── app/
│   │   ├── main.py             # Server entrypoint
│   │   ├── core/               # App config and database connection managers
│   │   └── models/             # SQLAlchemy ORM model schemas
│   └── requirements.txt        # Backend dependencies list
├── docs/                       # Strategic plans and PRD playbooks
│   ├── product_requirements.md  # System product spec details
│   └── backend_architecture.md # SQL database definitions
├── Data/                       # Local excel datastores (git-ignored)
└── requirements.txt            # Frontend python requirements
```

---

## 🛠️ Getting Started

### Prerequisites
*   Python 3.10 or higher
*   Virtual environment (`venv`) activated

### Running the Streamlit Frontend PoC
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Place your GSC export Excel file in `Data/whistle_data.xlsx` or upload it directly through the UI.
3. Run the application:
   ```bash
   streamlit run App/dashboard.py
   ```
4. Access the dashboard at `http://localhost:8501`.

### Running the FastAPI Backend
1. Install backend dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
2. Start the development server using uvicorn:
   ```bash
   uvicorn backend.app.main:app --reload --port 8000
   ```
3. Open the interactive OpenAPI documentation at `http://localhost:8000/docs`.