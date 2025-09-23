# AI Touchpoints Specifications

This document describes the **implementation details** for the two selected AI touchpoints for ShopLite: **Typeahead Search Suggestions** and **Support Assistant / Chatbot**.

---

## 1. Typeahead Search Suggestions

### Problem Statement
Users often struggle to find products quickly, especially with 10k SKUs in ShopLite. Typeahead search reduces search time, increases product discoverability, and improves conversion rates by suggesting relevant products as the user types.

### Happy Path (6–10 steps)
1. User starts typing a query in the search bar.
2. Frontend sends partial query to the backend search API.
3. Backend queries Elasticsearch for candidate SKUs.
4. AI model ranks suggestions based on query, past searches, and popularity.
5. Backend applies caching for frequently requested prefixes.
6. Suggestions are sent back to the frontend.
7. Frontend displays suggestions in a dropdown list.
8. User clicks a suggestion → navigates to product page.
9. Interaction logged for analytics (click-through and conversion tracking).

### Grounding & Guardrails
- AI suggestions grounded on **ShopLite product catalog via Elasticsearch**.  
- Max context: last 10 characters typed.  
- Refuses to suggest products not in catalog or discontinued items.  
- Only returns **indexed and live SKUs** from Elasticsearch.  
- Supports multiple languages: **English, Arabic, French**. Suggestions are matched to the language of the query.

### Human-in-the-loop
- Minimal human intervention needed.  
- Product team reviews analytics weekly to detect irrelevant suggestions.  
- UI surface: “Did you mean…” corrections if AI fails consistently.

### Latency Budget
- Elasticsearch query: 70 ms  
- AI ranking / prediction: 130 ms  
- Caching / filtering: 20 ms  
- Frontend render: 25 ms  
**Total:** ≤245 ms p95 (meets target)

### Error & Fallback Behavior
- If AI or Elasticsearch fails, fallback to **cached top products** or simple prefix match.  
- Users still see suggestions, ensuring search remains functional.

### PII Handling
- No personally identifiable information leaves ShopLite.  
- Queries logged masked for analytics.  
- No order history or payment details included.

### Success Metrics
- Product Metric 1: Click-through rate (CTR) on suggestions  
  Formula: CTR (%) = (Number of clicks on suggestions / Number of times suggestions shown) * 100
  *Measures how often users select AI suggestions, indicating relevance.*

- Product Metric 2: Average time-to-find product  
  Formula: Avg time-to-find (seconds) = Sum of (time from first keypress to product page click) / Number of searches
  *Tracks efficiency of search, aiming to reduce time from query to product page.*

- Business Metric: Conversion rate increase (%)  
  Formula: Conversion rate (%) = (Number of purchases / Number of sessions with AI suggestions) * 100
  *Shows impact of AI suggestions on actual sales.*

### Feasibility Note
- Stock Keeping Unit (SKU) catalog is indexed in Elasticsearch.  
- Backend API supports query endpoints.  
- Next step: implement AI ranking prototype, integrate with Elasticsearch, and measure latency with real traffic.

---

## 2. Support Assistant / Chatbot

### Problem Statement
Users frequently have questions about orders, shipping, or policies. A support assistant reduces support load, provides instant answers, and improves customer satisfaction.

### Happy Path (6–10 steps)
1. User opens the support chat interface.  
2. User types a question (e.g., “Where is my order?”).  
3. Frontend sends query to backend API.  
4. Backend forwards query to AI model with context from **FAQ markdown** and **order-status API**.  
5. Model returns answer with confidence score.  
6. Backend checks confidence; if low, escalates to human agent.  
7. Frontend displays AI answer to the user.  
8. User optionally confirms answer or asks follow-up.  
9. Interaction logged for analytics and future model improvement.

### Grounding & Guardrails
- AI grounded on **ShopLite FAQ and order-status API only**.  
- Maximum context: 2 previous messages.  
- Refuses answers outside ShopLite domain.  
- Supports multiple languages: **English, Arabic, French**. Responses are returned in the language of the user query.  
- Detects and blocks unsafe/jailbreak prompts; refuses to answer malicious or out-of-scope requests.

### Human-in-the-loop
- Escalation triggered if confidence < 70%.  
- Human agent receives notification and responds within 1 hour.  
- UI indicates when query is handled by human.

### Latency Budget
- Query preprocessing: 100 ms  
- AI model inference: 800 ms  
- Backend processing / routing: 100 ms  
- Frontend render: 100 ms  
**Total:** ≤1100 ms p95 (meets target)

### Error & Fallback Behavior
- If AI fails or confidence is low: fallback to **static FAQ answers** or human support.  
- Ensures users always get a response.

### PII Handling
- Order numbers partially masked; no sensitive payment info sent to AI.  
- Queries anonymized for logging.  
- Minimal metadata logged for analytics.

### Success Metrics
- Product Metric 1: Average resolution time per query  
  Formula: Avg resolution time (seconds) = Total time to answer / Number of queries
  *Measures how quickly AI provides answers.*

- Product Metric 2: % of queries fully handled by AI  
  Formula: % handled by AI = (Number of queries answered without human intervention / Total queries) * 100
  *Indicates AI effectiveness in resolving user questions.*

- Business Metric: Reduction in support ticket volume (%)  
  Formula: Reduction (%) = ((Baseline tickets - Tickets handled by AI) / Baseline tickets) * 100
  *Shows impact of AI on reducing manual support workload.*

### Feasibility Note
- Data from FAQ markdown and order-status API is available.  
- Next step: prototype AI assistant with limited context, measure latency, and validate responses.
