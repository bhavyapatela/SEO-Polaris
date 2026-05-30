# Product Requirements Document (PRD): SEO Polaris

## 1. Executive Summary & Objectives

SEO Polaris is a custom, internal SEO intelligence platform modeled after modern analytics tools like SEO Gets. The goal is to consolidate Google Search Console (GSC) and Google Analytics 4 (GA4) data to provide actionable search marketing insights, isolate brand-affinity bias, detect content performance decay, and prioritize rank optimization opportunities.

---

## 2. Target Audience & Personas

*   **SEO Manager**: Needs a daily view of search health, ranking shifts, keyword opportunities, and pages showing performance drops.
*   **Content Writer / Strategist**: Looks at decaying pages to prioritize content updates and updates title tags/meta descriptions for "striking distance" keywords.
*   **Executive Leadership**: Wants high-level summary KPIs (Clicks, Impressions, CTR, average Rank position) showing organic growth trends.

---

## 3. Functional Requirements

### 3.1 Data Ingestion & Storage
*   **PoC Phase**: Accept Excel file uploads containing standard GSC export sheets (`Chart`, `Queries`, `Pages`, `Countries`, `Devices`, `Search appearance`).
*   **Production Phase**: Automate daily batch ingestion using GSC and GA4 APIs, storing historical records perpetually in a PostgreSQL database (bypassing GSC's native 16-month limit).

### 3.2 Global Brand Segmentation
*   **Filter Engine**: The system must offer a global switch to toggle between **Branded**, **Generic (Non-Brand)**, and **All** traffic.
*   **Rule Engine**: Users must be able to specify custom brand keywords (e.g., "whistle") in the configuration. The platform will automatically classify any query containing these strings as "Branded."

### 3.3 Interactive Performance Trends
*   **KPI Cards**: Expose Clicks, Impressions, CTR, and Average Position with period-over-period (PoP) comparison rates (e.g., comparing selected 30 days to the preceding 30 days).
*   **Dual-Axis Visualization**: Display Clicks (primary axis) and Average Position (secondary inverted axis, rank 1 at the top) over time to visualize correlation.
*   **Dimension Splits**: Side-by-side device click share (mobile vs. desktop) and top traffic countries ranked by CTR.

### 3.4 Search Intelligence Reports
*   **Striking Distance Optimizer**: 
    *   Filter keywords ranking in positions 4–15.
    *   Expose **Click Potential** using benchmark click curves to project potential click gains if rankings improve.
*   **Content Decay Alert**:
    *   Flag landing pages showing negative click trajectories when comparing the second half of a date range vs. the first half.
*   **Device CTR Analysis**:
    *   Compare CTR side-by-side with Average Position across Mobile, Desktop, and Tablet to diagnose device-specific display or usability issues.

---

## 4. Non-Functional Requirements

### 4.1 Design & User Experience (UX)
*   **Premium Visuals**: Utilize Outfit typography, custom dark-theme gradients, and glassmorphic card overlays.
*   **Responsive Layout**: Dashboard widgets must scale gracefully across desktop monitors, tablets, and mobile devices.
*   **Micro-interactions**: Implement smooth hover transitions, click animations, and interactive charts (zoom/hover tooltips) using Plotly/Recharts.

### 4.2 Security & Authentication
*   **OAuth2**: Google API access must use secure Google OAuth credentials.
*   **Access Control**: Ensure internal company usage permissions match domain authorization restrictions.
