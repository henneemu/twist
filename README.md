# twister.twist()

## Overview

Enables to iterate over iterables together and independently of each other.  

    twister.twist(*iterables, **kwargs)

This `twister` module provides `twist()` function which has the following features:
  * takes iterables as argument and creates a generator.
  * upper compatible to `zip()` or `zip_longest()` except for the type of instance.
  * able to select from which iterators to aggregate elements via the `send()` method.

**Requirement: Python 3.0 or above.**

## Example

```python
from twister import twist

tw = twist(range(4), range(8))

for a, b in tw:
    print(a, b)
    
    if b == 1:
        tw.send([1, 1])   # tw.send([1]) selects (range(4), range(8))[1].

```

    0 0
    1 1
    1 3
    2 4
    3 5
    

## send(value)

To select iterators, pass keys of them to the value argument of the `send(value)` method as following:

  * `key` or `(key, thing)` ----  ex.) `tw.send(0)`, `tw.send((1, "a"))`
    
  * iterable, except for tuple, of two above ----  ex.) `tw.send([0, (1, "a")])`
    
  * empty iterable ---- ex.) `tw.send([])`

Without calling `send()`, works the same as `zip()`, or `itertools.zip_longest()` when the `longest` argument is `True`.

Negative key values are available. The evaluation order of aggregating elements is guaranteed by the order of keys. 

When the `longest` argument is `True`, passing keys of exhausted iterators raises `KeyError` exception.

If `(key, thing)` instead of `key`, calls `send(thing)` instead of `next()` on the argument iterator, which is supposed to be generator. For example:

```python
def gen_f(x=None):
    while True:
        x = (yield x)
        
        
tw = twist(range(4), gen_f())

for n, s in tw:
    print(n, s)
    
    if n == 1:
        tw.send([0, (1, "send")])
```

    0 None
    1 None
    2 send
    3 None


However, exactly when `thing` is `None`, calls `next()`.


## Parameters and Returns

    twister.twist(*iterables, longest=False, fillvalue=None, working=None, items=None, move=None)

<table>
  <tbody>
    <tr>
      <td>
          <b>Parameters:</b>
      </td>
      <td align="left">
          <b>iterables</b><i> : iterable</i><br>
          <blockquote>
              Variadic arguments.<br>
          </blockquote>
          <b>longest</b><i> : bool, default False</i><br>
          <blockquote>
              If True, works like itertools.zip_longest() when no send() called.<br>
          </blockquote>
          <b>fillvalue</b><i> : Any, default None</i><br>
          <blockquote>
              Works the same as in itertools.zip_longest().
          </blockquote>
          <b>working</b><i> : set or iterable, default None</i><br>
          <blockquote>
              Keys of the iterators to be treated as not exhausted. If None, set of all keys.
          </blockquote>
          <b>items</b><i> : list or iterable, default None</i><br>
          <blockquote>
              List of the initial values used before aggregating the first elements from the iterators. The length must be the same as of iterables. If None, list of fillvalue.
          </blockquote>
          <b>move</b><i> : the same as passed to the value argument of the send(value) method, default None</i><br>
          <blockquote>
              Keys of the iterators from which to aggregate elements at the first next(). If None, working.
          </blockquote>
      </td>
    </tr>
    <tr>
      <td>
          <b>Returns:</b>
      </td>
      <td align="left">
          <b>_twist</b><i> : generator</i><br>
          <blockquote>
              send(value) is available. twist() isn't generator function but calls a generator function _twist() inside.
          </blockquote>
      </td>
    </tr>
  </tbody>
</table>

## License

Distributed under the MIT License.
