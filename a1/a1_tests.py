from a1 import *


def test_function1():
    r = ["~~", "~~"]
    func_r = create_empty_board(2)

    assert r == func_r
    assert type(r) == type(func_r)
    print("pass test 1")


test_function1()
