# UPSC Daily Current Affairs RAG System

An automated AI-powered pipeline that converts daily news into
UPSC-ready notes using Retrieval-Augmented Generation (RAG), syllabus
mapping, and PYQ linkage.

Designed for serious UPSC aspirants.

------------------------------------------------------------------------

## 🎯 What This Project Does

Every day it:

1.  Scrapes news from:
    -   The Hindu
    -   Indian Express
2.  Filters relevant articles using:
    -   UPSC GS syllabus similarity
3.  Links each article to:
    -   GS syllabus topics
    -   Prelims PYQs
    -   Mains PYQs
4.  Generates:
    -   30-second summary
    -   Prelims facts
    -   Mains answer-style material
5.  Sends a daily email:
    -   Top 25 UPSC-relevant articles
    -   Fully formatted notes

------------------------------------------------------------------------

## 🧠 Core Idea

UPSC preparation requires connecting:

-   Current affairs\
-   Static syllabus\
-   PYQs

This system automates that bridge using AI + semantic search.

------------------------------------------------------------------------

## 🏗️ Architecture

RSS → Scraper → Syllabus Linker → PYQ Retrieval → Priority Engine → LLM
Summarizer → Email

Modules:

-   rss_fetcher.py → pulls daily news
-   news_scraper.py → extracts article text
-   syllabus_linker.py → GS topic mapping via FAISS
-   retriever.py → Prelims PYQ search
-   mains_pyq_retriever.py → Mains PYQ search
-   priority_classifier.py → relevance scoring
-   news_summarizer.py → LLM notes generation
-   daily_news_pipeline.py → orchestration
-   daily_mailer.py → sends email

------------------------------------------------------------------------

## 📊 Features

### 📚 Syllabus Intelligence

-   Maps news → GS1/GS2/GS3/GS4
-   Removes irrelevant content automatically

### 📜 PYQ Linkage

-   Shows years where similar questions appeared
-   Works for BOTH:
    -   Prelims
    -   Mains

### 🧾 Answer-Ready Material

Each article produces:

-   30-sec summary
-   Prelims facts
-   Mains material:
    -   Intro
    -   Body
    -   Conclusion + Way Forward

### 📬 Daily Email Automation

-   Sends Top 25 UPSC-relevant stories
-   Fully formatted notes

------------------------------------------------------------------------

## 🛠️ Tech Stack

-   Python
-   FAISS (semantic search)
-   SentenceTransformers
-   Google Gemini API
-   RSS scraping
-   HTML email automation

------------------------------------------------------------------------

## 📁 Folder Structure

upsc_rag/ │ ├── rag/ │ ├── daily_mailer.py │ ├── daily_news_pipeline.py
│ ├── news_pipeline.py │ ├── news_scraper.py │ ├── news_summarizer.py │
├── priority_classifier.py │ ├── retriever.py │ ├──
mains_pyq_retriever.py │ ├── syllabus_linker.py │ └── ... │ ├── data/ │
├── syllabus_index/ │ ├── prelims_pyq_index/ │ └── mains_pyq_index/ │
├── venv/ ├── requirements.txt └── README.md

------------------------------------------------------------------------

## ⚙️ Setup

### 1. Clone

git clone https://github.com/YOUR_USERNAME/upsc-current-affairs-rag.git
cd upsc-current-affairs-rag

### 2. Create virtual env

python -m venv venv source venv/bin/activate pip install -r
requirements.txt

### 3. Set API keys

export GOOGLE_API_KEY="your_key"

------------------------------------------------------------------------

## ▶️ Run Manually

python rag/daily_mailer.py

------------------------------------------------------------------------

## ⏰ Run Daily (Automation)

Use:

-   Windows Task Scheduler + WSL
-   Or cron in Linux

Runs automatically at 7 AM.

------------------------------------------------------------------------

## 🎓 Who Is This For?

-   UPSC aspirants
-   EdTech researchers
-   NLP + RAG learners
-   Productivity hackers

------------------------------------------------------------------------

## 👨‍💻 Author

Lakshya Yadav

Focused on: - AI + Education - RAG systems - UPSC automation tools

------------------------------------------------------------------------

## ⭐ Why This Project Matters

Instead of reading 50 articles daily, this system extracts only what
UPSC cares about.

It turns news into: - Exam-ready notes - PYQ-linked concepts - Mains
answer material

Automatically.
