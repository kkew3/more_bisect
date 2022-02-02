"""
Description of the parameter list ``(x, a=None, lo=None, hi=None, key=None)``
=============================================================================

``x`` is the target to search. ``a`` is the array to search. ``lo`` is the
index (inclusive) to start searching. ``hi`` is the index (inclusive) to stop
searching. ``key`` is a unary function (described below).

If ``a`` is provided not ``None``, ``a`` should be an array. ``key`` is used
to compute a comparison key out of ``a[i]``. If ``key`` is ``None``, ``key``
will be default to an identity function ``lambda x: x``. ``lo`` is default to
0 and ``hi`` default to ``len(a) - 1``.

If ``a`` is provided ``None``, ``lo``, ``hi`` and ``key`` must be provided not
``None``. Now ``key`` is used to compute a comparison key out of index ``i``
in each round of loop.

Example
=======

- ``(2, [1, 2, 3], lo=0, hi=1)`` searches [1, 2] for 2.
- ``(2, [('a', 1), ('b', 2), ('a', 3)], key=lambda x: x[1])`` searches
  [1, 2, 3] for 2
- ``(2, lo=1, hi=2, key=lambda i: [1, 2, 3][i])`` searches [2, 3] for 2
"""


__all__ = [
    'any_pos_of_x',
    'first_pos_of_x',
    'last_pos_of_x',
]


def _index_a_mapped(a, f):
    if f is None:
        def _pick(i):
            return a[i]
    else:
        def _pick(i):
            return f(a[i])
    return _pick


def _validate_args(a, lo, hi, key):
    if a is None:
        if lo is None or hi is None or key is None:
            raise ValueError('`lo`, `hi`, `key` must not be None when `a` '
                             'is None')
    else:
        if lo is None:
            lo = 0
        if hi is None:
            hi = len(a) - 1
        key = _index_a_mapped(a, key)
    return lo, hi, key


def any_pos_of_x(x, a=None, lo=None, hi=None, key=None):
    """
    Returns the index ``i`` such that ``a[i]`` (or ``key(i)`` if ``a`` is
    ``None``) is equal to ``x`` within range [``lo``, ``hi``]. If no such
    index is found, returns ``None``.
    """
    lo, hi, key = _validate_args(a, lo, hi, key)
    if lo > hi:
        return None
    while lo < hi:
        mi = lo + (hi - lo) // 2
        mi_value = key(mi)
        if mi_value == x:
            return mi
        if mi_value < x:
            lo = mi + 1
        else:
            hi = mi - 1
    if key(lo) == x:
        return lo
    return None


def first_pos_of_x(x, a=None, lo=None, hi=None, key=None):
    """
    Returns the index ``i`` such that ``a[i]`` (or ``key(i)`` if ``a`` is
    ``None``) is equal to ``x`` within [``lo``, ``hi``], and that ``i`` is
    the smallest. If no such index is found, returns ``None``.
    """
    lo, hi, key = _validate_args(a, lo, hi, key)
    if lo > hi:
        return None
    while lo < hi:
        mi = lo + (hi - lo) // 2
        mi_value = key(mi)
        if mi_value < x:
            lo = mi + 1
        elif mi_value > x:
            hi = mi - 1
        else:
            hi = mi
    if key(lo) == x:
        return lo
    return None


def last_pos_of_x(x, a=None, lo=None, hi=None, key=None):
    """
    Returns the index ``i`` such that ``a[i]`` (or ``key(i)`` if ``a`` is
    ``None``) is equal to ``x`` within [``lo``, ``hi``], and that ``i`` is
    the largest. If no such index is found, returns ``None``.
    """
    lo, hi, key = _validate_args(a, lo, hi, key)
    if lo > hi:
        return None
    while lo < hi:
        mi = lo + (hi - lo + 1) // 2
        mi_value = key(mi)
        if mi_value < x:
            lo = mi + 1
        elif mi_value > x:
            hi = mi - 1
        else:
            lo = mi
    if key(lo) == x:
        return lo
    return None


def last_pos_less_than(x, a=None, lo=None, hi=None, key=None):
    """
    Returns the index ``i`` such that ``a[i]`` (or ``key(i)`` if ``a`` is
    ``None``) is less than ``x`` within [``lo``, ``hi``], and that ``i`` is
    the largest. If no such index is found, returns ``None``.
    """
    lo, hi, key = _validate_args(a, lo, hi, key)
    if lo > hi:
        return None
    while lo < hi:
        mi = lo + (hi - lo + 1) // 2
        mi_value = key(mi)
        if mi_value < x:
            lo = mi
        else:
            hi = mi - 1
    if key(lo) < x:
        return lo
    return None



def first_pos_greater_than(x, a=None, lo=None, hi=None, key=None):
    """
    Returns the index ``i`` such that ``a[i]`` (or ``key(i)`` if ``a`` is
    ``None``) is greater than ``x`` within [``lo``, ``hi``], and that ``i`` is
    the smallest. If no such index is found, returns ``None``.
    """
    lo, hi, key = _validate_args(a, lo, hi, key)
    if lo > hi:
        return None
    while lo < hi:
        mi = lo + (hi - lo) // 2
        mi_value = key(mi)
        if mi_value <= x:
            lo = mi + 1
        else:
            hi = mi
    if key(lo) > x:
        return lo
    return None
