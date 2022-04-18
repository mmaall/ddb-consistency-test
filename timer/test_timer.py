import pytest
import timer
from datetime import timedelta 


def add(a: int, b: int):
    return a + b

def add_2(a = 1, b = 2):
    return a + b 

def test_timer_invoke_1():
    a = 1
    b = 2
    timer_obj = timer.time(add, a, b)

    assert timer_obj.output == a + b
    assert timer_obj.elapsed > timedelta(microseconds = 0) 

def test_timer_invoke_2():
    timer_obj = timer.time(add_2)

    assert timer_obj.output == 3

def test_timer_invoke_3():
    a = 0
    b = 1 
    timer_obj = timer.time(add_2, a = a, b = b)

    assert timer_obj.output == a + b 
