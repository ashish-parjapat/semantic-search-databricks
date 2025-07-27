# Databricks notebook source
df = spark.read.option("header", "true").json("abfss://data@newsdata.dfs.core.windows.net/News_Category_Dataset_v3.json")
display(df.show(5))


# COMMAND ----------

from pyspark.sql.functions import lower,col,trim

cleaned_df=df.select(trim(lower(col('headline'))).alias('headline'),
                     trim(lower(col('category'))).alias('category'),
                     trim(lower(col('date'))).alias('date'),
                     trim(lower(col('short_description'))).alias('description')
                     )

display(cleaned_df.show(5))                     

# COMMAND ----------

# Step 2: Combine into single 'text' column
from pyspark.sql.functions import concat_ws,col
processed_df = cleaned_df.withColumn(
    "text",
    concat_ws(" | ", col("headline"), col("description"), col("category"), col("date"))
)

processed_df.select("text").show(5, truncate=False)


# COMMAND ----------

processed_df.write.format("delta").mode("overwrite").save("/mnt/delta/news_processed")



# COMMAND ----------

display(dbutils.fs.ls("/mnt/delta/news_processed"))


# COMMAND ----------

processed_df.write.format("delta").mode("overwrite").save("abfss://data@newsdata.dfs.core.windows.net/processed/")
