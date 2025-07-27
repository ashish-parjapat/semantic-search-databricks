# 🧠 News Article Semantic Search with Sentence Transformers + FAISS on Databricks

This project implements a **semantic search engine** for news articles using **Sentence Transformers for vector embeddings** and **FAISS for similarity search**, entirely built and run on **Azure Databricks**.

---

## 🔍 Project Objective

The goal is to enable semantic (meaning-based) search across a collection of news articles. Instead of relying on keyword matches, we embed articles using **MiniLM** model and use **vector similarity** to find the most relevant content.

---

## 📁 Dataset

We use a news dataset that contains:

- `headline`: Title of the article  
- `category`: News category (e.g., politics, tech)
- `date`: Date of publication  
- `description`: Summary  
- `text`: Full content of the article  

---

## 🧰 Tools & Technologies

| Tool            | Purpose                                  |
|-----------------|------------------------------------------|
| Databricks      | Cloud compute & collaborative notebooks  |
| PySpark         | Distributed data processing              |
| SentenceTransformers | Text embedding model (`MiniLM-L6-v2`) |
| FAISS           | Fast Approximate Nearest Neighbor Search |
| Azure Data Lake | (Optional) Cloud data storage            |
| UMAP + Matplotlib | (Optional) Embedding visualization     |

---

## 🧱 Architecture

```mermaid
graph TD;
    A[Raw News Articles (CSV)] --> B[Databricks Notebook];
    B --> C[Text Preprocessing];
    C --> D[SentenceTransformer Embedding];
    D --> E[embedded_df];
    E --> F[FAISS Index];
    F --> G[Semantic Search Interface];
