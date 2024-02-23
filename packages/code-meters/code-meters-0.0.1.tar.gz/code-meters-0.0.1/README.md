# code-meters -- Monitor resource usage of Python code

## Example

As a context manager:

```python
from meters import ResourceMeter

with ResourceMeter("Data Processing"):
    data = [x**2 for x in range(1000000)]
# Data Processing: wall time: 0.24156 s (241560 microseconds), CPU time: 0.226669 s (226669 microseconds), memory: 92925952 bytes (88.6211 MiB)
```

As a function decorator:

```python
from meters import metered

@metered
def process(n):
    return sum([x**3 for x in range(n)])

print(process(1000000))
# process: wall time: 0.310323 s (310323 microseconds), CPU time: 0.291285 s (291285 microseconds), memory: 152657920 bytes (145.586 MiB)
# 249999500000250000000000
```