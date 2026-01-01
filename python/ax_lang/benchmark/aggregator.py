from abc import ABC, abstractmethod

import pandas as pd
from ax_lang.benchmark.benchmark import BenchResults
from tabulate import tabulate


class ResultAggregator(ABC):
    def __init__(self, benchmark_results: list[BenchResults]):
        self.benchmark_results = benchmark_results

    @abstractmethod
    def aggregate(self):
        pass


class TableAggregator(ResultAggregator):
    def aggregate(self):
        df = pd.DataFrame(self.benchmark_results[0].model_dump())
        print(tabulate(df, headers="keys", tablefmt="psql"))
