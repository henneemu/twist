# twister.twist()

Version 0.10.0

## Overview

  `twister.twist(*iterables, **kwargs)`

Function as enhanced `zip()` to control aggregating elements from iterables.

This `twister` module provides the `twist()` function which has the following features:
  * upper compatible to `zip()` or `zip_longest()` except returns a generator.
  * can select iterables to aggregate elements from via the `send()` method.
  * can call `send()` instead of `next()` on generator in argument iterables.

Requirement: **Python 3.0 or above.**



## Compatibility to zip()

When no `send()` method called on, works just like the built-in `zip()` function.

```python
from twister import twist

tw = twist(range(4), range(5))

for a, b in tw:
    print(a, b)
```

    0 0
    1 1
    2 2
    3 3


If the `longest` argument is `True`, works just like `itertools.zip_longest()` when no `send()`.



## The send(value) Method

The way of aggregating elements from iterables can be changed by passing their indices in argument iterables to the `value` argument of the `send(value)` method.

```python
tw = twist(range(4), range(5))

for a, b in tw:
    print(a, b)

    if a == 1:
        tw.send(0)   # tw.send(0) -> (range(4), range(8))[0]
```

    0 0
    1 1
    2 1
    3 2


For each element of iterables not aggregated from, the same element before are used.

How to select iterables:

  * To select `i`th iterable, pass `i` to the `value` argument of the `send(value)` method. ---- Ex.) `tw.send(0)`

  * To select multiple iterables, pass iterable of `i` except for tuple. ---- Ex.) `tw.send([0, 1])`, `tw.send(range(1:3))`.

  * To select no iterable, pass empty iterable. ---- Ex.) `tw.send([])`.

Negative indices are available. The evaluation order of aggregating elements is guaranteed by the order of indices.

Those indices are only used at the next aggregation. When calling `send()` twice or more, only the last call works.

If `(i, x)` used instead of `i`, calls `send(x)` instead of `next()` on the `i`th iterable which must be generator.

```python
def gen_f(x=None):
    while True:
        x = (yield x)


tw = twist(range(4), gen_f())

for n, x in tw:
    print(n, x)

    if n == 1:
        tw.send([0, (1, "send")])
```

    0 None
    1 None
    2 send
    3 None


However, exactly when `x` is `None`, or `(i, None)` instead of `i`, calls `next()`.



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
              If True, works like itertools.zip_longest() when no send().<br>
          </blockquote>
          <b>fillvalue</b><i> : Any, default None</i><br>
          <blockquote>
              Works just like in itertools.zip_longest().
          </blockquote>
          <b>working</b><i> : set or iterable, default None</i><br>
          <blockquote>
              Set of index of iterator to be treated as not exhausted. If None, set of all indices.
          </blockquote>
          <b>items</b><i> : list or iterable, default None</i><br>
          <blockquote>
              List of initial value used before aggregating the first element from each iterable. The length must be the same as iterables. If None, list of fillvalue.
          </blockquote>
          <b>cues</b><i> : the same as passed to the value argument of the send(value) method, default None</i><br>
          <blockquote>
              Works as if passed from the send(value) method before aggregating at the start. If None, working.
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
