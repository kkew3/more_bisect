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
    'any_pos_eq',
    'first_pos_eq',
    'last_pos_eq',
    'last_pos_lt',
    'last_pos_le',
    'first_pos_gt',
    'bisect_left',
    'bisect_right',
    'last_closest_to',
    'first_closest_to',
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


def any_pos_eq(x, a=None, lo=None, hi=None, key=None):
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


def first_pos_eq(x, a=None, lo=None, hi=None, key=None):
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


def last_pos_eq(x, a=None, lo=None, hi=None, key=None):
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


def last_pos_lt(x, a=None, lo=None, hi=None, key=None):
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


def last_pos_le(x, a=None, lo=None, hi=None, key=None):
    """
    Returns the index ``i`` such that ``a[i]`` (or ``key(i)`` if ``a`` is
    ``None``) is less than or equal to ``x`` within [``lo``, ``hi``], and that
    ``i`` is the largest. If no such index is found, returns ``None``.
    """
    lo, hi, key = _validate_args(a, lo, hi, key)
    if lo > hi:
        return None
    while lo < hi:
        mi = lo + (hi - lo + 1) // 2
        mi_value = key(mi)
        if mi_value <= x:
            lo = mi
        else:
            hi = mi - 1
    if key(lo) <= x:
        return lo
    return None


def first_pos_gt(x, a=None, lo=None, hi=None, key=None):
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


def bisect_left(x, a=None, lo=None, hi=None, key=None):
    """
    Identical to ``bisect.bisect_left``, except that ``lo`` and ``hi`` define
    an inclusive range (see module __doc__ for detail).
    """
    lo, hi, key = _validate_args(a, lo, hi, key)
    if lo <= hi and x > key(hi):
        return hi + 1
    while lo < hi:
        mi = lo + (hi - lo) // 2
        mi_value = key(mi)
        if mi_value < x:
            lo = mi + 1
        else:
            hi = mi
    return lo


def bisect_right(x, a=None, lo=None, hi=None, key=None):
    """
    Identical to ``bisect.bisect_right``, except that ``lo`` and ``hi`` define
    an inclusive range (see module __doc__ for detail).
    """
    lo, hi, key = _validate_args(a, lo, hi, key)
    if lo <= hi and x >= key(hi):
        return hi + 1
    while lo < hi:
        mi = lo + (hi - lo) // 2
        mi_value = key(mi)
        if mi_value > x:
            hi = mi
        else:
            lo = mi + 1
    return lo


def last_closest_to(x, a=None, lo=None, hi=None, key=None):
    """
    Returns the index ``i`` such that ``a[i]`` (or ``key(i)`` if ``a`` is
    ``None``) is the closest to ``x`` within [``lo``, ``hi``], and that ``i``
    is the largest. If the range defined by ``lo`` and ``hi`` is empty,
    returns ``None``.
    """
    lo, hi, key = _validate_args(a, lo, hi, key)
    if lo > hi:
        return None
    i = first_pos_gt(x, None, lo, hi, key)
    if i is None:
        return hi
    if i == lo:
        return lo
    if abs(key(i - 1) - x) < abs(key(i) - x):
        return i - 1
    return i


def first_closest_to(x, a=None, lo=None, hi=None, key=None):
    """
    Returns the index ``i`` such that ``a[i]`` (or ``key(i)`` if ``a`` is
    ``None``) is the closest to ``x`` within [``lo``, ``hi``], and that ``i``
    is the smallest. If the range defined by ``lo`` and ``hi`` is empty,
    returns ``None``.
    """
    lo, hi, key = _validate_args(a, lo, hi, key)
    if lo > hi:
        return None
    i = last_pos_lt(x, None, lo, hi, key)
    if i is None:
        return lo
    if i == hi:
        return hi
    if abs(key(i + 1) - x) < abs(key(i) - x):
        return i + 1
    return i
