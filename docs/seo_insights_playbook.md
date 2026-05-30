# SEO Polaris: Product Manager Insights Playbook

This playbook outlines the core intelligence insights that can be extracted from the Google Search Console (GSC) datasets: **Queries, Pages, Countries, and Devices**. 

---

## 1. Striking Distance Opportunity Detection

### Why It Matters
*   **The Concept**: Identifies queries ranking in positions 4–15 (bottom of page 1 or top of page 2) that already have high impressions but low click-through rates.
*   **Business Impact**: It is significantly easier to move a page from position 8 to position 4 than from position 80 to 8. Boosting these high-impression "striking distance" queries yields the fastest, highest-ROI traffic increases.

### How to Visualize
*   **Bubble Scatter Plot**: 
    *   **X-axis**: Average Position (inverted, so position 1 is on the far right).
    *   **Y-axis**: CTR (%).
    *   **Bubble Size**: Impressions (representing search volume potential).
*   **Interpretation**: The target opportunities appear as large bubbles in the bottom-middle quadrant (Position 4–15, low CTR, high volume).

### How SEO Gets Presents It
*   **The "Opportunities" Hub**: SEO Gets segments these queries into a dedicated tab, calculating a **"Click Potential" index** (e.g., *"If you move this from #11 to #3, you will gain +1,200 clicks/month"*).
*   It highlights them with visual tags and suggests optimizing title tags and meta descriptions.

---

## 2. Brand vs. Non-Brand Split Analysis

### Why It Matters
*   **The Concept**: Separates brand-name queries (e.g., "Whistle aligners") from generic industry queries (e.g., "clear teeth aligners price").
*   **Business Impact**: Branded search traffic is driven by offline marketing, PR, and word-of-mouth. Non-branded traffic measures actual search engine optimization success and new customer acquisition. If brand traffic dominates, the site is vulnerable to brand fatigue and has a narrow organic funnel.

### How to Visualize
*   **Stacked Area Chart / Split Donut**:
    *   An area chart showing total clicks over time, split into two colored bands (Brand vs. Non-Brand).
    *   A high-level ratio indicator (e.g., "75% Non-Brand / 25% Brand").

### How SEO Gets Presents It
*   **Instant Global Toggle**: SEO Gets features a prominent header toggle: **[Show Brand] / [Exclude Brand]**. Clicking it filters the entire dashboard on the fly, showing how the website ranks when brand equity is removed.

---

## 3. Mobile vs. Desktop CTR Discrepancy

### Why It Matters
*   **The Concept**: Compares the click-through rates of identical rankings across desktop and mobile devices.
*   **Business Impact**: If a landing page ranks #2 on both mobile and desktop, but mobile CTR is 4% while desktop CTR is 12%, this flags a critical issue. The mobile SERP layout may truncate the title tag, mobile page load speed may be causing bounces, or the layout might look broken on smaller screens.

### How to Visualize
*   **Slope Graph or Split Column Chart**:
    *   Compare CTR for top-volume pages side-by-side. A line connecting the mobile CTR and desktop CTR quickly exposes steep drops.

### How SEO Gets Presents It
*   **In-line Device Split**: When expanding a specific page's metrics in SEO Gets, it reveals a mini device scorecard inline (Mobile vs. Desktop icons with traffic share percentages and respective CTRs) instead of burying device data on a separate page.

---

## 4. Content Decay & Performance Loss

### Why It Matters
*   **The Concept**: Tracks pages that have experienced a steady decline in clicks, impressions, or rank over consecutive periods (e.g., WoW or MoM).
*   **Business Impact**: Content gets outdated or outcompeted. Detecting decay early allows content teams to refresh pages, update stats, or add internal links before rankings collapse entirely.

### How to Visualize
*   **Heatmap Matrix / Slope Charts**:
    *   A list of pages sorted by **Absolute Clicks Lost** compared to the prior period.
    *   A small red sparkline representing the downward trajectory.

### How SEO Gets Presents It
*   **The "Decay Report"**: SEO Gets has a specialized dashboard view displaying pages experiencing systematic loss. It highlights the "loss slope" and lists the specific queries that have dropped in position for each decayed page.

---

## 5. Geographical CTR & Localization Arbitrage

### Why It Matters
*   **The Concept**: Analyzes search volume and CTR by country to identify where international audiences are searching for your content but clicking less.
*   **Business Impact**: High impressions in a foreign country with low CTR indicates a language mismatch or lack of localized pricing/currency in title snippets. This flags opportunities to spin up localized landing pages (e.g., `/en-gb/` or `/en-ca/`).

### How to Visualize
*   **Interactive Choropleth (World Map)**:
    *   Countries colored by Click Volume.
    *   Hovering shows localized CTR and average position compared to the primary country.

### How SEO Gets Presents It
*   **Geographic Segment Cards**: Presents country performance as a clean leaderboard with flags. Allows the user to click any country to filter all keywords and pages for that specific regional search engine.
