#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Function as enhanced zip() to control aggregating elements from iterables.

This module provide twist() function which provides the following features:
  * upper compatible to `zip()` or `zip_longest()` except returns a generator.
  * can select iterables to aggregate elements from via the `send()` method.
  * can call `send()` instead of `next()` on generator in argument iterables.

Version 0.10.0
"""


def _twist(*iterators, longest, fillvalue, working, elems, cues):
    """Function creating the generator witch iterates over iterables.

    Separated from the main function to check the arguments before returns to
    the caller, since generators start execution only after called next() on.

    elems       each of them is the last element aggregated from iterables.
    i           index for the iterable to select in the argument tuple.
    x           object to pass to generator in iterables by calling send() on.
    cues        i or (i, x) or iterable of them except for tuple.
    """

    sentinel = object()
    len_iter = len(iterators)

    while True:

        #
        # Aggregating elements from the selected iterators
        #

        if isinstance(cues, int) or isinstance(cues, tuple):
            cues = [cues]
        else:
            cues = list(cues)

        for i in cues:

            # i or (i, x) -> i, x
            if isinstance(i, int):
                x = None
            elif isinstance(i, tuple):
                i, x = i
            else:
                raise ValueError("expected int or (int, object), but got", i)

            if i in working or (len_iter + i) in working:

                # Retrieving the next item
                if x is None:
                    elem = next(iterators[i], sentinel)
                else:
                    try:
                        elem = iterators[i].send(x)
                    except StopIteration:
                        elem = sentinel

                # Handling of the exhaustion
                if elem is sentinel:
                    if i in working:
                        working.remove(i)
                    else:
                        working.remove(len_iter + i)
                    if not longest:
                        return
                    elems[i] = fillvalue
                else:
                    elems[i] = elem

            # else:
            elif not -len_iter <= i < len_iter:
                raise IndexError

        if len(working) == 0:
            return

        #
        # Communicating with the callers
        #

        received = (yield tuple(elems))  # Returns to the next() caller

        if received is None:  # next() in a row
            cues = working
        else:
            while received is not None:  # send(value)
                cues = received
                received = (yield)


def twist(*iterables, longest=False, fillvalue=None, working=None, init_elems=None, first_cues=None):
    """Function aggregating elements from iterables with the control of send().

    iterables       indices in this argument tuple are used in this function.
    longest         if True, works like itertools.zip_longest() when no send().
    fillvalue       works just like in itertools.zip_longest().
    working         set of index of iterator to be treated as not exhausted.
    init_elems      list of initial value used before aggregating the first
                    element from each iterable.
    first_cues      works as if passed from the send(value) method before
                    aggregating at the start.
    """

    # check the arguments before the first call of next() on the created
    # generator, like __init__().

    iterators = tuple([iter(it) for it in iterables])
    len_iter = len(iterators)

    if working is None:
        working = set(range(len_iter))
    else:
        temp = {}
        for i in working:
            if 0 <= i < len_iter:
                temp |= {i}
            elif -len_iter <= i < 0:
                temp |= {len_iter + i}
            else:
                raise IndexError
        working = temp

    if not isinstance(longest, bool):
        raise TypeError("longest must be boolean, but got", type(longest))
    elif not longest and len(working) < len_iter:
        return

    if init_elems is None:
        elems = [fillvalue] * len_iter
    else:
        elems = list(init_elems)
        if len(elems) != len_iter:
            raise ValueError("expected {},".format(len_iter), "but got", len(elems))

    for i in range(len_iter):
        if i not in working:
            elems[i] = fillvalue

    if first_cues is None:
        cues = working
    else:
        cues = first_cues

    return _twist(*iterators, longest=longest, fillvalue=fillvalue, working=working, elems=elems, cues=cues)
