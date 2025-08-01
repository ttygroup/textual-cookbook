
from __future__ import annotations
from pathlib import Path
import importlib.util
from typing import cast
from textual.app import App
import pytest


EXAMPLES_DIR = Path(__file__).parent.parent / "examples"


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
        pytest.fail(f"Example {example_file.name} does not subclass App", pytrace=False)

    return AppClass


def make_test(example_file: Path):

    async def proto_test():  

        AppClass = None
        AppClass = get_app_class(example_file)
        assert AppClass is not None, f"(proto_test) App class not found in {example_file}"

        app = AppClass()
        async with app.run_test() as pilot:
            await pilot.pause()
            assert app.screen
            await pilot.exit(None) 

    return proto_test


for example_file in EXAMPLES_DIR.rglob("*.py"):

    proto_test = make_test(example_file)    
    test_name = f"test_script_{example_file.stem}"
    proto_test.__name__ = test_name
    globals()[test_name] = proto_test
