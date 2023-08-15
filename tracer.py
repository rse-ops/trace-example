__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2023, Vanessa Sochat"
__license__ = "MIT"

import os
import re
import psutil
import time
import sys

_data = {}


class CommandTracer:
    """
    A command tracer takes some function and args/kwargs checks conditions against
    a metric, and then yields some final list of results.
    """

    def trace(self, functions, commands):
        """
        Provide a list of commands and args, e.g.,

        commands = [[pytest.main, ['-xs', testpath1]], [pytest.main, ['-xs', testpath2]]]
        """
        # Set our functions (or other metadata) to global, being lazy
        # functions: the list of names (strings) we are interested in. This can be nested into other modules
        # results: the trace results, explicitly
        # metadata: other metadata about the same functions
        global _data
        _data = {"functions": set(functions), "results": {}, "metadata": {}}

        # Trace each command
        for command in commands:
            func, params = command
            if isinstance(params, list):
                sys.settrace(code_tracer)
                func(params)
                sys.settrace(None)
            else:
                sys.settrace(code_tracer)
                func(**params)
                sys.settrace(None)

        # When we get here, data is populated
        _data["functions"] = list(_data["functions"])
        return _data

def record_return(code):
    """
    Record return of a function (and time, etc.)
    """
    global _data

    function_name = code.co_name

    if function_name not in _data["results"] or not _data["results"][function_name]:
        raise ValueError("A function is returning that was never called or recorded.")

    # Given serial, this return is matched to the last call
    call = _data["results"][function_name][-1]

    # I'm not sure about these calculations - there was a ts_end
    # that I didn't see used, and I'm not sure how memory usage
    # is calculated. Please double check / comment these further.
    time_end = time.time()
    time_elapsed = time_end - call["time_start"]
    cpu_end = call["p"].cpu_times()
    cpu_end = cpu_end[0]
    cpu_end = cpu_end - call["cpu_start"]

    cpu_usage = (cpu_end / time_end) * 100
    mem_usage = call["p"].memory_info().rss
    if mem_usage > 0:
        mem_usage = mem_usage / 1000

    # Update the record
    call["time_end"] = time_end
    call["time_elapsed"] = time_elapsed
    call["cpu_end"] = cpu_end
    call["cpu_usage"] = cpu_usage
    call["mem_usage"] = mem_usage

    # Delete the process
    p = call["p"]
    call["pid"] = p.pid
    call["process_name"] = p.name()
    del call["p"]


def record_call(code):
    """
    Record the start (call) of a function
    """
    global _data
    function_name = code.co_name

    # In keeping a list, we assume the last entry (call)
    # is matched to the current end. This might not always be true
    # for multiple running of the same function. We could instead
    # use some kind of unique identifier.
    if function_name not in _data["results"]:
        _data["results"][function_name] = []

    p = psutil.Process(os.getpid())
    cpu_start = p.cpu_times()
    cpu_start = cpu_start[0]
    time_start = time.time()

    # The pid has more metadata we can save
    record = {
        "p": p,
        "name": p.name(),
        "cpu_start": cpu_start,
        "time_start": time_start,
    }
    _data["results"][function_name].append(record)


def inspect(code, frame):
    """
    Inspect code object and save basic metadata
    """
    # event is what happened (e.g., call)
    # code.co_names is what byte code uses
    # code.co_varnames are all local variable names, starting with args
    # code.co_argcount is the number args
    # split up decorators and args

    args = [x for x in code.co_varnames[: code.co_argcount] if not x.startswith("@")]
    decorators = list(set(code.co_varnames[: code.co_argcount]).difference(set(args)))
    locals = list(code.co_varnames)[code.co_argcount :]

    # note that frame.f_locals has some local context
    # note that code.co_argcount has argcount
    # Not sure how to derive type here (I don't think we can) but we can get size of stack
    res = {
        "function": code.co_name,
        "lineno": code.co_firstlineno,
        "stacksize": code.co_stacksize,
        "filename": code.co_filename,
        "args": args,
    }

    # Do we have a class (and name)?
    try:
        cls = frame.f_locals["self"].__class__.__name__
    except (KeyError, AttributeError):
        cls = None

    if code.co_freevars:
        res["freevars"] = code.co_freevars
    if decorators:
        res["decorators"] = decorators
    if locals:
        res["locals"] = locals

    # We can assume everything found is on the pythonpath
    regex = "(%s|__init__[.]py)" % "|".join(sys.path)
    modulepath = re.sub(regex, "", res["filename"]).strip(os.sep).replace(os.sep, ".")
    modulepath = modulepath.replace(".py", "")

    # Give the result context to compare to a database
    res["module"] = modulepath
    if cls:
        res["path"] = f"{modulepath}.{cls}.{code.co_name}"
    else:
        res["path"] = f"{modulepath}.{code.co_name}"
    return res


# Easy lookup
events = {"call": record_call, "return": record_return}


def code_tracer(frame, event, arg=None):
    """
    Local trace function that returns itself.

    Save data to global data because we are lazy.
    """
    # This is a cheap way to look up what we want to trace
    global _data

    # extracts frame code
    code = frame.f_code

    # This is the function name. If it's not in our set of interest, keep tracing!
    function_name = code.co_name
    if function_name not in _data["functions"]:
        return code_tracer

    # If we get here, we care about the function call and return (as start and stopping points)
    # Other events include line (pieces within a function) and that is probably too much detail
    if event not in ["call", "return"]:
        return code_tracer

    print(f"🟩️ Function {function_name} is being traced for event {event}!")

    # Just store metadata once, if we haven't seen it yet
    if function_name not in _data["metadata"]:
        _data["metadata"][function_name] = inspect(code, frame)

    # Record data (start for call or end for return)
    events[event](code)
    return code_tracer


def format_results(results):
    """
    Format into prettier json

    This was for the original trace function (not used)
    """
    save = {"calls": {}}

    # This is a tuple (key) and count (value) - we don't care about the value
    for order, (called, count) in enumerate(results.calledfuncs.items()):
        filename, module, function = called
        if filename not in save["calls"]:
            save["calls"][filename] = {
                "module": module,
                "functions": {},
                "order": order,
            }

        # The count should be the only one for the function, but not assuming anything.
        if function not in save["calls"][filename]["functions"]:
            save["calls"][filename]["functions"][function] = 0
        save["calls"][filename]["functions"][function] += count
    return save
