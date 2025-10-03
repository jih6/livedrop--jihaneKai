# Ground Truth Q&A for RAG System

---

### Q01: How do I register as a new buyer on Shoplite?
**Expected retrieval context:** Document 1: User Registration Process  
**Authoritative answer:** To register as a buyer, go to the registration page, provide your email, set a password, complete email verification, and optionally link payment methods.  
**Required keywords in LLM response:** ["buyer registration", "email verification"]  
**Forbidden content:** ["instant access without verification"]

### Q02: What steps are required to verify a creator account?
**Expected retrieval context:** Document 3: Creator Account Setup and Verification  
**Authoritative answer:** Creators must submit business documentation, verify their identity, and await approval. Access is granted once all documents are validated.  
**Required keywords in LLM response:** ["business verification", "document upload", "access granted"]  
**Forbidden content:** ["automatic approval", "no verification required"]

### Q03: How can a customer track the status of an order?
**Expected retrieval context:** Document 5: Order Placement & Tracking  
**Authoritative answer:** Customers can view real-time updates via the order tracking page, including shipping status, expected delivery, and any delays.  
**Required keywords in LLM response:** ["order tracking", "shipping status", "expected delivery"]  
**Forbidden content:** ["no tracking available", "manual updates only"]

### Q04: What are the return and refund policies on Shoplite?
**Expected retrieval context:** Document 7: Return and Refund Policies  
**Authoritative answer:** Returns are allowed within 30 days of delivery if the product is unused. Refunds are processed after return approval, typically within 5-7 business days.  
**Required keywords in LLM response:** ["30-day return window", "refund processed", "unused product"]  
**Forbidden content:** ["no returns allowed", "instant refund without return"]

### Q05: What are Shoplite's supported payment methods and security measures?
**Expected retrieval context:** Document 6: Payment Methods and Security  
**Authoritative answer:** Shoplite supports credit/debit cards, digital wallets, and bank transfers. All payment data is encrypted, PCI compliant, and error handling ensures failed transactions are retried safely.  
**Required keywords in LLM response:** ["credit/debit cards", "PCI compliance", "encryption"]  
**Forbidden content:** ["unsecured payments", "instant payout without verification"]

### Q06: How does Shoplite prevent abuse in product reviews?
**Expected retrieval context:** Document 8: Product Reviews and Ratings  
**Authoritative answer:** Shoplite moderates reviews, enforces content guidelines, and prevents spam or fraudulent ratings using automated detection and manual review.  
**Required keywords in LLM response:** ["moderation", "prevent abuse", "content guidelines"]  
**Forbidden content:** ["all reviews are published without checks", "fake reviews allowed"]

### Q07: What security measures are applied to user accounts?
**Expected retrieval context:** Document 2: User Login and Authentication + Document 15: Security and Privacy Policies  
**Authoritative answer:** Shoplite uses strong password policies, multi-factor authentication, JWT sessions, encrypted storage, and access control to protect user accounts.  
**Required keywords in LLM response:** ["MFA", "encryption", "access control"]  
**Forbidden content:** ["password only security", "unencrypted storage"]

### Q08: How can a seller update inventory and receive low-stock alerts?
**Expected retrieval context:** Document 10: Inventory Management for Sellers  
**Authoritative answer:** Sellers can adjust stock levels through their dashboard. Low-stock thresholds trigger notifications, and updates are reflected in real-time across all listings.  
**Required keywords in LLM response:** ["inventory update", "low-stock alerts", "dashboard"]  
**Forbidden content:** ["manual sync required", "no notifications"]

### Q09: How do I create a seller account on Shoplite?
**Expected retrieval context:** Document 9: Seller Account Setup and Management  
**Authoritative answer:** To create a seller account, visit the Shoplite seller registration page, provide business information including tax ID, and complete the verification process which takes 2-3 business days.  
**Required keywords in LLM response:** ["seller registration", "business verification", "2-3 business days"]  
**Forbidden content:** ["instant approval", "no verification required", "personal accounts"]

### Q10: How are API requests authenticated and rate-limited?
**Expected retrieval context:** Document 14: API Documentation for Developers  
**Authoritative answer:** API requests require token-based authentication. Rate-limits prevent excessive requests, and endpoints respond with standard error codes if limits are exceeded.  
**Required keywords in LLM response:** ["token authentication", "rate-limit", "error codes"]  
**Forbidden content:** ["unauthenticated access", "no rate-limiting"]

