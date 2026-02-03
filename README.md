# Unified-Payments-API
This project is a Unified Payments API that centralizes payment data from Stripe and Mollie into a single, normalized backend, with a web dashboard for analytics and monitoring.

# Unified Payments API — Stripe & Mollie

## 🚀 Overview

This project is a **Unified Payments API** that centralizes payment data from **Stripe** and **Mollie** into a single, normalized backend, with a web dashboard for analytics and monitoring.

The goal of this project is to replicate, in a simplified and personal way, the concept of a **unified financial API**, similar to what companies like Chift provide.

Instead of interacting separately with Stripe and Mollie, this API allows you to:

* Connect multiple payment providers
* Sync transactions from each provider
* Store them in a unified database
* Expose clean, aggregated endpoints
* Visualize everything in a dashboard

This project was built as both:

* A technical challenge in **Python/FastAPI**
* A portfolio project to demonstrate backend design, API integration, and data processing

---

## 🎯 Motivation

While applying to fintech startups, I discovered companies like **Chift**, which offer a unified API for financial tools.

Having previously worked with **Node.js and PHP**, I wanted to challenge myself with a larger project in **Python**, while also exploring real-world payment APIs.

So I built a **miniature version of a unified payments platform**, connecting:

* **Stripe** (international payments)
* **Mollie** (popular in Benelux for Bancontact, iDEAL, etc.)

---

## 🏗️ Architecture

### High-level Flow

```
Customer → Shop → Stripe or Mollie → Payment Provider
```

Then, in my system:

```
Unified API → Calls Provider → Syncs Data → Stores in DB → Dashboard
```

### Components

#### 🔹 Backend (FastAPI - Python)

* REST API built with **FastAPI**
* Provider abstraction layer (`StripeService`, `MollieService`)
* Unified data model for payments
* Background sync mechanism
* Error handling for API limits, invalid keys, etc.
* SQLite database with SQLAlchemy
* Redis for caching (optional)

#### 🔹 Dashboard (HTML / JS / Chart.js)

The frontend allows you to:

* Select a provider (Stripe, Mollie, or All)
* Trigger manual sync
* View:

  * Total revenue
  * Transactions by status (succeeded, failed, pending, etc.)
  * Breakdown by currency
  * Activity over time (charts)

---

## 🔌 Supported Providers

| Provider | Status             | Features                                       |
| -------- | ------------------ | ---------------------------------------------- |
| Stripe   | ✅ Supported        | List payments, sync transactions, analytics    |
| Mollie   | ✅ Supported        | List payments, sync transactions, analytics    |

---

## 📡 Key API Endpoints

Later

## 🧠 Unified Data Model (Simplified)

All providers are normalized into a single structure like:

```json
{
  "id": "tr_123",
  "provider": "stripe",
  "amount": 1500,
  "currency": "EUR",
  "status": "succeeded",
  "created_at": "2026-01-20T14:32:00Z"
}
```

## 🛠️ Tech Stack

### Backend

* Python 3.12
* FastAPI
* SQLAlchemy + SQLite
* Pydantic
* Stripe SDK
* Mollie SDK

### Frontend

* HTML / CSS / JavaScript
* Chart.js for data visualization

### DevOps

* Docker
* Docker Compose

---

## 👨‍💻 Author

**Armand**

* Backend & Cloud enthusiast
* Interested in FinTech, APIs, and payment systems
* Building real-world projects to learn and showcase skills
