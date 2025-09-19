# livedrop--jihaneKai-
# LiveDrop – Flash-Sale & Follow Platform

## Overview
LiveDrop allows creators to run limited-inventory live product drops. Users can follow creators, receive real-time notifications, browse products, and place orders during drops. The system handles sudden traffic spikes from popular creators while ensuring data consistency and reliability.

---

## Architecture Diagram
[Link to your Excalidraw diagram here]

---

## High-Level Design

### 1. API Layer
- **API Gateway / Load Balancer**: Stateless, routes requests, rate-limits, validates JWTs.  
  **Why:** Ensures scalability, protects backend from traffic spikes.  
  **Prevents:** Overload, unauthorized access.

- **Public API Endpoints**: Cursor-based pagination for followers, products, and drops.  
  **Why:** Efficient fetching, mobile-friendly.  
  **Prevents:** Slow response, inconsistent paging.

---

### 2. Core Microservices
| Service | Purpose | Key Solutions & Prevented Issues |
|---------|---------|---------------------------------|
| **Auth Service** | User login/signup | Stateless, JWT, replicated DB. Prevents auth bottlenecks. |
| **User Service** | Follow/unfollow, list followers/following | Sharding + hashing, Redis cache for hot creators, cursor pagination. Prevents hot-key issues, ensures deterministic results. |
| **Creator Service** | Profile, media management | Media in Blob Storage/CDN, thumbnails. Prevents slow media delivery, reduces bandwidth. |
| **Product/Drop Service** | Create drops, manage stock | Normalized DB, indexing, stock cache, distributed locks, ACID transactions. Prevents overselling, ensures low-latency reads. |
| **Order Service** | Place orders, track status | Idempotency key, distributed locks, async event bus tasks. Prevents duplicate orders, maintains stock integrity.

---

### 3. Databases & Cache
- **SQL DB**: Stores Users, Creators, Products, Drops, Orders. Normalized, sharded, replicated.  
  **Why:** ACID compliance, high availability.  
  **Prevents:** Overselling, data loss, hot spots for celebrity creators.

- **Redis Cache**: Stock levels, hot follower lists, popular products/drops.  
  **Why:** Low-latency access for high-read traffic.  
  **Prevents:** Slow queries, read bottlenecks.

- **Blob Storage / CDN**: Media delivery.  
  **Why:** Fast access, scalable.  
  **Prevents:** High bandwidth usage, slow page loads.

---

### 4. Event Bus & Async Tasks
- **Kafka/RabbitMQ**: Stock updates, drop start/sold out events, notifications, audit logs.  
  **Why:** Decouples async tasks from main requests.  
  **Prevents:** Blocking critical flows, ensures notifications are delivered reliably.

---

### 5. Key System Solutions
| Feature | Why Chosen | Prevented Issue |
|---------|-----------|----------------|
| **Cursor-based pagination** | Efficient, deterministic queries | Slow or inconsistent paging |
| **Sharding & hashing** | Distribute follower data | Hot key / celebrity creator bottlenecks |
| **Idempotency key** | Safe retries | Duplicate orders / follows |
| **Distributed locks** | Safe stock deduction | Overselling with concurrent orders |
| **Replication** | High availability | Data loss, read overload |
| **Monitoring / Metrics** | Track performance | Undetected failures or bottlenecks |
| **Audit Trail** | Record critical actions | Loss of traceability |
| **Stateless microservices** | Easy horizontal scaling | Single-node failure impact |

---

### 6. Performance & Scaling
- Supports 500 sustained read requests/sec (bursts up to 1500).  
- 150 order attempts/sec during live drops.  
- Read p95 ≤200ms, order placement ≤500ms, notifications <2s.  
- Designed to scale horizontally; cache & replication prevent performance collapse during celebrity drops.

---

### 7. Security & Access
- Users can only access their own orders and follow relationships.  
- Internal service-to-service communication is authenticated and authorized.

---

### 8. Summary
This design ensures **scalability, reliability, consistency, and low-latency notifications** while handling **sudden spikes from popular creators**. Each choice solves a specific problem: caching for speed, sharding for distribution, ACID + locks for correctness, and async queues for responsive event handling.
