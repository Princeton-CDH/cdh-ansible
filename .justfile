set default-list := true

docs:
    uv run --extra docs sphinx-build -b html -W --keep-going docs/ docs/_build/

clean-docs:
    rm -rf docs/_build
    @just docs
