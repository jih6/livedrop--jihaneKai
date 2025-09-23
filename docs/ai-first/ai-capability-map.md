| Capability | Intent (user) | Inputs (this sprint) | Risk 1–5 (tag) | p95 ms | Est. cost/action | Fallback | Selected |
|---|---|---|---|---:|---|---|:---:|
| Typeahead search suggestions | Quickly find products while typing | Partial search text, optional past searches | 2 | 245 | $0.002 | Simple prefix match or cached top products | Yes |
| Support assistant / chatbot | Ask order or policy questions | User query, order-status API, FAQ markdown | 3 | 1100 | $0.01 | Return FAQ only or escalate to human agent | Yes |
| Cart upsell / cross-sell suggestions | Suggest complementary items in cart | Cart contents, browsing history | 3 | 450 | $0.004 | No suggestion displayed | No |
| Dynamic pricing hints | Suggest optimal price adjustments | SKU price, inventory, historical sales | 4 | 500 | $0.005 | Keep current price | No |
| Fraud detection | Flag suspicious orders | Order info, IP, payment info | 4 | 600 | $0.003 | Manual review by team | No |
| Image-based product search | Find products via uploaded images | Uploaded image, product catalog images | 3 | 700 | $0.006 | Fallback to text search | No |

## Why we selected these two

We selected “Typeahead search suggestions” and “Support assistant / chatbot” because they directly improve user experience and measurable KPIs. Typeahead search increases product discoverability and conversion by helping users find products quickly. The support assistant reduces support contacts and improves satisfaction by answering order and policy questions efficiently. Both features have low to moderate risk, are feasible with current ShopLite data, and can be integrated without impacting system stability.
