# pylibsmeta-search

Simple Python library to search and retrieve metadata from [pylibsmeta](https://github.com/tushkum34-cloud/pylibsmeta).

---

## Installation

```bash
pip install pylibsmeta-search
```

---

## Usage

### Basic Search

```python
from pylibsmeta_search import PyLibsMetaSearch

# Search for requests library v2.31.0
result = PyLibsMetaSearch.search("requests", "2.31.0")
print(result)
```

---

### Get Functions

```python
functions = PyLibsMetaSearch.get_functions("requests", "2.31.0")
print(functions)
```

---

### Get Classes

```python
classes = PyLibsMetaSearch.get_classes("requests", "2.31.0")
print(classes)
```

---

### Get All Symbols

```python
symbols = PyLibsMetaSearch.get_symbols("requests", "2.31.0")
print(symbols)
```

---

## API Reference

### search(library_name, version=None)

Search for a library in pylibsmeta database.

- library_name (str)
- version (str, optional)

Returns: dict

---

### get_symbols(library_name, version=None)

Get raw symbols/metadata.

---

### get_functions(library_name, version=None)

Get list of functions.

---

### get_classes(library_name, version=None)

Get dictionary of classes.

---

### encode_version(version)

Example:
"2.31.0" → "v000200310000"

---

## Response Format

```python
{
    'library': 'requests',
    'version': '2.31.0',
    'status': 'found',
    'filename': 'requests_v000200310000.json',
    'metadata': {}
}
```

---

## Use Cases

- IDE Autocomplete  
- Documentation Generation  
- Static Analysis  
- LLM Training  

---

## Requirements

```
requests>=2.28.0
```

---

## License

MIT
