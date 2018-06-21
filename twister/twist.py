#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Enables to iterate over iterables together and independently of each other.

This module provide twist() function which provides the following features:
  * takes iterables as argument and creates a generator.
  * upper compatible to zip() or zip_longest() except for type of instance.
  * able to select from which iterators to aggregate elements via send().

"""


def _twist(*iterators, longest, fillvalue, working, items, move):
    """Generator function witch executes the main iteration process of twist().

    Separated from the main function to check the arguments just after taking
    them. That's because generator doesn't start execution until the first call
    of next().
    """

    sentinel = object()
    num_iterators = len(iterators)

    while True:

        #
        # Aggregating elements from the selected iterators
        #

        if isinstance(move, int) or isinstance(move, tuple):
            move = [move]
        else:
            move = list(move)

        for cue in move:

            # Converting supported formats into common variables
            if isinstance(cue, int):
                key, thing = cue, None
            elif isinstance(cue, tuple):
                key, thing = cue
            else:
                raise ValueError

            if key in working or (num_iterators + key) in working:

                # Retrieving the next item
                if thing is None:
                    elem = next(iterators[key], sentinel)
                else:
                    try:
                        elem = iterators[key].send(thing)
                    except StopIteration:
                        elem = sentinel

                # Handling of the exhaustion
                if elem is sentinel:
                    if key in working:
                        working.remove(key)
                    else:
                        working.remove(num_iterators + key)
                    if not longest:
                        return
                    items[key] = fillvalue
                else:
                    items[key] = elem

            else:
                raise KeyError

        if len(working) == 0:
            return

        #
        # Communicating with the callers
        #

        received = (yield tuple(items))  # Return to the next() caller

        if received is None:  # next() in a row
            move = working
        else:
            while received is not None:  # send(value)
                move = received
                received = (yield)


def twist(*iterables, longest=False, fillvalue=None, working=None, items=None, move=None):
    """Function working as enhanced zip() by attachment of send() method.

    iterables       tuple of iterable. keys are widely used in this function.
    longest         if True, works like itertools.zip_longest().
    fillvalue       works the same as in itertools.zip_longest().
    working         set of key of not exhausted iterators.
    items           list of the last element retrieved from each iterator.
    move            cue or iterable of cue except for tuple. passed from the
                    value argument of send() of the generator created.
    cue             key or (key, thing). key is of the iterator to aggregate
                    elements from at the next call of next(). if (key, thing),
                    send(thing) is called on the iterator instead of next().
    """

    # check the arguments before the first call of next(), like __init__().

    iterators = tuple([iter(it) for it in iterables])
    num_iterators = len(iterators)

    if working is None:
        working = set(range(num_iterators))
    else:
        temp = {}
        for key in working:
            if 0 <= key < num_iterators:
                temp |= {key}
            elif -num_iterators <= key < 0:
                temp |= {num_iterators + key}
            else:
                raise ValueError
        working = temp

    if not isinstance(longest, bool):
        raise TypeError
    elif not longest and len(working) < num_iterators:
        return

    if items is None:
        items = [fillvalue] * num_iterators
    else:
        items = list(items)
        if len(items) != num_iterators:
            raise ValueError

    for key in range(num_iterators):
        if key not in working:
            items[key] = fillvalue

    if move is None:
        move = working

    return _twist(*iterators, longest=longest, fillvalue=fillvalue, working=working, items=items, move=move)
