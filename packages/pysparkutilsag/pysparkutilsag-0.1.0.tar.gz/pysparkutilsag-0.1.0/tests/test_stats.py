from pyspark_utils.stats import Stats
from pyspark.sql import DataFrame, SparkSession

# spark = (
#   SparkSession
#     .builder
#     .appName("AshSparkApp")
#     .master("local[*]")
#     .getOrCreate()
# )


# obj = [1,2,3,4]
# size_in_bytes = Stats.get_size_for_machine(obj,spark=spark)
# assert size_in_bytes==144, True