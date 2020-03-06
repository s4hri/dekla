## Pretty json
```python
>>> import json
>>>
>>> your_json = '["foo", {"bar":["baz", null, 1.0, 2]}]'
>>> parsed = json.loads(your_json)
>>> print(json.dumps(parsed, indent=4, sort_keys=True))
[
    "foo", 
    {
        "bar": [
            "baz", 
            null, 
            1.0, 
            2
        ]
    }
]
```


```python
with open('filename.txt', 'r') as handle:
    parsed = json.load(handle)
```