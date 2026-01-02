import logging
import time

from ax_lang.benchmark.lang_executor import LanguageExecutorFactory
from ax_lang.benchmark.models import Benchmark, BenchmarkResult, BenchmarkResults
from ax_lang.utils import get_examples_root

logger = logging.getLogger(__name__)


class BenchmarkRunner:
    def __init__(self, lang: str, dry_run: bool = False) -> None:
        self.executor = LanguageExecutorFactory.get(lang)
        self.dry_run = dry_run
        self.lang = lang

    def _run_benchmark(self, bench: Benchmark) -> BenchmarkResult:
        test_file_path = self._get_full_test_file_path(
            self.executor.lang_name(), bench.test_case, self.executor.lang_extension()
        )

        start = time.time()
        if self.dry_run:
            logger.info("Dry run - benchmark has not been executed.")
        else:
            self.executor.run(test_file_path)
        end = time.time()
        duration_sec = end - start

        return BenchmarkResult(
            lang=bench.lang,
            test_case=bench.test_case,
            duration_sec=duration_sec,
            peak_mem_mb=0.0,
            lang_version=self.executor.get_lang_version(),
        )

    def _get_full_test_file_path(self, dir_name: str, test_case: str, extension: str):
        return str(get_examples_root() / dir_name / f"{test_case}.{extension}")

    def run(self, tests: list[str]) -> BenchmarkResults:
        results = []
        for test in tests:
            benchmark = Benchmark(lang=self.executor.lang_name(), test_case=test)
            result = self._run_benchmark(benchmark)
            results.append(result)

        return BenchmarkResults(lang=self.lang, benchmark_results=results)
