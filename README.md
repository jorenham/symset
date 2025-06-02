# symset

## Development

Install the [maturin import hook](https://www.maturin.rs/import_hook.html) in the uv project:

```shell
uv run -m maturin_import_hook site install --detect-uv
```

Linting, formatting, typechecking, and testing:

```shell
uv run ruff check
uv run ruff format
uv run basedpyright
uv run pytest
```
