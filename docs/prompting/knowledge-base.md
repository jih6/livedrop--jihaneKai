# Knowledge Base for RAG System (15-20 documents)

---

### Document 1:  User Registration Process

Shoplite allows both buyers and creators to register for accounts through a streamlined signup process. Users visit the registration page and are prompted to provide their email address, create a secure password, and fill in basic profile information such as name and contact details. Email verification is required within 24 hours of registration to activate the account, ensuring the authenticity of the user.

For creators, an additional business verification step is required, including providing a valid business license or tax identification number. Only after successful verification can creators run live product drops. Buyers have the option to create a free account with immediate access to browsing and following creators.

**Technical Implementation:**  
- Registration is handled by the **Auth Service**, a stateless microservice issuing JWT tokens on successful registration/login.  
- Passwords are hashed using **bcrypt** before storage in the **Users SQL database**.  
- The Users table is **sharded by region** and **replicated** across multiple nodes for high availability and to prevent bottlenecks during traffic spikes.  
- **Rate-limiting:** Maximum of 5 registrations per IP per hour to prevent abuse.  
- Failed or duplicate registrations are logged and trigger automated alerts.  
- Email verification failures or expired links prompt the system to allow a re-send of the verification email.

**User Guidance:**  
- Click the email verification link within 24 hours.  
- Use a strong password (minimum 8 characters, including letters, numbers, symbols). MFA is recommended for added security.  
- Creators must submit valid business documents; incomplete submissions delay account approval.  
- Password recovery is available through “Forgot Password” with secure token links.  
- For business verification issues, users can contact Shoplite support at support@Shoplite.com.

**Error Handling / Edge Cases:**  
- **Email already registered:** System returns a clear error message with instructions to recover the account.  
- **Abandoned registrations:** Unverified accounts are purged after 7 days.  
- **Verification attempts exceeded:** Users are temporarily blocked and prompted to retry later.  
- **Creator pre-verification login attempts:** Access is restricted until verification completes.  

**Overlap With Other Topics:**  
- Registration integrates with the **User Service** (follow/unfollow, profile management) and the **Notification System** (welcome emails, verification reminders).  
- This overlap ensures that the RAG system can retrieve relevant documents when queries involve multiple components, such as “How do I register and follow a creator?”

**Security Practices:**  
- Enforced password complexity rules and optional MFA.  
- Business verification data is securely stored and accessible only by authorized microservices.  
- Rate-limiting and logging prevent abuse and detect suspicious activity.

**Common Questions / Edge Cases:**  
- Can a creator register before verification? No, they must complete business verification first.  
- What happens to abandoned registrations? They are automatically deleted after 7 days.  
- How to recover passwords if verification fails? Use the “Forgot Password” flow.

### Document 2:  User Login and Authentication

The Shoplite login process allows both buyers and creators to securely access their accounts. Users provide their registered email address and password, which is verified against stored credentials in the **Auth Service**. Upon successful authentication, a **JWT token** is issued for session management, valid for a configurable duration (default: 24 hours).

For creators, login access is only granted after **business verification** is completed. Login attempts are monitored to prevent brute-force attacks, and suspicious activity triggers temporary account lockouts.

**Technical Implementation:**  
- Passwords are stored securely using **bcrypt** hashing with unique salts for each user.  
- Auth Service verifies credentials and issues JWTs containing user ID, role (buyer or creator), and expiration timestamp.  
- User sessions are stateless; token verification occurs on each API request.  
- **Rate-limiting:** Max 10 login attempts per IP per hour. Excessive attempts result in a 15-minute lockout.  
- Multi-factor authentication (MFA) can be enabled optionally for creators, requiring a TOTP or SMS code at login.

**Error Handling / Edge Cases:**  
- **Incorrect password:** System returns an informative error without revealing whether the email exists.  
- **Unverified email:** Login is blocked; users prompted to complete verification.  
- **Expired JWT tokens:** Users must re-authenticate to receive a new token.  
- **Locked accounts:** Temporarily blocked users receive guidance via email to unlock.  

**User Guidance:**  
- Use “Forgot Password” for recovery; a secure reset token is sent to the registered email.  
- Creators must ensure business verification is complete to access live drop management features.  
- MFA setup can be configured in account settings for enhanced security.

**Overlap With Other Topics:**  
- Integrates with **Registration Process** (Document 1) and **User Service** (follower/following, profile updates).  
- Overlaps with **Notification System** for login alerts and security notifications.  
- Ensures RAG queries involving login, registration, or account access retrieve consistent context across documents.

**Security Practices:**  
- Rate-limiting and lockouts prevent brute-force attacks.  
- Passwords are hashed with bcrypt; no plaintext storage.  
- MFA is recommended and strongly advised for creator accounts.  
- All JWTs are signed with a secret key and verified at each request.

**Common Questions / Edge Cases:**  
- What if I forget my password? Use the “Forgot Password” flow with secure token email.  
- Can a creator login before verification? No, access is blocked until verification completes.  
- What happens on multiple failed login attempts? Temporary lockout with instructions to retry.

### Document 3:  Creator Account Setup and Verification

Creators on Shoplite must register a dedicated **creator account** to host live drops, manage products, and interact with followers. The setup process ensures authenticity, compliance, and system security.

**Account Setup Process:**  
1. Navigate to the “Become a Creator” page.  
2. Provide required business information: legal business name, tax ID, email, phone number, and bank account details.  
3. Upload identity documents (government ID, business license).  
4. System validates documents automatically and flags incomplete or invalid submissions for manual review.  
5. Upon verification, the account is approved, and creators can access the **Creator Dashboard**.

