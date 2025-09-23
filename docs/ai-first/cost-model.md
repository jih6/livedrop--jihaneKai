# Cost Model for Selected AI Touchpoints

## 1. Support Assistant / Chatbot

### Assumptions
- Model: GPT-4o-mini at $0.15 / 1K prompt tokens, $0.60 / 1K completion tokens
- Avg tokens in: 50
- Avg tokens out: 100
- Requests/day: 1,000
- Cache hit rate: 30%
- Multi-language support: English, Arabic, French (minor overhead assumed negligible)

### Calculation

**Formula:**  
Cost/action = (tokens_in / 1000 * prompt_price) + (tokens_out / 1000 * completion_price)
Daily cost = Cost/action * Requests/day * (1 - cache_hit_rate)


**Step-by-step:**  
Cost/action = (50 / 1000 * 0.15) + (100 / 1000 * 0.60)
= 0.0075 + 0.06
= 0.0675 ≈ $0.068 per query

Daily cost = 0.0675 * 1,000 * (1 - 0.3)
= 0.0675 * 1,000 * 0.7
= 47.25 ≈ $47/day


### Results
- Support Assistant / Chatbot: Cost/action = $0.068, Daily = $47

### Cost Lever if Over Budget
- Shorten context tokens for Support Assistant  
- Reduce output tokens  
- Use cheaper model for low-risk paths  

---

## 2. Typeahead Search Suggestions

### Assumptions
- Model: GPT-4o-mini at $0.15 / 1K prompt tokens, $0.60 / 1K completion tokens
- Avg tokens in: 5
- Avg tokens out: 20
- Requests/day: 50,000
- Cache hit rate: 70%
- Multi-language support: English, Arabic, French (minor overhead assumed negligible)

### Calculation

**Formula:**  
Cost/action = (tokens_in / 1000 * prompt_price) + (tokens_out / 1000 * completion_price)
Daily cost = Cost/action * Requests/day * (1 - cache_hit_rate)

**Step-by-step:**  

Cost/action = (5 / 1000 * 0.15) + (20 / 1000 * 0.60)
= 0.00075 + 0.012
= 0.01275 ≈ $0.013 per query

Daily cost = 0.01275 * 50,000 * (1 - 0.7)
= 0.01275 * 50,000 * 0.3
= 191.25 ≈ $191/day

### Results
- Typeahead Search Suggestions: Cost/action = $0.013, Daily = $191


### Cost Lever if Over Budget
- Reduce output tokens for Typeahead  
- Use caching more aggressively  
- Use cheaper model for low-risk paths
