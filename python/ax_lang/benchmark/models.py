from pydantic import BaseModel


class Benchmark(BaseModel):
    """Model to run a Benchmark."""

    lang: str
    test_case: str


class BenchmarkResult(BaseModel):
    """Benchmark result for a single test case."""

    lang: str
    test_case: str
    duration_sec: float
    pick_mem_mb: float
    lang_version: str


class BenchmarkResults(BaseModel):
    """Model to store Benchmark results for all test cases."""

    lang: str
    benchmark_results: list[BenchmarkResult]