**Technical Implementation:**  
- Creator data is stored in the **Creator Service**, with sharding by region to ensure scalable access.  
- Verification status is stored in a replicated SQL DB to prevent data loss.  
- Uploads (ID, business license) are stored in **Blob Storage** with secure, signed URLs.  
- **Rate-limiting:** Max 5 account submissions per IP per hour to prevent spam registrations.  
- Verification triggers an asynchronous workflow via **Kafka**, sending approval notifications and enabling system access.

**Error Handling / Edge Cases:**  
- **Incomplete submission:** System prompts the creator to complete missing fields; RAG can retrieve guidance on required fields.  
- **Failed verification:** Notification sent with steps to correct issues.  
- **Duplicate business info:** System checks existing registrations and blocks duplicates.  
- **Network/storage errors:** Uploads retried automatically; manual intervention if repeated failures.

**User Guidance:**  
- Contact support for document issues or manual verification delays.  
- Use recommended formats for uploads (PDF, JPG, max 5MB).  
- Creators cannot participate in drops until verification completes.  

**Overlap With Other Topics:**  
- Connects to **User Login** (Document 2) for authentication.  
- Links to **Product/Drop Management** (Document 4) to enable drop creation.  
- RAG precision benefits from cross-referencing error handling, document submission, and rate-limiting guidance.

**Security Practices:**  
- Sensitive creator documents stored securely with access control.  
- Data transmitted over HTTPS; uploads signed and time-limited.  
- Verification workflow monitored for anomalies and repeated failures.  

**Common Questions / Edge Cases:**  
- Can a creator register multiple accounts? No, duplicate verification blocked.  
- What if verification takes longer than expected? Email notification and support contact instructions.  
- What happens if an ID is rejected? System prompts resubmission with correct documentation.

### Document 4:  Product / Drop Management

The **Product / Drop Service** allows creators to list products, schedule live drops, and manage inventory. It ensures real-time availability, prevents overselling, and provides a smooth user experience.

**Product Listing Workflow:**  
1. Creator accesses the **Creator Dashboard**.  
2. Adds product details: name, description, price, images, inventory count.  
3. Optionally schedules a live drop: start time, quantity, duration.  
4. Product and drop information is stored in the **Product/Drop Service**, normalized in a SQL database with indexing for fast retrieval.  
5. Inventory levels are mirrored in **Redis cache** for low-latency stock reads during live drops.  

**Technical Implementation:**  
- **ACID transactions** ensure stock integrity when multiple users place orders simultaneously.  
- **Distributed locks** prevent overselling during high-concurrency drops.  
- **Sharding** of products by creator ID ensures scalable access patterns.  
- Asynchronous events (via Kafka) notify **Order Service** of sold-out status, and trigger push notifications to followers.  
- Drop metadata and product images stored in **Blob Storage/CDN** for fast delivery.  

**Error Handling / Edge Cases:**  
- **Inventory mismatch:** System checks stock before confirming orders; insufficient stock triggers user notification.  
- **Failed image upload:** Retry mechanism with error logging; alerts creator if repeated failures occur.  
- **Drop time conflicts:** System prevents overlapping drops for the same creator.  
- **Network/DB errors:** Automatic retries; manual admin intervention if persistent.  

**User Guidance:**  
- Creators must ensure accurate inventory counts.  
- Recommended image formats: JPG, PNG, max 5MB.  
- Drops cannot start if inventory is zero or verification pending.  

**Overlap With Other Topics:**  
- Connects to **Creator Account Setup** (Document 3) for verified creator status.  
- Links to **Order Service** (Document 5) for live drop fulfillment.  
- References **Redis caching** and **distributed locks** (performance / scaling context).  

**Security Practices:**  
- Only verified creators can schedule drops.  
- Access control ensures creators can only modify their products.  
- Blob Storage URLs signed and time-limited to prevent unauthorized access.  

**Common Questions / Edge Cases:**  
- What happens if a drop sells out instantly? Real-time stock updates prevent overselling; users see sold-out status.  
- Can a product be edited after scheduling? Only pre-drop edits allowed; during live drop, edits are blocked.  
- What if Redis cache fails? Fallback to SQL reads; slightly higher latency but consistent inventory.

### Document 5:  Order Placement & Tracking

The **Order Service** handles all aspects of placing, confirming, and tracking orders during live drops. It ensures data consistency, prevents duplicate orders, and provides real-time updates to users.

**Order Placement Workflow:**  
1. User selects products from a live drop and adds them to the cart.  
2. The system validates stock availability from **Redis cache** and SQL database.  
3. Generates a unique **idempotency key** for each order to prevent duplicates.  
4. User confirms payment via supported **payment methods** (credit card, digital wallet, etc.).  
5. Order is committed in an **ACID transaction** to guarantee stock deduction and order integrity.  
6. Async events are published to **Kafka/RabbitMQ** for notifications, analytics, and inventory updates.  
7. User receives a confirmation with estimated delivery time and tracking link.  

**Technical Implementation:**  
- **Distributed locks** ensure multiple concurrent order attempts do not oversell inventory.  
- **Sharding** by user ID allows horizontal scaling of order processing.  
- **Retry logic** for transient failures in payment gateway or database access.  
- Orders are mirrored in **Redis cache** for fast retrieval in dashboards.  

**Error Handling / Edge Cases:**  
- **Payment failure:** User is notified immediately; stock is released.  
- **Stock mismatch:** Orders fail gracefully; users prompted to adjust quantity.  
- **Duplicate submission:** Idempotency key prevents double-charging or double-ordering.  
- **Network failure:** Transactions rolled back; user prompted to retry.  

