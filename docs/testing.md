
### Testing


#### Test tools

* [pytest](https://docs.pytest.org/en/stable/)
* [nox](https://github.com/wntrblm/nox)
* [flake8](https://github.com/pycqa/flake8)
* [mypy](https://www.mypy-lang.org/)


#### Running tests

Mailnagger unit tests are located in `tests` directory.

To run tests development environment, install pytest python package.
Then run command
```
    python3 -m pytest
```
in main directory.

Whole tests set can be run with command 
```
    nox
```
or
```
    nox -R
```
which skips installing and is faster.

Nox runs

* unit tests using pytest,
* flake8 to do static code checks and
* mypy to make static type checking.

