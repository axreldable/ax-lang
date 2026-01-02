from ax_lang.benchmark.aggregator import TableAggregator
from ax_lang.benchmark.benchmark import BenchmarkRunner
from ax_lang.benchmark.models import BenchmarkResults
from ax_lang.utils import print_df


def run_benchmarks(langs: list[str], tests: list[str]) -> list[BenchmarkResults]:
    # dry_run = True
    dry_run = False
    results = []
    for lang in langs:
        runner = BenchmarkRunner(lang, dry_run)
        results.append(runner.run(tests))
    return results


def print_benchmark_results(langs: list[str], results: list[BenchmarkResults]) -> None:
    agg = TableAggregator(results)
    for lang in langs:
        df = agg.aggregate_by_name(lang)
        print(f"Benchmark results for `{lang}`:")
        print_df(df)

    print("Benchmark aggregated duration results:")
    df = agg.aggregate_by_field("duration_sec", langs)
    print_df(df)

    print("Benchmark aggregated memory results:")
    df = agg.aggregate_by_field("pick_mem_mb", langs)
    print_df(df)


def benchmark_results_md(langs: list[str], results: list[BenchmarkResults]) -> str:
    """Generates markdown with aggregated Benchmark results."""
    agg = TableAggregator(results)
    md_lines = []

    md_lines.append("# Benchmark Results\n")

    # Individual language results
    for lang in langs:
        df = agg.aggregate_by_name(lang)
        md_lines.append(f"## Benchmark results for `{lang}`\n")
        md_lines.append(df.to_markdown(index=False))
        md_lines.append("\n")

    # Aggregated duration results
    md_lines.append("## Benchmark aggregated `duration` results\n")
    df = agg.aggregate_by_field("duration_sec", langs)
    md_lines.append(df.to_markdown())
    md_lines.append("\n")

    # Aggregated memory results
    md_lines.append("## Benchmark aggregated `memory` results\n")
    df = agg.aggregate_by_field("pick_mem_mb", langs)
    md_lines.append(df.to_markdown())
    md_lines.append("\n")

    return "\n".join(md_lines)


def save_text(text: str, file_name: str) -> None:
    with open(file_name, "w") as f:
        f.write(text)
