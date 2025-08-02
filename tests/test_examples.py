"""Dynamic test function creator script for Textual Cookbook recipes

This script dynamically creates test functions for each example
found in the recipes directory.

How it works:
1. It scans the `recipes` directory for Python files.
2. For each file, it attempts to load the module and find a subclass of `App`
    (the `get_app_class` function).
3. If a subclass of `App` cannot be found or loaded, the test will fail.
4. The script uses a function factory (`make_test`) to create a test
    function for each example, which is then registered in the global namespace.
5. Pytest will discover these functions and treat every example as a separate test case.
"""

from __future__ import annotations
from pathlib import Path
import importlib.util
from typing import cast
from textual.app import App
import pytest


EXAMPLES_DIR = Path(__file__).parent.parent / "recipes"


def get_app_class(path: Path) -> type[App[None]] | None:

    module_name = f"{path.name}"
    
    ### ~ Stage 1: Load the module spec ~ ###
    try:
        spec = importlib.util.spec_from_file_location(module_name, path)
    except Exception:
        pytest.fail(f"Failed to load spec for app {module_name}", pytrace=False)
    else:
        if spec is None or spec.loader is None:
            pytest.fail(f"Failed to load spec for app {module_name}", pytrace=False)
    
    ### ~ Stage 2: Load module using the spec ~ ###
    try:
        
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except Exception as e:
        # breakpoint()
        pytest.fail(f"Failed to load module for app {module_name} with error: {e}", pytrace=False)
    
    ### ~ Stage 3: Retrieve the app class from module ~ ###
    candidates = {name: obj for name, obj in module.__dict__.items()}
    AppClass = None
    try:
        for _name, obj in candidates.items():
            if isinstance(obj, type):
                if issubclass(obj, App) and obj is not App:
                    AppClass = cast(type[App[None]], obj)
                    break
    except StopIteration:
        pytest.fail(f"Failed to find a valid App subclass in {module_name}", pytrace=False)
    except Exception:
        pytest.fail(f"Error while searching for App subclass in {module_name}", pytrace=False)

    if not issubclass(AppClass, App):   # type: ignore (NOT UNNECESSARY)
        pytest.fail(f"Example {recipe_file.name} does not subclass App", pytrace=False)

    return AppClass


def make_test(recipe_file: Path):
    "The test function factory"

    async def proto_test():  

        AppClass = None
        AppClass = get_app_class(recipe_file)
        assert AppClass is not None, f"(proto_test) App class not found in {recipe_file}"

        app = AppClass()
        async with app.run_test() as pilot:
            await pilot.pause()
            assert app.screen
            await pilot.exit(None) 

    return proto_test


for recipe_file in EXAMPLES_DIR.rglob("*.py"):

    proto_test = make_test(recipe_file)    
    test_name = f"test_{recipe_file.stem}"
    proto_test.__name__ = test_name
    globals()[test_name] = proto_test
