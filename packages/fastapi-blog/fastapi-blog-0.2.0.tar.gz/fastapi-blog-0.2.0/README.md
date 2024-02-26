# FastAPI Blog README

A blog engine for FastAPI

## Releasing a new version

```
pip install -U build
python -m build
pip install -U twine
python -m twine upload dist/*
make tag
```