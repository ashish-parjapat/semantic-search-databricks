# Databricks notebook source
# MAGIC %pip install -U sentence-transformers

# COMMAND ----------

dbutils.library.restartPython()


# COMMAND ----------

df = spark.read.format("delta").load("abfss://data@newsdata.dfs.core.windows.net/processed/")
# pdf = df.select("text").toPandas()   # Convert to Pandas for embedding
# texts = pdf['text'].tolist()


# COMMAND ----------

# Create UDF for embedding
from pyspark.sql.functions import udf
from pyspark.sql.types import ArrayType, FloatType
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text):
    return model.encode(text).tolist()

embed_texts_udf = udf(get_embedding, ArrayType(FloatType()))

# Apply embedding to the `text` column
embedded_df = df.withColumn("embedding", embed_texts_udf("text"))

# View results
# embedded_df.select("text", "embedding").show(truncate=False)



# COMMAND ----------

embedded_df.printSchema()



# COMMAND ----------

# Create global temp view
embedded_df.createOrReplaceGlobalTempView("embedded_temp_view")


# COMMAND ----------

#just checking the vectors

# COMMAND ----------

# Limit to 3000 or less to keep viz fast
embed_pd = embedded_df.select("embedding").toPandas()
vectors = embed_pd["embedding"].tolist()


# COMMAND ----------

# MAGIC %pip install --upgrade numpy
# MAGIC

# COMMAND ----------

# MAGIC %restart_python

# COMMAND ----------

# MAGIC %pip install --force-reinstall --no-cache-dir numpy==1.25.2
# MAGIC

# COMMAND ----------

dbutils.library.restartPython()

# COMMAND ----------

# MAGIC %pip install umap-learn matplotlib
# MAGIC

# COMMAND ----------

import umap.umap_ as umap
import matplotlib.pyplot as plt

# Assuming `vectors` is your list of embeddings
umap_model = umap.UMAP(n_components=2, random_state=42)
reduced = umap_model.fit_transform(vectors)

# Plot
plt.figure(figsize=(10, 6))
plt.scatter(reduced[:, 0], reduced[:, 1], s=5, alpha=0.6)
plt.title("2D Visualization of Text Embeddings")
plt.xlabel("UMAP-1")
plt.ylabel("UMAP-2")
plt.grid(True)
plt.show()


# COMMAND ----------

from pyspark.sql.functions import col, size

# Remove rows where `embedding` is null or empty
clean_df = embedded_df.filter((col("embedding").isNotNull()) & (size("embedding") > 0))


# COMMAND ----------

#embedding search
reduced_df = clean_df.select("embedding")





# COMMAND ----------

reduced_df.count()

# COMMAND ----------

pdf = reduced_df.toPandas()
