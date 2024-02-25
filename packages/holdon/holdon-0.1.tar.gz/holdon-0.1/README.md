# holdon

Holdon, pronounced "hold'n," is a lightweight Python progress bar library with a simple API.

```haskell
$ pip install holdon
```

## Get Started

Holdon is like [tqdm](https://pypi.org/project/tqdm), just wrap `progress()` around an iterator and we're good to go.

```python
import time
from holdon import progress

for i in progress(range(100)):
    time.sleep(0.1)
```

```python
 23.0% ━━━╸━━━━━━━━━━━━━━━━  23 / 100 (9.9it/s)
```

<br />

If you do not have any iterator, you can use <kbd>class</kbd> `RawProgress()` and update everything manually. To learn more, refer to the documentation below.

## Documentation

Minimal, lol.

### <kbd>def</kbd> progress()

```python
progress(
    iterator: Iterator, 
    *, 
    width: Optional[int] = None, 
    size: Optional[int] = None,
    unit: Literal["it", "bytes"] = "it"
) -> Iterator[Any]
```

Creates a progress bar.

**Example:**

You can wrap `progress()` around any iterator:

```python
for i in progress(range(100)):
    ... # do your work here
```

You can also wrap it around a custom iterator, but you'll need to specify its total iterations.

```python
words = ["cheese", "is", "good", "but", "i'm", "lactose", "intolerant"]

def word_it():
    for word in words:
        yield word + " "

for word in progress(word_it(), size=len(words)):
    ... # do your work here
```

**Args:**

- iterator (`Iterator`): The iterator. For instance, `range` or `list`.
- width (`int`, *optional*): Width of the progress bar. Defaults to 50.
- size (`int`, *optional*): Size of the iterator or the `len()` of the iterator.
- unit (`Literal["it", "bytes"]`): Unit. Could be one of: "it" (iterations) or "bytes" (bytes).


### <kbd>class</kbd> RawProgress

<details>
    <summary><b>Attributes</b></summary>
<div>

- <kbd>const</kbd> fmt (`str`): Progress bar format.
- <kbd>slots</kbd> width (`int`): Progress bar width.
- <kbd>slots</kbd> size (`int`): Total iterations as "size."
- <kbd>slots</kbd> unit (`Literal["it", "bytes"]`): Unit. Could be one of: "it" (iterations) or "bytes" (bytes).

</p>
</details>

<br />

```python
__init__(
    self, 
    width: int = 50, 
    size: int = 100,
    unit: Literal["it", "bytes"] = "it"
)
```

The progress bar.

**Example:**

A minimal example:

```python
rp = RawProgress()

for i in range(500):
    rp.advance(1)
```

You can also change the `unit` parameter to `"bytes"` and specify the total content length (see [`requests`](https://pypi.org/project/requests)) to indicate download progress:

```python
rp = RawProgress(
    unit="bytes",
    size=int(http_response.headers['Content-Length'])
)

for chunk in http_response.iter_content():
    rp.advance(len(chunk))
```

**Args:**

- width (`int`): Progress bar width.
- size (`int`): Total iterations as "size."
- unit (`Literal["it", "bytes"]`): Unit. Could be one of: "it" (iterations) or "bytes" (bytes).


#### <kbd>def</kbd> RawProgress.advance()

```python
advance(self, i: int = 1) -> None
```

Advance.

**Args:**

- i (`int`): Advance size.

#### <kbd>def</kbd> RawProgress.render()

```python
render(self) -> None
```

Renders the progress bar.

***

(c) 2024 AWeirdDev
