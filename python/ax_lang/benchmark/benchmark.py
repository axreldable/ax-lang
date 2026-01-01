import time

from ax_lang.benchmark.lang_executor import LanguageExecutorFactory
from ax_lang.utils import get_examples_root
from pydantic import BaseModel


class Benchmark(BaseModel):
    lang_name: str
    test_file: str


class BenchResult(BaseModel):
    benchmark: Benchmark
    duration_sec: float
    pick_mem_mb: float
    lang_version: str


class BenchResults(BaseModel):
    bench_results: list[BenchResult]


class BenchmarkRunner:
    def _run_benchmark(self, bench: Benchmark) -> BenchResult:
        executor = LanguageExecutorFactory.get(bench.lang_name)

        start = time.time()
        executor.run(bench.test_file)
        end = time.time()
        duration_sec = end - start

        return BenchResult(
            benchmark=bench,
            duration_sec=duration_sec,
            pick_mem_mb=0.0,
            lang_version=executor.get_lang_version(),
        )

    def _get_full_test_file_path(self, lang: str, test: str, extension: str):
        return str(get_examples_root() / lang / f"{test}.{extension}")

    def __init__(self, langs: list[str], tests: list[str]) -> None:
        self.benchmarks = []
        for lang in langs:
            executor = LanguageExecutorFactory.get(lang)
            for test in tests:
                test_file = self._get_full_test_file_path(
                    executor.lang_cli_runner(), test, executor.lang_extension()
                )
                benchmark = Benchmark(lang_name=lang, test_file=test_file)
                self.benchmarks.append(benchmark)

    def run(self) -> BenchResults:
        results = []
        for bench in self.benchmarks:
            bench_result = self._run_benchmark(bench)
            results.append(bench_result)
        return BenchResults(bench_results=results)
