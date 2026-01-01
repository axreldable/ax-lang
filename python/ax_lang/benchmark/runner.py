from ax_lang.benchmark.aggregator import TableAggregator
from ax_lang.benchmark.benchmark import BenchmarkRunner

if __name__ == "__main__":
    tests = ["factorial", "fibonacci", "higher_order", "simple", "switch"]

    # todo:
    #     finish visual
    #     integrate to ci
    #     have it as a part of docs
    runner = BenchmarkRunner(["python"], tests)
    # runner = BenchmarkRunner(["axlang"], tests)
    results = runner.run()
    agg = TableAggregator([results])
    agg.aggregate()
