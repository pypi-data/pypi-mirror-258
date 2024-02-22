# Puffling

## Usage

See the [dummy project](https://github.com/astral-sh/puffling/blob/main/tests/dummy/pyproject.toml) for a minimum
example.

### Debugging config-settings

Puffling writes received `config-settings` into distributions:

```
$ cd tests/dummy
$ puffling build -Ctest=1 -Ctest=2 -Cbird=yes
[sdist]
dist/dummy-1.0.0.tar.gz

[wheel]
dist/dummy-1.0.0-py3-none-any.whl

$ tar -xvf dist/dummy-1.0.0.tar.gz
x dummy-1.0.0/src/dummy/__init__.py
x dummy-1.0.0/.gitignore
x dummy-1.0.0/pyproject.toml
x dummy-1.0.0/PKG-INFO
x dummy-1.0.0/CONFIG-SETTINGS

$ cat dummy-1.0.0/CONFIG-SETTINGS
{
  "test": [
    "1",
    "2"
  ],
  "bird": "yes"
}
```

## Acknowlegements

This is a fork of [hatchling](https://github.com/pypa/hatch/tree/master/backend) by Ofek Lev which is available under the [MIT license](https://github.com/pypa/hatch/blob/a5f62c2f298e7da39f1ca19877a362e8e97c2c24/backend/LICENSE.txt).

This project only exists for test purposes and should not be used to build projects in production.