**User Guidance:**  
- Users should review cart items carefully before checkout.  
- Estimated delivery times are provided; delays may occur during high-traffic drops.  
- Users can track orders in the **Order Dashboard** or receive notifications via email/app.  

**Overlap With Other Topics:**  
- Links to **Product / Drop Management** (Document 4) for live inventory validation.  
- Connects to **Payment Methods & Security** (Document 6) for secure transactions.  
- References **Redis caching**, distributed locks, and Kafka for performance and reliability.  

**Security Practices:**  
- Sensitive data encrypted at rest and in transit (AES-256, TLS 1.2+).  
- Payment data handled via PCI-compliant gateways; no sensitive data stored locally.  
- Only authenticated users can access their own order information.  

**Common Questions / Edge Cases:**  
- Can a user place multiple orders for the same product? Yes, but stock availability and idempotency checks apply.  
- What happens if payment is delayed? Order is held in a pending state; stock is temporarily reserved.  
- How are order cancellations handled? Within allowed window, cancelled orders release stock and trigger refunds.  

### Document 6:  Payment Methods & Security

The **Payment Service** ensures secure, fast, and reliable processing of user transactions during live drops. It supports multiple payment methods while adhering to strict security and compliance standards.

**Supported Payment Methods:**  
- Credit/Debit Cards (Visa, MasterCard, AMEX)  
- Digital wallets (PayPal, Apple Pay, Google Pay)  
- Bank transfers (selected regions)  
- Promotional codes and discounts applied at checkout  

**Transaction Workflow:**  
1. User selects preferred payment method during checkout.  
2. Payment details are validated locally (format, required fields).  
3. Payment request sent to **PCI-compliant payment gateway**.  
4. Payment gateway response is processed; if approved, order proceeds to **Order Service**.  
5. Failed or declined transactions trigger user notifications and rollback of reserved stock.  
6. Async events sent to **Kafka/RabbitMQ** for analytics and audit logging.  

**Security Implementation:**  
- All sensitive data encrypted in transit (TLS 1.2+) and at rest (AES-256).  
- Payment card information never stored on Shoplite servers.  
- Multi-Factor Authentication (MFA) encouraged for high-value transactions.  
- Tokenization used for recurring payment methods.  
- Fraud detection checks for suspicious activity (geolocation mismatches, velocity checks).  

**Error Handling / Edge Cases:**  
- **Payment declined:** User prompted to retry or select another method.  
- **Network errors:** Transaction rolled back; retries allowed without double-charging.  
- **Invalid promo codes:** Discount rejected, user notified.  
- **Partial payment failures:** System prevents order confirmation until full payment is authorized.  

**User Guidance:**  
- Users should verify card details and ensure sufficient balance.  
- Keep payment methods updated in profile for faster checkout.  
- Contact support immediately if transactions fail repeatedly.  

**Overlap With Other Topics:**  
- Ties to **Order Placement & Tracking** (Document 5) for transactional integrity.  
- References **Auth & User Service** (Document 1) for verified account identity.  
- Connects to **Cart & Checkout Features** (Document 3) for discount and promo code validation.  

**Technical Details:**  
- Retry logic with exponential backoff for transient gateway errors.  
- Audit logs recorded in SQL DB and mirrored in **Redis** for monitoring dashboards.  
- Payment microservice horizontally scalable for high-concurrency live drops.  

**Common Questions / Edge Cases:**  
- Can a user use multiple payment methods for a single order? Not supported; select one.  
- What if the payment succeeds but the order fails? Transaction rollback ensures stock and funds are consistent.  
- How are refunds processed? Triggered via same payment method, asynchronously confirmed via events.  

### Document 7:  Return & Refund Policies

Shoplite provides clear and fair **return and refund policies** to ensure customer trust and compliance with regional consumer protection laws. These policies are integrated directly with the order and payment systems to automate processing.

**Return Eligibility:**  
- Products must be unused and in original condition within **14 days** of delivery.  
- Digital or limited-edition items (e.g., live drop exclusive products) may be **non-returnable**; indicated clearly on the product page.  
- Sellers must approve returns for items not covered by automated rules.

**Refund Workflow:**  
1. User submits a return request via the **Order Service**.  
2. System validates eligibility based on delivery date, item type, and purchase records.  
3. Approved requests trigger a return shipping label (physical products).  
4. Upon receiving the returned product, **Payment Service** processes the refund using the original payment method.  
5. Refund confirmation is sent to the user; audit logs updated asynchronously via **Kafka/RabbitMQ**.  

**Security & Compliance:**  
- Refunds follow strict verification to prevent fraud (e.g., multiple claims for the same order).  
- Only verified accounts (Document 1) can request refunds.  
- Sensitive transaction data is not stored locally, following PCI standards.  

**Error Handling / Edge Cases:**  
- **Late return requests:** Automatically rejected; user notified.  
- **Partial product returns:** Refunds calculated proportionally, stock adjusted.  
- **Failed refund due to payment gateway error:** Retry logic with notifications to support.  
- **Disputed refunds:** Escalation to support team with tracking via audit logs.  

**User Guidance:**  
- Users are encouraged to check the product page for return eligibility before purchase.  
- Support contact provided for non-standard cases or seller disputes.  
- Track refund status in the **Order Service** interface.  

**Overlap With Other Topics:**  
- Integrates with **Payment Methods & Security** (Document 6) to process refunds.  
- References **Order Placement & Tracking** (Document 5) for validating order history.  
- Related to **Product/Drop Service** (Document 4) for stock adjustments.  

**Technical Details:**  
- Return requests validated against **SQL DB** and mirrored in **Redis cache** for performance.  
- Asynchronous event-driven architecture ensures refunds do not block ongoing order placements.  
- Logs stored for at least 6 months to comply with auditing standards.  

