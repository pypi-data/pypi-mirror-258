import math
import sys
from pyspark.sql import DataFrame, SparkSession


class LocalCalculator:
    @staticmethod
    def __convert_bytes(size_in_bytes):
        """
        Converts a size into appropriate SI units based on it's size
        """

        if not isinstance(size_in_bytes, int):
            size_in_bytes = sys.getsizeof(size_in_bytes)

        if size_in_bytes == 0:
            return "0B"

        unit_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB", "RB")
        i = int(math.floor(math.log(size_in_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_in_bytes / p, 2)
        return "%s %s" % (s, unit_name[i])


class ObjectSizeCalculator:
    def __init__(self, spark: SparkSession):
        self.__spark = spark

    def get_size_for_machine(self, obj: object):
        sc = self.__spark.sparkContext
        size_estimate = -1
        if type(obj) == DataFrame:
            size_estimate = sc._jvm.org.apache.spark.util.SizeEstimator.estimate(obj._jdf)
        else:
            size_estimate = sc._jvm.org.apache.spark.util.SizeEstimator.estimate(obj)
        return size_estimate

    def get_size_for_human(self, obj: object):
        size_in_bytes = self.get_size_for_machine(obj)
        human_readable_size = LocalCalculator.__convert_bytes(size_in_bytes)
        return human_readable_size
