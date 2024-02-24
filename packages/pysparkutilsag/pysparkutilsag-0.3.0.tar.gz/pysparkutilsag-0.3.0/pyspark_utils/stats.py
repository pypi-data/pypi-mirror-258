from pyspark.sql import DataFrame, SparkSession


class Stats:
    @staticmethod
    def get_size_for_machine(obj: object, spark: SparkSession):
        sc = SparkSession.sparkContext
        size_estimate = -1
        if type(obj) == DataFrame:
            size_estimate = sc._jvm.org.apache.spark.util.SizeEstimator.estimate(obj._jdf)
        else:
            size_estimate = sc._jvm.org.apache.spark.util.SizeEstimator.estimate(obj)

        return size_estimate

    @staticmethod
    def get_size_for_human(obj: object, spark: SparkSession):
        size_in_bytes = Stats.get_size_for_machine(obj, spark)
        human_readable_size = Stats.__convert_bytes(size_in_bytes)
        return human_readable_size

    @staticmethod
    def __convert_bytes(size_in_bytes):
        """
        Converts a size into appropriate SI units based on it's size
        """
        import math
        import sys

        if not isinstance(size_in_bytes, int):
            size_in_bytes = sys.getsizeof(size_in_bytes)

        if size_in_bytes == 0:
            return "0B"

        # unit_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB", "RB")
        unit_name = (
            "Bytes",
            "Kilo Bytes",
            "Mega Bytes",
            "Giga Bytes",
            "Terra Bytes",
            "Peta Bytes",
            "EB",
            "Zetta Bytes",
            "YB",
            "RB")
        i = int(math.floor(math.log(size_in_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_in_bytes / p, 2)
        return "%s %s" % (s, unit_name[i])
