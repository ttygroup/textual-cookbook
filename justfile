# Install the package
install:
	uv sync

run script:
	uv run {{script}}

run-dev script:
	uv run textual run --dev {{script}}

# Runs ruff, exits with 0 if no issues are found
lint:
  @uv run ruff check examples || (echo "Ruff found issues. Please address them." && exit 1)

# Runs mypy, exits with 0 if no issues are found
typecheck:
  @uv run mypy examples || (echo "Mypy found issues. Please address them." && exit 1)
  @uv run basedpyright examples || (echo "BasedPyright found issues. Please address them." && exit 1)

# Runs black
format:
  @uv run black examples

test:
  @uv run pytest tests -v

# Runs ruff, mypy, and black
all-checks: lint typecheck format test
  echo "All checks passed."

# Run the Nox testing suite for comprehensive testing
nox:
  nox

# Remove build/dist directories and pyc files
clean:
  rm -rf build dist
  find . -name "*.pyc" -delete

# Remove tool caches
clean-caches:
  rm -rf .mypy_cache
  rm -rf .ruff_cache
  rm -rf .nox

# Remove the virtual environment and lock file
del-env:
  rm -rf .venv
  rm -rf uv.lock

nuke: clean clean-caches del-env
  @echo "All build artifacts and caches have been removed."

# Removes all environment and build stuff
reset: nuke install
  @echo "Environment reset."