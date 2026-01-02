from ax_lang.benchmark.runner import (
    benchmark_results_md,
    print_benchmark_results,
    run_benchmarks,
    save_text,
)

if __name__ == "__main__":
    langs = ["python", "axlang"]
    tests = ["factorial", "fibonacci", "higher_order", "simple", "switch"]
    results = run_benchmarks(langs, tests)

    print_benchmark_results(langs, results)

    md_text = benchmark_results_md(langs, results)
    save_text(md_text, "RESULTS.md")
