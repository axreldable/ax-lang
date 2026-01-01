from ax_lang.benchmark.aggregator import TableAggregator
from ax_lang.benchmark.benchmark import BenchmarkRunner

if __name__ == "__main__":
    tests = ["factorial", "fibonacci", "higher_order", "simple", "switch"]

    # todo:
    #     finish TableAggregator
    #     integrate to ci
    #     have it as a part of docs
    runner = BenchmarkRunner("python", True)
    # runner = BenchmarkRunner(["axlang"], tests)
    results = runner.run(tests)
    agg = TableAggregator([results])
    agg.aggregate()
