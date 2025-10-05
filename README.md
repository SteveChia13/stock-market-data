# 🧠 S&P 500 Data Engineering Pipeline

A personal project to practice **data engineering** concepts and tools — including **Python**, **Airflow**, **dbt**, **BigQuery**, and **Docker** — by building a fully automated pipeline that collects and transforms **S&P 500 minute-interval stock data**.

---

## 🚀 Project Overview

This project simulates a modern data engineering workflow:

1. **Data Extraction** – Python web scraper collects S&P 500 minute-level data.
2. **Data Storage** – Raw data is stored in **Google BigQuery** (using the free Sandbox tier).
3. **Transformation** – **dbt** models clean, aggregate, and prepare the data for analysis.
4. **Orchestration** – **Apache Airflow** automates daily pipeline runs.
5. **Version Control** – Code managed via **Git** and **GitHub**.
6. **Containerization** – **Docker** ensures reproducible environments.

---

## 🧰 Tech Stack

| Tool | Purpose |
|------|----------|
| **Python** | Data extraction & utilities |
| **BeautifulSoup / Requests** | Web scraping |
| **BigQuery (Sandbox)** | Data warehouse |
| **dbt** | SQL-based data transformations |
| **Airflow** | Workflow orchestration |
| **Docker** | Containerized setup |
| **Git & GitHub** | Version control and collaboration |

---

## 🧩 Project Structure

