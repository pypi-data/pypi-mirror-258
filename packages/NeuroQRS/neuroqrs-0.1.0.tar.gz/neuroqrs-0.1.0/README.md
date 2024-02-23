# NeuroQRS
NeuroQRS (Neuro Query Recommendation System) is Faiss + LLM based query recommender with auto-improvement using closed feedback loop!

It works by first using faiss to check for any similar previous search, if not then it builds one using genai! XD

## Installation

[Coming Soon] Install the ``neuroqrs`` package with [pip](https://pypi.org/project/neuroqrs):

```console
$ pip install neuroqrs
```

Or install the latest package directly from github

```console
$ pip install git+https://github.com/searchX/neuroqrs
```

Example Usage
-------------
```python
from neuroqrs.main import NeuroQRS
neuroqrs = NeuroQRS()
async def main():
    ... statements
import asyncio
asyncio.run(main())
```

1. Force fetch documents from chatgpt api (index + search mode)
```python
print(await neuroqrs.query_and_index("nike casual ", "nike", {}, {}))
# Output: ['nike casual black', 'nike casual men', 'nike casual white', 'nike casual wear', 'nike casual shoes']
```

2. Only do quick query without reindexing/genai
```python
print(await neuroqrs.quick_query("nike casual ", "nike"))
# Output: ['nike casual black', 'nike casual men', 'nike casual white', 'nike casual wear', 'nike casual shoes']
```

3. Try quick query, if data not avaliable then index and get results (combines above two)
```python
print(await neuroqrs.query_maybe_index("nike casual ", "nike", {}, {}))
# Output: ['nike casual black', 'nike casual men', 'nike casual white', 'nike casual wear', 'nike casual shoes']
```

Please look into official docs for more information - https://searchx.github.io/neuroqrs/