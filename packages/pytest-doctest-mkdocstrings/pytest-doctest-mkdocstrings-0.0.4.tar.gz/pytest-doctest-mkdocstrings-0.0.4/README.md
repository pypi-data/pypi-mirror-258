# pytest-doctest-mkdocstrings

A pytest plugin that allows you to use doctest and enclose your example code blocks in ` ``` ` codeblocks (e.g. when building documentation with mkdocs and mkdocstring).

Usually this docstring would fail doctest:

```
    """
    A function description

    Examples:
    --------
    ```
    >>> x = 1
    >>> x
    1
    ```
    """
```

As doctest looks for the output
```
Expected:
    1
    ```
Got:
    1
```

This plugin works by mockeypatching doctests parser when pytest begins each test session and including ` ``` ` as an identifier of the end of an expected result (a `want`).

It only works when doctest is invoked via pytest, not when invoking doctest directly

If you have code examples or expected results which actually contain ` ``` ` then you'll need to re-write them.

## Usage

1. **Strongly recommended** to set up a virtual environment first! (e.g.. `python3 -m venv .venv`, `. .venv/bin/activate`)
1. Install with `pip install pytest-doctest-mkdocstrings`
1. Run pytest: `pytest --doctest-modules`

You can also add the following to your `pyproject.toml` so that pytest always runs doctests:
```
[tool.pytest.ini_options]
addopts = [
    "--doctest-modules",
]
```