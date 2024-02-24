# ribs

Report comparisons and other CPU-bound logic, implemented in Rust to speed up usages in Python from our other repositories:
- [`worker`](https://github.com/codecov/worker)
- [`codecov-api`](https://github.com/codecov/codecov-api)

It uses [pyo3](https://pyo3.rs) for bindings and [maturin](https://www.maturin.rs/) for packaging.

Testing:
```
$ cargo test --no-default-features
```
