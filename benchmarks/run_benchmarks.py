#!/usr/bin/env python3
"""
Benchmark runner for comparing AxLang and Python performance.

This script runs equivalent benchmarks in both AxLang and Python,
measures execution time and memory usage, and generates comparison reports.
"""

import json
import statistics
import subprocess
import sys
import time
from pathlib import Path
from typing import List, Tuple


class BenchmarkResult:
    def __init__(
        self,
        name: str,
        axlang_time: float,
        python_time: float,
        axlang_memory: float = 0,
        python_memory: float = 0,
    ):
        self.name = name
        self.axlang_time = axlang_time
        self.python_time = python_time
        self.axlang_memory = axlang_memory
        self.python_memory = python_memory
        self.ratio = axlang_time / python_time if python_time > 0 else 0

    def __repr__(self):
        return (
            f"BenchmarkResult(name={self.name}, "
            f"axlang={self.axlang_time:.4f}s, "
            f"python={self.python_time:.4f}s, "
            f"ratio={self.ratio:.2f}x)"
        )


def run_command(cmd: List[str], timeout: int = 60) -> Tuple[bool, float]:
    """
    Run a command and measure its execution time.

    Args:
        cmd: Command to execute as a list of strings
        timeout: Maximum time to wait for command completion

    Returns:
        Tuple of (success: bool, execution_time: float)
    """
    try:
        start_time = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        end_time = time.time()

        if result.returncode != 0:
            print(f"Error running {' '.join(cmd)}:")
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
            return False, 0.0

        return True, end_time - start_time
    except subprocess.TimeoutExpired:
        print(f"Timeout running {' '.join(cmd)}")
        return False, 0.0
    except Exception as e:
        print(f"Exception running {' '.join(cmd)}: {e}")
        return False, 0.0


def run_benchmark(
    name: str, axlang_file: Path, python_file: Path, iterations: int = 3
) -> BenchmarkResult:
    """
    Run a single benchmark in both AxLang and Python.

    Args:
        name: Name of the benchmark
        axlang_file: Path to AxLang benchmark file
        python_file: Path to Python benchmark file
        iterations: Number of times to run each benchmark for averaging

    Returns:
        BenchmarkResult object with timing information
    """
    print(f"\nRunning {name}...")

    # Run AxLang benchmark
    axlang_times = []
    for i in range(iterations):
        success, exec_time = run_command(["axlang", "file", str(axlang_file)])
        if success:
            axlang_times.append(exec_time)
            print(f"  AxLang iteration {i+1}: {exec_time:.4f}s")
        else:
            print(f"  AxLang iteration {i+1}: FAILED")

    # Run Python benchmark
    python_times = []
    for i in range(iterations):
        success, exec_time = run_command([sys.executable, str(python_file)])
        if success:
            python_times.append(exec_time)
            print(f"  Python iteration {i+1}: {exec_time:.4f}s")
        else:
            print(f"  Python iteration {i+1}: FAILED")

    # Calculate median times (more robust than mean for timing)
    axlang_time = statistics.median(axlang_times) if axlang_times else 0.0
    python_time = statistics.median(python_times) if python_times else 0.0

    return BenchmarkResult(name, axlang_time, python_time)