**Common Questions / Edge Cases:**  
- Can a user return part of a multi-item order? Yes, system calculates proportional refund.  
- What happens if the product is lost during return shipping? Dispute resolution via support.  
- Are digital products refundable? No, unless explicitly stated on product page.  

### Document 8:  Product Reviews & Ratings

Shoplite allows users to provide **feedback on purchased products** via reviews and ratings, helping future buyers make informed decisions and providing insights to creators.

**Review Submission:**  
- Only **verified buyers** (Document 1) can submit reviews to ensure authenticity.  
- Reviews consist of a **star rating (1-5)** and optional text comments (max 500 characters).  
- Media attachments (images/videos) are stored in **Blob Storage/CDN** and linked to the review record.  

**Moderation & Guardrails:**  
- Automatic profanity filter applied to all text content.  
- Flagged reviews are sent to a **Human-in-the-loop** moderation queue.  
- Duplicate reviews for the same product by the same user are prevented via **unique constraints** in the **SQL DB**.  
- Reviews cannot be edited after **48 hours**, except for correcting typos; changes are logged for audit purposes.  

**Display & Aggregation:**  
- Average rating calculated in real-time and cached in **Redis** for fast retrieval on product pages.  
- Reviews displayed with **most recent first**; pagination implemented via **cursor-based pagination** (Document 5).  
- Star rating summary includes counts of each rating level for transparency.  

**Error Handling / Edge Cases:**  
- **Failed submission due to network error:** Retry logic triggers automatically.  
- **Invalid media upload:** System rejects and notifies user with allowed formats and size limits.  
- **Spam detection:** Multiple low-quality reviews from a single account trigger temporary posting restrictions.  
- **Deleted products:** Associated reviews are marked inactive but retained for auditing.  

**Security & Compliance:**  
- User-identifying information is not exposed publicly.  
- Review data replicated across regions for availability, but GDPR-compliant anonymization applied when required.  

**User Guidance:**  
- Users encouraged to rate all purchased items to improve recommendations.  
- Support contact provided for media upload issues or moderation disputes.  
- Users notified when flagged reviews are approved or rejected.  
- Track refund status in the **Order Service** interface; refunds typically take 3–5 business days to appear in your account.

**Overlap With Other Topics:**  
- Relates to **Order Tracking & Delivery** (Document 5) to validate purchase.  
- Integrates with **Customer Support Procedures** (Document 11) for handling disputes.  
- Media storage overlaps with **Creator Service / Product Media** (Document 4).  

**Technical Details:**  
- Reviews stored in **SQL DB**, indexed by product_id and user_id.  
- Cached aggregates updated asynchronously via **event bus** to prevent performance bottlenecks.  
- Moderation workflow implemented as background tasks in **RabbitMQ/Kafka**.  

**Common Questions / Edge Cases:**  
- Can a user edit a review after 48 hours? Only typos, logged for audit.  
- Are anonymous reviews allowed? No, only verified buyers.  
- What happens if a review violates policy? Flagged for moderation; user notified.  

### Document 9:  Seller Account Setup & Management

Shoplite allows creators to register as sellers to run product drops and manage their inventory. This document covers **seller onboarding, account management, and technical workflows**.

**Seller Registration:**  
- Creators register through the **Seller Registration Page**, providing business info (name, tax ID, bank details).  
- Email verification and **MFA** are required for account activation.  
- Rate limiting applied: **max 5 registrations per IP per hour** to prevent spam.  

**Account Verification:**  
- Business verification performed asynchronously; expected time: **2-3 business days**.  
- Verification status stored in **SQL DB**, sharded by region for scalability.  
- Users notified via email and in-app notifications on verification status changes.  

**Profile Management:**  
- Sellers can manage **profile details**, media, and storefront customization.  
- Media uploaded to **Blob Storage/CDN**; thumbnails generated automatically.  
- Changes logged for **audit trails** and compliance.  

**Inventory & Product Management Integration:**  
- After approval, sellers can create products/drops (see Document 4).  
- Inventory synchronized with **Product/Drop Service**; distributed locks prevent overselling.  
- Stock updates broadcast to **Redis cache** and **event bus** for notifications.  

**Error Handling / Edge Cases:**  
- **Failed verification:** Users receive instructions for resubmission or contacting support.  
- **Duplicate registrations:** System rejects with a descriptive error message.  
- **Incomplete documentation:** Registration cannot proceed until all mandatory fields are provided.  
- **Revoked or suspended accounts:** Sellers cannot create new drops; existing orders remain active.  

**Security & Compliance:**  
- Sensitive data (tax ID, bank info) hashed/encrypted using **bcrypt** or **AES-256** in the DB.  
- MFA enforced for critical actions (creating drops, updating bank info).  
- Activity monitored for suspicious patterns; anomalies trigger admin review.  

**User Guidance:**  
- Creators guided through the registration wizard with tooltips and common troubleshooting tips.  
- Support contact available for verification delays or media upload issues.  
- FAQ includes edge cases: “Can I edit business info after verification?” Answer: Yes, but some changes require re-verification.  
- Support contact available for verification delays or media upload issues.  
- **Average verification time is 2–3 business days**; users are notified via email when verification is complete.

**Overlap With Other Topics:**  
- Links to **Product/Drop Service** (Document 4) for drop creation and stock management.  
- Integrates with **Inventory Management** (Document 10) for stock syncing.  
- Shares user authentication mechanisms with **Auth Service** (Document 2).  

