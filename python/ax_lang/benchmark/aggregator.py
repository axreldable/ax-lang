from abc import ABC, abstractmethod

import pandas as pd
from ax_lang.benchmark.benchmark import BenchmarkResults
from tabulate import tabulate


class ResultAggregator(ABC):
    def __init__(self, benchmark_results: list[BenchmarkResults]):
        self.benchmark_results_dict = self.benchmark_results_to_df_dict(
            benchmark_results
        )
        self.benchmark_results_df = self.benchmark_results_to_df(benchmark_results)

    @abstractmethod
    def aggregate(self):
        pass

    def bench_to_df(self, results: BenchmarkResults) -> pd.DataFrame:
        results = [result.model_dump() for result in results.benchmark_results]
        return pd.DataFrame(results)

    def benchmark_results_to_df_dict(
        self, results: list[BenchmarkResults]
    ) -> dict[str, pd.DataFrame]:
        d = {}
        for result in results:
            df = self.bench_to_df(result)
            d[result.lang] = df
        return d

    def benchmark_results_to_df(self, results: list[BenchmarkResults]) -> pd.DataFrame:
        return pd.concat([self.bench_to_df(result) for result in results])


class TableAggregator(ResultAggregator):
    def aggregate(self):
        for lang_name, benchmark_result_df in self.benchmark_results_dict.items():
            print(f"Benchmark {lang_name}")
            print(tabulate(benchmark_result_df, headers="keys", tablefmt="psql"))

    def aggregate_by_name(self, benchmark_name: str) -> pd.DataFrame:
        return self.benchmark_results_dict[benchmark_name]

    def aggregate_by_field(self, field: str, langs: list[str]) -> pd.DataFrame:
        df = self.benchmark_results_df
        df = df.pivot(index="test_case", columns="lang", values=field)
        df = df[langs]  # to have lang columns in order
        column_rename = {col: f"{col}_{field}" for col in df.columns}
        df = df.rename(columns=column_rename)
        return df
