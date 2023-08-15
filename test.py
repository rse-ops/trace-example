#!/usr/bin/env python

import time

# import perfflowaspect
# import perfflowaspect.aspect


# Note that previous decorators for "around" are commented out.
# @perfflowaspect.aspect.critical_path(pointcut="around")
def bas():
    print("bas")


# @perfflowaspect.aspect.critical_path(pointcut="around")
def bar():
    print("bar")
    time.sleep(0.001)
    bas()


# @perfflowaspect.aspect.critical_path()
def foo(msg):
    print("foo")
    time.sleep(0.001)
    bar()


def test_dont_trace():
    print("Inside do not trace")
    for i in range(4):
        foo("hello do not trace")


def test_trace():
    print("Inside trace")
    for i in range(4):
        foo("hello trace")