**Technical Details:**  
- Seller data stored in **SQL DB**, sharded by region, replicated for high availability.  
- Media served via CDN; audit logs maintained in **event bus**.  
- Verification workflow uses async tasks in **Kafka/RabbitMQ** to decouple from API latency.  

**Common Questions / Edge Cases:**  
- Can a creator register multiple accounts? No, one account per verified business.  
- What happens if verification fails? User notified; resubmission allowed.  
- Can suspended sellers access their orders? Yes, for audit and fulfillment purposes.  

### Document 10:  Inventory Management for Sellers

Shoplite provides sellers with a robust inventory management system to track, update, and optimize product stock for live drops. This document outlines **inventory workflows, technical integration, and edge cases**.

**Inventory Overview:**  
- Each seller’s products are tracked in the **Inventory Service**, linked to their account.  
- Stock levels are synchronized with the **Product/Drop Service** to ensure accurate availability during live drops.  
- Supports multiple product variants (size, color, limited editions) with separate stock tracking.  

**Stock Updates:**  
- Sellers can **add, remove, or adjust stock** through the dashboard or API.  
- Stock changes trigger **event bus messages** to update **Redis cache** for low-latency reads and notify subscribed users.  
- **Distributed locks** ensure stock cannot be oversold during concurrent order placements.  

**Low Stock & Threshold Alerts:**  
- Sellers can configure **low-stock thresholds**; alerts sent via email or in-app notifications.  
- Integration with analytics allows reporting of popular items and potential restocking needs.  

**Technical Details:**  
- Inventory stored in **SQL DB**, sharded by seller ID, replicated for fault tolerance.  
- Event bus (Kafka/RabbitMQ) ensures asynchronous updates, decoupling inventory changes from API latency.  
- **Cache invalidation** implemented for Redis whenever stock is updated to maintain consistency.  

**Error Handling / Edge Cases:**  
- **Overselling prevention:** Distributed locks prevent negative stock.  
- **Failed updates:** API returns descriptive errors; retry mechanisms available.  
- **Out-of-sync stock:** Background reconciliation job ensures DB, cache, and event bus are consistent.  
- **Product removal:** Cannot remove products with pending orders; must wait until orders are fulfilled.  

**Security & Compliance:**  
- Inventory updates require authenticated sessions via **JWT tokens**.  
- Only verified sellers can modify stock; unauthorized attempts are logged and blocked.  
- Audit logs capture all stock changes, who made them, and timestamp for traceability.  

**User Guidance:**  
- Sellers guided via dashboards with visual stock indicators.  
- Tooltips explain thresholds, variant management, and bulk update procedures.  
- FAQ section includes edge cases: “What happens if two admins update stock simultaneously?” Answer: Distributed locks handle concurrency safely.  

**Overlap With Other Topics:**  
- Linked to **Seller Account Setup** (Document 9) for seller identification.  
- Connected with **Product/Drop Service** (Document 4) for live drop stock accuracy.  
- Shares caching and event bus infrastructure with **Core Microservices** (Documents 2–5).  

**Common Questions / Edge Cases:**  
- Can stock be negative? No, system prevents overselling.  
- How are abandoned carts handled? Stock is returned after cart expiration.  
- Can multiple variants of a product share stock? No, each variant is tracked independently.  

### Document 11:  Commission and Fee Structure

Shoplite applies a transparent commission and fee model for creators and sellers participating in live drops. This document outlines **fee types, calculation methods, technical implementation, and edge cases**.

**Commission Overview:**  
- Shoplite charges a **standard commission percentage** per sale, applied automatically at the time of order completion.  
- Additional fees may include **payment processing fees**, **promotion fees**, or **late listing fees** depending on seller agreements.  
- Commission rates can be tiered based on seller level or volume of sales.

**Fee Calculation:**  
- **Commission = Sale Price × Commission Rate**  
- **Net Seller Earnings = Sale Price − Commission − Payment Fees**  
- Fees are calculated in real-time during checkout and stored in the **Order Service**.  
- Batch reconciliation occurs nightly to ensure all fees are accurately recorded.  

**Technical Details:**  
- **Order Service** records fee components per transaction.  
- Fees stored in SQL DB with replication and sharding by seller ID.  
- Calculations are deterministic; rounding follows standard financial rules (2 decimal places).  
- Event bus messages trigger notifications for both sellers and accounting systems.  

**Edge Cases & Error Handling:**  
- **Refunds / Returns:** Fees are automatically recalculated if an order is partially or fully refunded.  
- **Discounted Orders:** Commission is applied after any promotional discounts.  
- **Multiple Currencies:** Fees are calculated in the order currency; conversion rates applied when transferring earnings to bank accounts.  
- **Failed Payment Processing:** Transactions are rolled back; seller not charged until successful payment.  

**Security & Compliance:**  
- Only authorized finance or accounting services can access fee calculation APIs.  
- Logs of fee calculations are stored for audit and dispute resolution.  
- GDPR-compliant data handling ensures no unauthorized exposure of personal or financial information.  

**User Guidance:**  
- Seller dashboard displays real-time fees and net earnings per sale.  
- FAQs include: “Can I negotiate my commission rate?” (Answer: Only for verified enterprise-level sellers).  
- Notifications are sent when fees are updated or promotional campaigns affect rates.  

**Overlap With Other Topics:**  
- Tied to **Order Service** (Document 5) for transaction integrity.  
- Shares event bus infrastructure with **Inventory Management** (Document 10) for live drop updates.  
- Related to **Payment Methods & Security** (Document 6) for fee collection and settlement.  

**Common Questions / Edge Cases:**  
- Can fees ever be negative? No, system prevents negative commission scenarios.  
- What happens if an order is canceled after payout? Reverse calculation and adjustment performed.  
- Are promotions applied before or after commission? Before, so sellers pay commission on net sales.  


