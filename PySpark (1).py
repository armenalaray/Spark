from pyspark.sql import SparkSession
import pyspark.sql.functions as F

spark = (
    SparkSession.
    builder.
    appName("Analysing the vocabulary of Pride and Prejudice.").
    getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

results=(
    spark.read.text("Gutenberg/*.txt").
    select(F.split(F.col("value"), " ").alias("line")).
    select(F.explode(F.col("line")).alias("word")).
    select(F.lower(F.col("word")).alias("word_lower")).
    select(F.regexp_extract(str=F.col("word_lower"),pattern="[a-z]+",idx=0).alias("word")).
    filter(F.col("word")!="").
    groupBy(F.col("word")).
    count()
)

results.orderBy(F.col("count"), ascending=False).show(10)
results.write.csv("Data/simple_count.csv", mode="overwrite")





