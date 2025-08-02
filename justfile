# Install the package
install:
	uv sync

cook:
	uv run recipe_runner.py

cook-dev:
	uv run textual run --dev recipe_runner.py 

# Runs ruff, exits with 0 if no issues are found
lint script:
  @uv run ruff check recipes/{{script}}

# Runs mypy, exits with 0 if no issues are found
typecheck script:
  @uv run mypy recipes/{{script}}
  @uv run basedpyright recipes/{{script}}

# Runs black
format script:
  @uv run black recipes/{{script}}

# Runs pytest using whatever version of Textual is installed
test:
  @uv run pytest tests -v

# Run the Nox testing suite for comprehensive testing.
# This will run pytest against all versions of Textual and Python
# specified in the noxfile.py
nox:
  nox
  
# Remove all caches and temporary files
clean:
  find . -name "*.pyc" -delete
  rm -rf .mypy_cache
  rm -rf .ruff_cache
  rm -rf .nox

# Remove the virtual environment and lock file
del-env:
  rm -rf .venv
  rm -rf uv.lock

nuke: clean del-env
  @echo "All build artifacts and caches have been removed."

# Removes all environment and build stuff
reset: nuke install
  @echo "Environment reset."