### Document 12:  Customer Support Procedures

Shoplite provides structured support channels to assist users with account issues, order inquiries, refunds, technical problems, and creator-related questions. This document outlines support workflows, escalation paths, system integrations, and edge-case handling.

**Support Channels:**
- **In-App Chat Support:** Real-time chat for logged-in users.
- **Email Support:** `support@Shoplite.com` for non-urgent issues.
- **Help Center / FAQ:** Accessible from app or website, with searchable guides and troubleshooting tips.
- **Phone Support (Optional):** Available during peak drops or promotional events.

**Ticket Workflow:**
1. **Issue Submission:** User submits request via chat, email, or help center form.
2. **Automated Categorization:** AI-assisted ticket tagging based on keywords (e.g., “refund”, “account locked”).
3. **Prioritization & Assignment:** High-priority issues (payment failures, live drop errors) routed immediately to Tier 1 agents; low-priority routed to Tier 2 queue.
4. **Resolution:** Agent follows documented procedures; system tracks SLA compliance.
5. **Escalation:** Complex cases escalated to Tier 2 or Tier 3, including engineering support if needed.
6. **Closure & Feedback:** Ticket closed once resolved; user invited to provide feedback.

**Key Procedures & Edge Cases:**
- **Order Issues:** 
  - Failed payment retries automatically logged.
  - Stock unavailability triggers refund or alternative suggestions.
  - Duplicate order prevention with idempotency keys.
- **Account Issues:**
  - Locked accounts require email verification or MFA reset.
  - Forgotten passwords handled via secure recovery link with expiration.
- **Live Drop Failures:**
  - Delayed notifications or missed drops prompt apology and compensatory credits.
  - System logs events for audit trails and monitoring.

**Technical Integration:**
- Support system integrates with **Order Service** (Doc 5) for real-time order lookups.
- **Auth Service** (Doc 1) ensures secure account access during troubleshooting.
- AI-assisted auto-responses use **Knowledge Base** (Docs 1–16) for fast resolution and RAG retrieval.
- Logging captures timestamps, user ID, ticket ID, action taken, and resolution outcome for analytics.

**Performance Metrics:**
- SLA for Tier 1 response: ≤ 15 minutes.
- Ticket resolution: ≤ 24 hours for standard issues, ≤ 2 hours for urgent/live-drop issues.
- Customer satisfaction tracked via post-resolution ratings.

**Security & Privacy:**
- PII redacted in logs, encrypted in transit and at rest.
- Support agents require role-based access to sensitive data.
- Escalations follow strict approval process to prevent unauthorized access.

**User Guidance:**
- Users instructed on proper channels for different issues.
- Common FAQs linked directly in auto-responses to reduce repetitive tickets.
- Feedback mechanism ensures continuous improvement.

**Overlap With Other Topics:**
- Integrated with **Order Service** (Doc 5), **Auth Service** (Doc 1), and **Promotions** (Doc 16) for context-aware support.
- Edge-case scenarios provide RAG retrieval clarity for AI-assisted support.


### Document 13:  Mobile App Features

The Shoplite mobile application delivers an optimized experience for users to browse, follow creators, participate in live product drops, and manage their account on-the-go. This document details the app's core features, technical implementation, and edge cases.

**Core Features:**
1. **User Authentication & Profile Management:**  
   - Login via email, social accounts (OAuth2), or phone number.  
   - Multi-factor authentication (MFA) for enhanced security.  
   - Profile editing includes avatar upload, notification preferences, and linked payment methods.  

2. **Creator Following & Notifications:**  
   - Users can follow creators to receive push notifications for upcoming drops.  
   - Notifications are rate-limited to prevent spam (max 10 per hour per user).  
   - Users can mute or customize notifications per creator.  

3. **Live Drop Browsing & Participation:**  
   - Real-time inventory updates during drops.  
   - Optimized cursor-based pagination for products and drops.  
   - Countdown timers display drop start and end times accurately.  
   - Stock updates handled via Redis cache for low latency (<200ms).  

4. **Shopping Cart & Checkout:**  
   - Add multiple items across different drops.  
   - Apply promotional codes, view discounts, and estimated shipping costs.  
   - Payment methods include credit/debit cards, digital wallets, and promo credits.  
   - Order placement uses distributed locks and idempotency keys to prevent overselling.  

5. **Search & Filtering:**  
   - Search by product name, creator, category, or tags.  
   - Filters for price range, availability, popularity, and drop timing.  
   - Auto-complete suggestions powered by cached token embeddings.  

6. **Order Tracking & History:**  
   - Real-time order status updates integrated with Order Service (Doc 5).  
   - Users can cancel or request refunds within allowed windows.  
   - Notifications alert users about shipped, delivered, or delayed orders.  

**Technical Implementation:**
- **Frontend:** React Native for cross-platform support.  
- **Backend Integration:** Calls public API endpoints with cursor pagination.  
- **Caching & Performance:** Hot creator lists and popular products cached in Redis.  
- **Error Handling:**  
  - Failed payments prompt retry flow with clear user guidance.  
  - Network issues trigger offline mode with queued actions.  
  - Edge case handling for abandoned carts and expired drops.  

**Security & Privacy:**
- Sensitive data encrypted at rest and in transit.  
- Rate-limiting and CAPTCHA protect account creation and login flows.  
- Personal data handled according to privacy policies, accessible only to authorized services.  

**User Guidance & Edge Cases:**
- FAQs embedded within app for common issues (e.g., drop missed, payment failed).  
- Guidance on password recovery, account lockouts, and notification settings.  
- Edge cases such as app crashes during checkout or push notification delays are logged for monitoring and automated alerting.  

