# Databricks notebook source
import faiss
import numpy as np

# Convert list of embeddings into numpy array
embeddings = np.array(pdf["embedding"].tolist()).astype("float32")

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)  # L2 distance
index.add(embeddings)  # Add all vectors to index


# COMMAND ----------

query_vector = embeddings[0].reshape(1, -1)  # Shape (1, 384)

# Search for top 5 similar vectors
distances, indices = index.search(query_vector, k=5)


# COMMAND ----------

print("Top 5 similar entries for input 0:")
pdf.iloc[indices[0]][["text"]]  # Show the text of similar entries
