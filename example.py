#!/usr/bin/env/python3

# This is one way to get releases!
# import json
import os
import sys
import json
import pytest

# We don't have a real module, so add the PWD
here = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, here)
from tracer import CommandTracer

results = {}
sig = None


def main():
    # Ensure we get a function from sys.argv to trace
    if len(sys.argv) < 2:
        sys.exit("Please provide the name of a function to trace!")

    # EXAMPLE 1: Command trace (I'm using pytest just because)
    commands = [
        [pytest.main, ["-xs", "test.py"]],
    ]

    # Functions we want to trace (name in lit)
    # This could come from the command line, config file, etc.
    functions = [sys.argv[1]]
    tracer = CommandTracer()

    # The tracer will add incompatibilities / results to the metric
    data = tracer.trace(functions, commands)

    # Show mee the data!
    print(json.dumps(data, indent=4))


if __name__ == "__main__":
    main()
