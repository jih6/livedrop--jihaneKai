# RAG System Evaluation

## Retrieval Quality Tests (10 tests)
| Test ID | Question | Expected Documents | Pass Criteria |
|---------|----------|-------------------|---------------|
| R01 | How do I create a seller account on Shoplite? | Document 9: Seller Account Setup and Management | Retrieved docs include Document 9 |
| R02 | What are Shoplite's return policies and how do I track my order? | Document 7: Return and Refund Policies; Document 5: Order Placement & Tracking | Retrieved docs include both Document 7 and Document 5 |
| R03 | How can I apply promotional codes at checkout? | Document 16: Promotional Codes and Discounts | Retrieved docs include Document 16 |
| R04 | What payment methods does Shoplite support? | Document 6: Payment Methods and Security | Retrieved docs include Document 6 |
| R05 | How do sellers manage their inventory? | Document 10: Inventory Management for Sellers | Retrieved docs include Document 10 |
| R06 | How can I leave a review for a product? | Document 8: Product Reviews and Ratings | Retrieved docs include Document 8 |
| R07 | What steps are needed to reset my password? | Document 1: User Registration Process | Retrieved docs include Document 1 |
| R08 | How do I track my order status in the mobile app? | Document 5: Order Placement & Tracking; Document 13: Mobile App Features | Retrieved docs include both Document 5 and Document 13 |
| R09 | How does Shoplite protect user privacy? | Document 15: Security and Privacy Policies | Retrieved docs include Document 15 |
| R10 | How does Shoplite charge commission to sellers? | Document 11: Commission and Fee Structure | Retrieved docs include Document 11 |

## Response Quality Tests (15 tests)  
| Test ID | Question | Required Keywords | Forbidden Terms | Expected Behavior |
|---------|----------|-------------------|-----------------|-----------------|
| Q01 | How do I create a seller account on Shoplite? | ["seller registration", "business verification", "2-3 business days"] | ["instant approval", "no verification required"] | Direct answer with citation to Document 9 |
| Q02 | What are Shoplite's return policies and how do I track my order? | ["30-day return window", "return authorization", "order tracking"] | ["no returns accepted", "lifetime returns"] | Multi-source synthesis from Documents 7 & 5 |
| Q03 | How can I apply promotional codes at checkout? | ["apply promo code", "discount", "checkout"] | ["automatic discount", "no code required"] | Step-by-step answer referencing Document 16 |
| Q04 | What payment methods does Shoplite support? | ["credit card", "PayPal", "security"] | ["unsupported methods", "cash on delivery"] | Direct answer with citation to Document 6 |
| Q05 | How do sellers manage their inventory? | ["inventory update", "stock levels", "product listing"] | ["manual tracking only", "no updates allowed"] | Direct answer citing Document 10 |
| Q06 | How can I leave a review for a product? | ["product review", "rating", "feedback"] | ["fake reviews", "anonymous only"] | Direct answer citing Document 8 |
| Q07 | What steps are needed to reset my password? | ["password reset", "email verification", "security"] | ["password guessing", "default password"] | Direct answer citing Document 1 |
| Q08 | How do I track my order in the mobile app? | ["order tracking", "mobile app", "status update"] | ["tracking not available", "desktop only"] | Multi-source synthesis from Documents 5 & 13 |
| Q09 | How does Shoplite protect user privacy? | ["privacy policy", "data protection", "encryption"] | ["data sharing without consent", "unsecured data"] | Direct answer citing Document 15 |
| Q10 | How does Shoplite charge commission to sellers? | ["commission", "fee structure", "percentage"] | ["no fees", "hidden charges"] | Direct answer citing Document 11 |
| Q11 | How do I register as a buyer on Shoplite? | ["buyer account", "registration", "verification email"] | ["seller registration", "instant approval"] | Direct answer citing Document 1 |
| Q12 | Can I return an item purchased from multiple sellers? | ["return policy", "multi-seller", "authorization"] | ["no returns", "lifetime returns"] | Multi-source synthesis from Document 7 |
| Q13 | What are the steps to add a new product as a seller? | ["product listing", "add item", "inventory management"] | ["no approval", "instant listing"] | Step-by-step instructions citing Documents 4 & 9 |
| Q14 | How do I redeem a promotional code on the mobile app? | ["promo code", "redeem", "mobile app"] | ["code not required", "automatic discount"] | Step-by-step answer citing Documents 16 & 13 |
| Q15 | What security measures are in place for payments? | ["encryption", "secure checkout", "payment verification"] | ["insecure payments", "no verification"] | Direct answer citing Document 6 |

## Edge Case Tests (5 tests)
| Test ID | Scenario | Expected Response Type |
|---------|----------|----------------------|
| E01 | Question not in knowledge base | Refusal with polite explanation: "I’m sorry, this topic is not covered in the Shoplite documentation." |
| E02 | Ambiguous question | Clarification request: "Could you please clarify your question?" |
| E03 | Question contains conflicting information | Identify inconsistencies and explain using only the available Shoplite documentation; request clarification if unresolved |
| E04 | Question asks for personal advice or speculation | Refusal: "I cannot provide advice beyond the Shoplite documentation." |
| E05 | Question includes typos or partial words | Attempt to interpret the question using context from documents; if still unclear, request clarification politely |
