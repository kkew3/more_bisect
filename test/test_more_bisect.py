import pytest

import more_bisect
from more_bisect.more_bisect import _validate_args


def test__validate_args():
    lo, hi, key = _validate_args([1, 2], None, None, None)
    assert lo == 0
    assert hi == 1
    assert key(0) == 1 and key(1) == 2
    with pytest.raises(IndexError):
        key(2)

    lo, hi, key = _validate_args([('a', 1), ('a', 2)], None, 1,
                                 key=lambda x: x[1])
    assert lo == 0
    assert hi == 1
    assert key(0) == 1 and key(1) == 2
    with pytest.raises(IndexError):
        key(2)

    a = [1, 2]
    lo, hi, key = _validate_args(None, 0, 1, lambda i: a[i])
    assert lo == 0
    assert hi == 1
    assert key(0) == 1 and key(1) == 2
    with pytest.raises(IndexError):
        key(2)

    a = [('a', 1), ('a', 2)]
    lo, hi, key = _validate_args(None, 0, 1, lambda i: a[i][1])
    assert lo == 0
    assert hi == 1
    assert key(0) == 1 and key(1) == 2
    with pytest.raises(IndexError):
        key(2)


def test_any_pos_of_x():
    a = [1, 3, 3, 3, 3, 4, 5, 6, 7, 8, 9, 10]
    pos = more_bisect.any_pos_of_x(3, a)
    assert 1 <= pos <= 4
    pos = more_bisect.any_pos_of_x(-3, list(reversed(a)), key=lambda x: -x)
    assert 7 <= pos <= 10
    a = [2, 3]
    assert more_bisect.any_pos_of_x(3, a) == 1
    a = [3, 4]
    assert more_bisect.any_pos_of_x(3, a) == 0
    a = []
    assert more_bisect.any_pos_of_x(3, a) is None
    a = [1, 4, 5, 6, 7, 8, 9, 10]
    assert more_bisect.any_pos_of_x(3, a) is None


def test_first_pos_of_x():
    a = [1, 3, 3, 3, 3, 4, 5, 6, 7, 8, 9, 10]
    pos = more_bisect.first_pos_of_x(3, a)
    assert pos == 1
    pos = more_bisect.first_pos_of_x(-3, list(reversed(a)), key=lambda x: -x)
    assert pos == 7
    a = [2, 3]
    assert more_bisect.first_pos_of_x(3, a) == 1
    a = [3, 4]
    assert more_bisect.first_pos_of_x(3, a) == 0
    a = []
    assert more_bisect.first_pos_of_x(3, a) is None
    a = [1, 4, 5, 6, 7, 8, 9, 10]
    assert more_bisect.first_pos_of_x(3, a) is None



def test_last_pos_of_x():
    a = [1, 3, 3, 3, 3, 4, 5, 6, 7, 8, 9, 10]
    pos = more_bisect.last_pos_of_x(3, a)
    assert pos == 4
    pos = more_bisect.last_pos_of_x(-3, list(reversed(a)), key=lambda x: -x)
    assert pos == 10
    a = [2, 3]
    assert more_bisect.last_pos_of_x(3, a) == 1
    a = [3, 4]
    assert more_bisect.last_pos_of_x(3, a) == 0
    a = []
    assert more_bisect.last_pos_of_x(3, a) is None
    a = [1, 4, 5, 6, 7, 8, 9, 10]
    assert more_bisect.last_pos_of_x(3, a) is None


def test_last_pos_less_than():
    a = [1, 3, 3, 3, 3, 4, 5, 6, 7, 8, 9, 10]
    assert more_bisect.last_pos_less_than(3, a) == 0
    a = [3, 3, 3, 3, 4, 5, 6, 7, 8, 9, 10]
    assert more_bisect.last_pos_less_than(3, a) is None
    a = [2, 3]
    assert more_bisect.last_pos_less_than(3, a) == 0
    a = [3, 4]
    assert more_bisect.last_pos_less_than(3, a) is None
    a = [1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9, 10]
    assert more_bisect.last_pos_less_than(3, a) == 3