**Overlap With Other Docs:**
- Integrates with **Auth Service** (Doc 1), **Order Service** (Doc 5), and **Promotions** (Doc 16).  
- Provides retrieval context for AI-assisted responses in customer support (Doc 17).  

### Document 14:  API Documentation for Developers

The Shoplite API enables third-party developers, internal tools, and mobile apps to interact with the Shoplite platform programmatically. This document outlines endpoints, request/response formats, authentication, error handling, and best practices.

**Core API Endpoints:**
- **Authentication**
  - `POST /api/v1/auth/login`: Returns JWT token after verifying user credentials.
  - `POST /api/v1/auth/signup`: Registers a new user or creator account. Includes rate limiting (max 10 registrations/IP/hour).
  - `POST /api/v1/auth/refresh`: Refreshes JWT tokens.
- **User Management**
  - `GET /api/v1/users/{user_id}`: Fetch user profile, follows, and order history.
  - `PUT /api/v1/users/{user_id}`: Update profile or payment information.
- **Creator & Drops**
  - `GET /api/v1/creators/{creator_id}`: Fetch creator profile and active drops.
  - `POST /api/v1/drops`: Create new drops (creator-only endpoint, authenticated).
  - `GET /api/v1/drops/{drop_id}`: Retrieve drop details including stock, start time, and product list.
- **Orders**
  - `POST /api/v1/orders`: Place new order with product IDs, quantities, and payment method.
  - `GET /api/v1/orders/{order_id}`: Check order status.
- **Notifications**
  - `GET /api/v1/notifications`: Fetch user notifications (cursor-based pagination supported).

**Authentication & Security:**
- **JWT Tokens:** All endpoints require Bearer token; short-lived (1 hour) with refresh support.
- **Rate Limiting:** Protects endpoints, e.g., max 100 order requests per user per minute.
- **Data Access Control:** Users can access only their own orders; creators access only their drops.

**Request/Response Standards:**
- JSON request/response body.
- Error responses include `code`, `message`, and optional `details` for debugging.
- Idempotency supported via `Idempotency-Key` header for POST endpoints (e.g., orders, follows).

**Error Handling Examples:**
- `400 Bad Request`: Invalid parameters.
- `401 Unauthorized`: Missing or expired JWT token.
- `403 Forbidden`: Accessing another user’s data.
- `409 Conflict`: Duplicate order or already registered email.
- `429 Too Many Requests`: Exceeded rate limits.
- `500 Internal Server Error`: System failure; includes `request_id` for tracing.

**Best Practices for Developers:**
- Use cursor-based pagination to reduce load.
- Cache frequently accessed endpoints (e.g., popular drops).
- Respect rate limits and retry on `429` with exponential backoff.
- Verify server responses for null/empty fields before processing.

**Overlap With Other Topics:**
- Auth endpoints tie to **User Registration & Auth Service** (Doc 1 & Doc 3).
- Orders endpoints integrate with **Order Service** (Doc 5).
- Drops endpoints overlap with **Product/Drop Service** (Doc 4).
- Notifications endpoints overlap with **Shoplite Mobile App** (Doc 13).

**Common Questions / Edge Cases:**
- What happens if stock changes between order fetch and placement? Endpoint returns `409 Conflict` with current stock.
- Can multiple devices place the same order? Idempotency keys prevent duplicate orders.
- What if JWT token expires mid-request? API responds with `401`, requiring refresh.

### Document 15:  Security and Privacy Policies

Shoplite prioritizes the security of user data, creator assets, and platform operations. This document outlines authentication, encryption, data retention, and privacy policies to ensure safe and compliant usage.

**Authentication & Account Security:**
- All users and creators must authenticate via secure JWT tokens (short-lived, 1-hour expiry) with refresh tokens.
- Multi-Factor Authentication (MFA) is recommended for creators handling sensitive inventory or financial operations.
- Password requirements: minimum 12 characters, at least one uppercase, one lowercase, one number, one special character.
- Passwords are hashed using **Argon2id** before storage.
- Failed login attempts: 5 consecutive failed attempts per hour triggers temporary lockout (cooldown: 30 minutes).

**Data Encryption:**
- All data in transit is encrypted via **TLS 1.3**.
- Sensitive fields (e.g., payment info, emails) are encrypted at rest using **AES-256**.
- Media content stored in Blob Storage/CDN is served over HTTPS.

**Rate-Limiting and Abuse Prevention:**
- Registration: max 10 new accounts per IP per hour.
- Order placement: max 100 requests per user per minute.
- Notification requests: max 500 requests per user per hour.
- Automated suspicious activity detection triggers temporary blocks and alerts the security team.

**Privacy Policies:**
- User data is only used for platform operations, analytics, or notifications with explicit consent.
- Personally Identifiable Information (PII) is never shared with third parties without user consent.
- Data retention: inactive accounts are archived after 2 years, deleted after 5 years.
- Users may request full data export or account deletion via the `/api/v1/users/export` or `/api/v1/users/delete` endpoints.

**Security Practices & Best Practices for Developers:**
- All internal service-to-service communication uses signed JWTs with service-specific claims.
- Audit logging is enforced for critical actions: user registration, order placement, drop creation, and payment processing.
- Distributed locks and idempotency keys prevent duplicate operations in concurrent environments.
- Sharding & replication ensure high availability and prevent single-node failures.

**Common Questions / Edge Cases:**
- What happens if MFA fails? Users can request recovery codes or contact support.
- Can a deleted account’s email be reused immediately? Emails remain blocked for 30 days to prevent abuse.
- How are abandoned drops protected? Media and stock remain isolated until creator finalizes or cancels the drop.

