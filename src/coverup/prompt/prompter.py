import abc
import typing as T
from pathlib import Path
from ..utils import lines_branches_do
from ..segment import CodeSegment


class Prompter(abc.ABC):
    """Interface for a CoverUp prompter."""

    def __init__(self, cmd_args):
        self.args = cmd_args


    @abc.abstractmethod
    def initial_prompt(self, segment: CodeSegment) -> T.List[dict]:
        """Returns initial prompt(s) for a code segment."""


    @abc.abstractmethod
    def error_prompt(self, segment: CodeSegment, error: str) -> T.List[dict] | None:
        """Returns prompts(s) in response to an error."""


    @abc.abstractmethod
    def missing_coverage_prompt(self, segment: CodeSegment,
                                missing_lines: set, missing_branches: set) -> T.List[dict] | None:
        """Returns prompts(s) in response to the suggested test(s) lacking coverage."""


    def get_functions(self) -> T.List[T.Callable]:
        """Returns a list of functions to be made available to the LLM.
           Each function's docstring must consist of its schema in JSON format."""
        return []


def get_module_name(src_file: Path, src_dir: Path) -> str:
    # assumes both src_file and src_dir Path.resolve()'d
    try:
        relative = src_file.relative_to(src_dir)
        return ".".join((src_dir.stem,) + relative.parts[:-1] + (relative.stem,))
    except ValueError:
        return None  # not relative to source


def mk_message(content: str, *, role="user") -> dict:
    return {
        'role': role,
        'content': content
    }
