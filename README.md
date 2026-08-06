# Portfolio
Lilith Froude | Data Science & AI Portfolio
ML Engineer • Data Scientist • Full-Stack Developer
📍 Phoenix, AZ | 📧 lilith.froude@gmail.com | www.linkedin.com/in/lilithfroude

## About Me
I build intelligent systems that turn complex data into actionable insights. With a background bridging business strategy and technical implementation, I specialize in translating data science solutions into real-world business value.
Completed my MS in AI in Business at Arizona State University, I bring a unique perspective to technical problems—combining rigorous machine learning methodology with clear communication tailored to stakeholders, whether they're executives, engineers, or end-users.

## Core Competencies
Python, TensorFlow/Keras, scikit-learn, BiLSTM, Random Forest, Isolation Forest, K-MeansData, Tableau, Streamlit, Plotly, Matplotlib, Seaborn, Full-Stack Development, React, TypeScript, Next.js, Node.js, PostgreSQL, Blockchain/Web3, Smart Contracts, SQL, Pandas, NumPy, Data Pipelines, Feature Engineering, NLP

# Featured Projects

## Multi-Agent Systems & Agentic AI

Design and architecture work for a **CrewAI** multi-agent pipeline that turns chat history into sitter retention intelligence: a five-agent crew (Supervisor, Data Collector, Perception, Reasoning, Reporter) ingests conversation data, scores surface and deep sentiment (VADER, HuggingFace, LangChain RAG over FAISS), and produces churn risk plus personalized outreach. The write-up covers agent roles, standard vs. custom tools, and open-source LLM choices (e.g. Llama 3.1, Mistral, Qwen2.5) for real chat signal.

**Deliverable:** [Agentic Sentiment — Babysitter Churn Detection Workflow (PDF)](Agentic_AI/agentic_sentiment_babysitter.pdf)

CrewAI, LangChain, open-source LLMs, NLP, RAG, sentiment analysis

## 🧬 Machine Learning Protein Prediction Pipeline
Multi-Model ML Pipeline for Drug Discovery
Built an end-to-end computational triage system using three models selected for distinct prediction tasks:

BiLSTM Neural Network → Secondary structure prediction
Random Forest Classifier → Protein stability classification
Isolation Forest → Anomaly detection

Impact: Reduces initial drug candidate screening from 6-18 months to minutes, with potential cost savings of $100K-$500K per structure.
Python, TensorFlow/Keras, scikit-learn, Pandas

## 🐾 Pet-Friendly Arizona Venue Recommendation System
Built an end-to-end NLP pipeline that goes beyond Yelp's binary "pet-friendly" label to surface the actual quality of pet experiences at Arizona venues. The system analyzes 4,577 reviews across 422 businesses using a four-stage pipeline:

1. **Text Preprocessing** → spaCy lemmatization + rule-based extraction to flag 10 binary pet features (patio, shade, fencing, water, safety, etc.)
2. **Topic Modeling** → BERTopic (SentenceTransformer + UMAP + HDBSCAN) discovered 34 distinct topics across the review corpus, revealing clear rating-driven patterns in how customers describe pet-friendly venues.
3. **Multi-Label Classification** → Compared Logistic Regression, Linear SVM, and Random Forest on the pet feature classification task. Linear SVM achieved the best Macro F1 of 0.1635 — low due to severe class imbalance (under 5% of reviews contain explicit pet language), but the composite scoring engine compensates by weighting learnable features more heavily.
4. **Composite Scoring Engine** → Ranked 269 venues across four weighted dimensions: NLP-detected features (40%), VADER sentiment (35%), BERTopic relevance (15%), and Yelp star ratings (10%).

**Key insight:** Top-ranked venues cluster at low review counts — venues with fewer but more concentrated pet-specific reviews outperform high-volume venues where pet language gets diluted.

Python, spaCy, BERTopic, VADER, scikit-learn, UMAP, HDBSCAN, Pandas, Matplotlib

## 🚗 Sky Harbor Airport Ride-Hailing Dashboard
Real-Time Interactive Data Visualization
Developed a Streamlit-based dashboard visualizing ride-hailing activity at Phoenix Sky Harbor Airport's pickup zones.

Service-specific color coding (Uber, Lyft, Waymo, Taxi)
Dynamic statistics panels with real-time filtering
Animated 60-frame visualization showing temporal patterns

Techniques: Time-series analysis, visualization, animation generation,
Python, Streamlit, Tableau, Matplotlib

## 💳 CommunityTap – Full-Stack SaaS Platform
Hyper-Local Crowdfunding Application
Architected and built a complete crowdfunding platform in a 48-hour sprint, demonstrating rapid prototyping and full-stack capabilities.

PostgreSQL schema with 8+ tables and Row-Level Security
Edge Functions for payment processing and automation
Third-party integrations: Stripe Connect, Mapbox, Resend

React, TypeScript, PostgreSQL, Stripe API, Mapbox API

## 🎫 CrowdCtrl – Blockchain Ticketing System
Decentralized Event Management Platform
Designed a Web3 ticketing solution using NFT technology to combat fraud and enable transparent resale markets.

ERC-721 NFT tickets with automated royalty distribution
Smart contracts enforcing resale price ceilings and transfer restrictions
2nd Place – GVSU DEMO Day Pitch Competition

Solidity, BASE/Ethereum L2, Next.js, Smart Contracts

## Tableau Visualization Projects
Interactive dashboards demonstrating business intelligence across multiple domains:
Dashboards, calculated fields, parameters, Heat maps, trend analysis, categorical comparisons, scatter plots, Competitive analysis

## Technical Philosophy
I believe the best data solutions are audience-aware:

For Executives: High-level dashboards with clear KPIs and business impact metrics
For Engineers: Well-documented code, reproducible pipelines, and scalable architecture
For End-Users: Intuitive interfaces that surface insights without requiring technical expertise

This portfolio demonstrates my ability to work across the entire data lifecycle—from raw data ingestion to production deployment—while adapting my communication style to the audience at hand.

## Education
Master of Science in AI in Business | Arizona State University | Expected Spring 2026
Bachelor of Business Administration | Grand Valley State University | 2023
Majors: Marketing, Entrepreneurship | Minor: Digital Studies

## Let's Connect
I'm actively seeking opportunities in Data Science, ML Engineering, and AI Product Development.
📧 lilith.froude@gmail.com
🔗 www.linkedin.com/in/lilithfroude

Built with curiosity, caffeine, and a commitment to continuous learning.
