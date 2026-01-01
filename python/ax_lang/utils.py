from pathlib import Path


def get_project_root() -> Path:
    return Path(__file__).parent.parent


def get_repo_root() -> Path:
    return get_project_root().parent


def get_benchmark_root() -> Path:
    return get_repo_root() / "benchmarks"


def get_examples_root() -> Path:
    return get_repo_root() / "examples"
