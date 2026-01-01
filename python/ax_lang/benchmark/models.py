from pydantic import BaseModel


class Benchmark(BaseModel):
    lang_name: str
    test_case: str


class BenchmarkResult(BaseModel):
    lang_name: str
    test_case: str
    duration_sec: float
    pick_mem_mb: float
    lang_version: str


class BenchmarkResults(BaseModel):
    benchmark_results: list[BenchmarkResult]
