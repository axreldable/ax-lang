from abc import ABC, abstractmethod

import pandas as pd
from tabulate import tabulate

from ax_lang.benchmark.benchmark import BenchmarkResults


class ResultAggregator(ABC):
    def __init__(self, benchmark_results: list[BenchmarkResults]):
        self.benchmark_results = benchmark_results

    @abstractmethod
    def aggregate(self):
        pass


class TableAggregator(ResultAggregator):
    def aggregate(self):
        df = pd.DataFrame(self.benchmark_results[0].model_dump())
        print(tabulate(df, headers="keys", tablefmt="psql"))