def generate_markdown_report(results: List[BenchmarkResult], output_path: Path):
    """
    Generate a markdown report of benchmark results.

    Args:
        results: List of BenchmarkResult objects
        output_path: Path where to save the markdown report
    """
    with open(output_path, "w") as f:
        f.write("# AxLang vs Python Benchmark Results\n\n")
        f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write("## Summary\n\n")
        f.write("| Benchmark | AxLang (s) | Python (s) | Ratio (AxLang/Python) |\n")
        f.write("|-----------|------------|------------|----------------------|\n")

        for result in results:
            f.write(
                f"| {result.name} | {result.axlang_time:.4f} | "
                f"{result.python_time:.4f} | {result.ratio:.2f}x |\n"
            )

        f.write("\n## Detailed Results\n\n")

        for result in results:
            f.write(f"### {result.name}\n\n")
            f.write(f"- **AxLang**: {result.axlang_time:.4f}s\n")
            f.write(f"- **Python**: {result.python_time:.4f}s\n")
            f.write(f"- **Ratio**: {result.ratio:.2f}x ")

            if result.ratio > 1:
                f.write(f"(AxLang is {result.ratio:.2f}x slower)\n")
            elif result.ratio < 1:
                f.write(f"(AxLang is {1/result.ratio:.2f}x faster)\n")
            else:
                f.write("(approximately equal)\n")

            f.write("\n")

        # Add statistics
        if results:
            avg_ratio = statistics.mean([r.ratio for r in results])
            f.write("\n## Overall Statistics\n\n")
            f.write(f"- **Average slowdown**: {avg_ratio:.2f}x\n")
            f.write(
                f"- **Fastest benchmark**: {min(results, key=lambda r: r.ratio).name} "
                f"({min(results, key=lambda r: r.ratio).ratio:.2f}x)\n"
            )
            f.write(
                f"- **Slowest benchmark**: {max(results, key=lambda r: r.ratio).name} "
                f"({max(results, key=lambda r: r.ratio).ratio:.2f}x)\n"
            )


def generate_json_report(results: List[BenchmarkResult], output_path: Path):
    """
    Generate a JSON report of benchmark results for machine processing.

    Args:
        results: List of BenchmarkResult objects
        output_path: Path where to save the JSON report
    """
    data = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "benchmarks": [
            {
                "name": r.name,
                "axlang_time": r.axlang_time,
                "python_time": r.python_time,
                "ratio": r.ratio,
            }
            for r in results
        ],
    }

    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)


def main():
    """Main entry point for the benchmark runner."""
    print("=" * 60)
    print("AxLang vs Python Benchmark Suite")
    print("=" * 60)

    # Get benchmark directory
    benchmark_dir = Path(__file__).parent
    axlang_dir = benchmark_dir / "axlang"
    python_dir = benchmark_dir / "python"
    results_dir = benchmark_dir / "results"
    results_dir.mkdir(exist_ok=True)

    # Define benchmarks to run
    benchmarks = [
        ("Fibonacci (n=25)", "fibonacci.ax", "fibonacci.py"),
        ("Factorial (n=1000)", "factorial.ax", "factorial.py"),
        ("Prime Numbers (limit=1000)", "prime_numbers.ax", "prime_numbers.py"),
        ("Nested Loops (n=100)", "nested_loops.ax", "nested_loops.py"),
        ("Function Calls (n=10000)", "function_calls.ax", "function_calls.py"),
        ("List Operations (n=1000)", "list_operations.ax", "list_operations.py"),
        ("Recursion - Ackermann(3,6)", "recursion.ax", "recursion.py"),
    ]

    # Run all benchmarks
    results = []
    for name, axlang_file, python_file in benchmarks:
        axlang_path = axlang_dir / axlang_file
        python_path = python_dir / python_file

        if not axlang_path.exists():
            print(f"Warning: AxLang file not found: {axlang_path}")
            continue
        if not python_path.exists():
            print(f"Warning: Python file not found: {python_path}")
            continue

        result = run_benchmark(name, axlang_path, python_path)
        results.append(result)

    # Generate reports
    print("\n" + "=" * 60)
    print("Generating reports...")

    markdown_path = results_dir / "benchmark_report.md"
    json_path = results_dir / "benchmark_results.json"

    generate_markdown_report(results, markdown_path)
    generate_json_report(results, json_path)

    print("\nReports generated:")
    print(f"  - Markdown: {markdown_path}")
    print(f"  - JSON: {json_path}")

    # Print summary to console
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for result in results:
        print(f"{result.name:40} {result.ratio:6.2f}x")

    if results:
        avg_ratio = statistics.mean([r.ratio for r in results])
        print("=" * 60)
        print(f"{'Average slowdown:':40} {avg_ratio:6.2f}x")
        print("=" * 60)


if __name__ == "__main__":
    main()