### Q11: How can I apply a promotional code at checkout?
**Expected retrieval context:** Document 16: Promotional Codes and Discounts  
**Authoritative answer:** Customers enter the promo code at checkout. The system validates eligibility, applies the discount, and enforces rules like expiration or one-time use.  
**Required keywords in LLM response:** ["promo code", "eligibility", "discount applied"]  
**Forbidden content:** ["automatic discount without code", "expired code accepted"]

### Q12: What are the GDPR requirements for handling user data in Shoplite?
**Expected retrieval context:** Document 17: GDPR / Regional Compliance  
**Authoritative answer:** Shoplite must obtain explicit consent, store data securely, provide user access and deletion rights, maintain a cookie policy, and limit data retention according to regulations.  
**Required keywords in LLM response:** ["explicit consent", "data retention", "cookie policy"]  
**Forbidden content:** ["store data indefinitely without consent", "ignore user deletion requests"]

### Q13: How do buyer and creator registration processes differ?
**Expected retrieval context:** Document 1: User Registration Process + Document 3: Creator Account Setup and Verification  
**Authoritative answer:** Buyers provide basic information and email verification, while creators must submit business documentation, undergo verification, and await approval before accessing creator features.  
**Required keywords in LLM response:** ["buyer registration", "creator verification", "business documentation"]  
**Forbidden content:** ["same process for both", "no verification for creators"]

### Q14: How can customers track orders and return products simultaneously?
**Expected retrieval context:** Document 5: Order Placement & Tracking + Document 7: Return and Refund Policies  
**Authoritative answer:** Customers can track order status via the tracking page. If eligible for a return, they can initiate it online, obtain return authorization, and track refund processing alongside shipment tracking.  
**Required keywords in LLM response:** ["order tracking", "return authorization", "refund processing"]  
**Forbidden content:** ["no tracking for returns", "returns accepted without eligibility check"]

### Q15: What are the mobile app features for offline browsing and notifications?
**Expected retrieval context:** Document 13: Mobile App Features  
**Authoritative answer:** The app caches listings and user data for offline browsing. Push notifications alert users about drops, orders, or promotions, and changes sync when the device reconnects.  
**Required keywords in LLM response:** ["offline caching", "push notifications", "sync"]  
**Forbidden content:** ["no offline support", "notifications not working"]

### Q16: How does Shoplite handle multi-factor authentication during login?
**Expected retrieval context:** Document 2: User Login and Authentication + Document 15: Security and Privacy Policies  
**Authoritative answer:** Users enable MFA, receive a one-time code via email or SMS, and must enter it after their password to complete login. This ensures enhanced account security.  
**Required keywords in LLM response:** ["MFA", "one-time code", "enhanced security"]  
**Forbidden content:** ["password only login", "MFA optional without notice"]

### Q17: What is the commission and fee structure for sellers?
**Expected retrieval context:** Document 11: Commission and Fee Structure  
**Authoritative answer:** Shoplite charges a percentage-based commission on sales, deducts platform fees during payout, and provides detailed reports of all transactions and fees.  
**Required keywords in LLM response:** ["commission", "platform fees", "transaction reports"]  
**Forbidden content:** ["no fees", "hidden charges"]

### Q18: How does Shoplite manage product drops and inventory scheduling?
**Expected retrieval context:** Document 4: Product / Drop Management + Document 10: Inventory Management for Sellers  
**Authoritative answer:** Sellers schedule product drops with inventory levels. The platform ensures stock consistency, updates listings in real-time, and prevents overselling during live drops.  
**Required keywords in LLM response:** ["product drops", "inventory scheduling", "real-time updates"]  
**Forbidden content:** ["overselling allowed", "no scheduling"]

### Q19: How can customer support tickets be escalated if unresolved?
**Expected retrieval context:** Document 12: Customer Support Procedures  
**Authoritative answer:** Tickets can be escalated according to priority levels and SLA timelines. Higher-level support or management intervenes if resolution exceeds defined thresholds.  
**Required keywords in LLM response:** ["ticket escalation", "SLA", "priority levels"]  
**Forbidden content:** ["no escalation process", "tickets ignored"]

### Q20: How does Shoplite ensure international GDPR compliance for user data transfers?
**Expected retrieval context:** Document 17: GDPR / Regional Compliance  
**Authoritative answer:** Shoplite applies data transfer mechanisms like standard contractual clauses, conducts risk assessments, encrypts data in transit, and informs users about cross-border data handling.  
**Required keywords in LLM response:** ["standard contractual clauses", "encrypted data", "cross-border transfer"]  
**Forbidden content:** ["unregulated international transfers", "user data shared without notice"]
