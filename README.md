# Apex-Stock: Institutional Resource Planning (IRP) Framework

Apex-Stock is not a traditional inventory system. It is a **Financial and Accountability Control Layer** that sits on top of school operations, ensuring every resource is tracked, auditable, and optimally used.

## 1. Domain Model: Hierarchy & Structure
The system mirrors the **Physical World**, with a three-pillar data model.

### A. Spatial Hierarchy (Space Tracking)
Assets are spread across the campus—not just in a store. Apex-Stock models the full spatial chain:

- **Root:** Organization (The School)
- **Node:** Branch (Campus A, Campus B)
- **Leaf:** Zones (Admin, Academics, Lab) → Rooms → Cupboards → Shelves

**Benefit:** You can audit a specific cupboard and even a single shelf to see exactly what is stored there.

### B. Asset vs. Consumable Logic
Each item is treated according to its nature:

- **Fixed Assets** (Projectors, Tablets, Chairs)
  - Tracked by **Unique ID**
  - Subject to periodic audits
- **Consumables** (Glue sticks, Papers, Chalks)
  - Tracked by **Quantity**
  - **Wastage rates** are calculated over time

## 2. The "Double-Shake" Custody Protocol
Apex-Stock’s USP eliminates pilferage by locking accountability into a two-step acceptance flow.

1. **Issuance (Handover):** Store-keeper creates a transaction record. Stock is not deducted yet—only **locked**.
2. **In-Transit State:** Accountability remains with the store-keeper until acceptance.
3. **Digital Acknowledgement:** The receiver (Teacher) verifies and clicks **Accept**.
4. **Final Transfer:** Stock is deducted from store-keeper (-) and credited to teacher (+).

**Result:** No one can claim *“I never received it.”*

## 3. Advanced Transformation & Production Module
Tracks conversion of raw materials into finished goods.

- **BOM (Bill of Materials):** Admin defines inputs (e.g., a **Bird Model** needs 2 foam sheets + 1 glue stick).
- **Transformation Request:** Teacher submits conversion.
- **Visual Proof:** Teacher uploads a photo of the finished item.
- **Ledger Update:** System deducts inputs and credits the finished good to the teacher’s wallet.

## 4. Strategic Reporting & AI Alerts
Data becomes insight-driven action:

- **Abnormal Consumption Alerts:** If one teacher uses far more resources than peers, the principal receives a red flag.
- **Dead-Stock Reports:** Items untouched for 6+ months are flagged for redistribution.
- **Predictive Re-ordering:** Based on past usage, the system forecasts stock depletion.

## 5. Technical Framework & Security

### Stack
- **Core:** Django (Python) — secure relational management via ORM
- **Interface:** Tailwind CSS + Alpine.js — sleek SaaS UI
- **Cloud:** AWS EC2 & RDS — high availability and durability

### Security Layers
- **Audit Logging:** Every action is recorded (who, what, when)
- **Encrypted Storage:** All uploaded images stored securely in AWS S3

## 6. Role-Based Access Matrix (Example)

| Role          | Dashboard View | Key Powers |
|---------------|----------------|-----------|
| Super Admin   | Global View    | Full Control, Delete Permissions, Financial Audit |
| Coordinator   | Zone View      | Approve/Reject Staff Requests, Transfer items between Teachers |
| Store-keeper  | Warehouse View | Inward Stock, QR Code Printing, Low Stock Alerts |
| Teacher       | Personal Wallet| Request Items, Consumption Logging, Return Assets |

## Final Vision Statement
> "Main aik aisa intelligent ecosystem bana raha hoon jo school ke har chotay se chotay resource ki lifecycle ko track karta hai. Ye sirf aik software nahi hai, ye school management ki digital aankh (Digital Eye) hai jo resources ko chori hone se bachati hai aur unke behtareen istemal (Optimal Usage) ko yaqeeni banati hai."