**Overlap With Other Topics:**
- Authentication and password policies tie to **User Registration & Auth Service** (Doc 1 & Doc 3).
- Data encryption and audit logging overlap with **Order Service** (Doc 5) and **Creator Service** (Doc 4).
- Rate-limiting policies support both **API Documentation** (Doc 14) and **Mobile App Features** (Doc 13).

### Document 16:  Promotional Codes and Discounts

Shoplite allows creators and the platform to offer promotional codes and discounts to encourage engagement, increase sales, and reward loyal users. This document outlines the types of promotions, redemption rules, technical implementation, and edge cases.

**Types of Discounts:**
- **Percentage-Based Discounts:** e.g., 10% off on a specific drop or creator.
- **Fixed Amount Discounts:** e.g., $5 off orders above $50.
- **Time-Limited Promotions:** Valid for a specific duration, automatically expiring after the set time.
- **First-Time Buyer Promotions:** Restricted to users placing their first order.
- **Creator-Specific Codes:** Only valid for drops from a specific creator.

**Redemption Rules:**
- Codes are unique, case-insensitive, and stored in the PromoCode table.
- Each code includes metadata: max usage (per user / overall), expiration date, discount type, applicable product/drop, creator restriction.
- Validation occurs at order placement:
  - Check code exists and is active.
  - Check user eligibility (first-time, creator-specific, max usage not exceeded).
  - Apply discount and update usage counters atomically to prevent race conditions.
- Failed redemption triggers clear error messages (e.g., “Code expired”, “Usage limit reached”).

**Technical Implementation:**
- PromoCode Table Fields: `code`, `type`, `value`, `max_global_usage`, `max_user_usage`, `creator_id`, `start_date`, `end_date`, `active`.
- Redis cache stores active codes for high-performance validation during flash drops.
- Atomic operations with distributed locks prevent oversubscription during high-demand drops.
- Expired codes are automatically deactivated via background cleanup tasks (e.g., cron job or async worker).

**Error Handling & Edge Cases:**
- What if a code is entered simultaneously by multiple users? Distributed locks ensure only valid redemptions update usage counters.
- What if a creator deletes a drop with active promo codes? Associated codes are immediately marked inactive.
- Can a code be reused after refund or canceled order? Usage counters are decremented to allow reapplication.
- Invalid codes prompt “Code not recognized” without leaking any system information.

**User Guidance:**
- Users are notified of code acceptance, applied discount, and remaining validity at checkout.
- First-time buyer promotions clearly display eligibility and restrictions.
- Support contact for promotion issues: `support@Shoplite.com` or in-app help chat.

**Overlap With Other Topics:**
- Closely linked with **Shopping Cart & Checkout Process** (Doc 2) and **Order Service** (Doc 5) for real-time discount application.
- Edge-case handling integrates with **Security & Privacy Policies** (Doc 15) to prevent abuse.


### Document 17:  GDPR / Regional Compliance

Shoplite complies with GDPR and other regional privacy regulations to protect user data, ensure transparency, and provide users with control over their personal information. This document covers privacy principles, data retention, consent management, and cookie policies for international operations.

**Privacy Principles:**
- **Lawfulness, Fairness, and Transparency:** Users are informed about what data is collected, why, and how it will be used. Privacy policies are accessible from all pages.
- **Data Minimization:** Only essential information is collected for account creation, transactions, or analytics.
- **Purpose Limitation:** Data is used solely for intended purposes such as order processing, payment verification, and marketing with consent.
- **Accuracy:** Users can update personal data; automated systems check for inconsistencies.
- **Integrity and Confidentiality:** Data is encrypted at rest and in transit (AES-256, TLS 1.2+).

**Consent Management:**
- During registration (Docs 1 & 3), users explicitly consent to data collection.
- Cookie banners inform users about tracking cookies, optional analytics, and marketing preferences.
- Users can revoke consent at any time through account settings.
- Special procedures exist for minors or region-specific restrictions.

**Data Retention Policies:**
- Buyer account data: retained for 5 years post-account deactivation unless deletion requested.
- Creator account data: retained for 7 years for financial compliance.
- Transaction records: stored for 7 years for audit purposes.
- Personal documents (IDs, licenses): stored securely for verification, deleted upon account closure or regulatory expiration.

**Technical Implementation:**
- Data is segmented by region for legal compliance; EU data is stored on EU servers.
- Users can submit **data access requests** via secure forms; exported in machine-readable JSON/CSV.
- Automated deletion workflows handle data erasure requests (Right to be Forgotten).
- Logging tracks data access, updates, and deletions for audit purposes.
- Consent flags and cookie preferences are stored in the **Consent Service**, queried during API calls and frontend rendering.

**Error Handling & Edge Cases:**
- Users requesting deletion while orders are pending: account is disabled but transactional data retained as required.
- Conflicting regional rules: highest standard applies (e.g., GDPR vs. local law).
- Revoked consent for marketing: immediately excluded from newsletters and targeted promotions.

**User Guidance:**
- Access privacy dashboard from account settings to view or delete personal data.
- Manage cookie preferences via pop-ups on first site visit or through account settings.
- Contact support (`privacy@Shoplite.com`) for GDPR inquiries, complaints, or data export requests.

**Overlap With Other Topics:**
- Links to **User Registration & Login** (Docs 1 & 2) for consent capture.
- Connects with **Security & Privacy Policies** (Doc 15) for secure data handling.
- Interfaces with **Order & Payment Services** (Docs 5 & 6) for retention of transactional information.
- Supports RAG queries about compliance, user rights, and cookie policies with precise retrieval.
