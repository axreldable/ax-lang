import subprocess
from abc import ABC, abstractmethod

from ax_lang.exceptions import BenchmarkError


class LanguageExecutor(ABC):
    def _run(self, args: list[str], file: str) -> str:
        result = subprocess.run(
            [*args, file],
            capture_output=True,
            text=True,  # decode bytes -> str automatically
            check=True,
        )

        output = result.stdout.strip()
        return output

    def run(self, full_file_path: str) -> str:
        cli_command_with_args = [self.lang_cli_runner()] + self.lang_cli_runner_args()
        return self._run(cli_command_with_args, full_file_path)

    @abstractmethod
    def lang_cli_runner(self) -> str:
        pass

    @abstractmethod
    def lang_cli_runner_args(self) -> list[str]:
        pass

    @abstractmethod
    def lang_extension(self) -> str:
        pass

    def get_lang_version(self) -> str:
        return "v1"


class PythonExecutor(LanguageExecutor):
    def lang_cli_runner_args(self) -> list[str]:
        return []

    def lang_cli_runner(self) -> str:
        return "python"

    def lang_extension(self) -> str:
        return "py"


class AxLangExecutor(LanguageExecutor):
    def lang_cli_runner_args(self) -> list[str]:
        return ["file"]

    def lang_cli_runner(self) -> str:
        return "axlang"

    def lang_extension(self) -> str:
        return "ax"


class LanguageExecutorFactory:
    @staticmethod
    def get(name) -> LanguageExecutor:
        if name == "python":
            return PythonExecutor()
        elif name == "axlang":
            return AxLangExecutor()
        else:
            raise BenchmarkError(f"Unsupported language `{name}`!")
