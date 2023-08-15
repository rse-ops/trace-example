# Tracing without Decorators

This is a dummy example of tracing without decorators, namely grabbing a process before and after,
and recording times and memory usage. The pros are that with this method, we can trace any function
(by name) at any level of Python code (meaning it doesn't have to be in a module that we control)
and we can save basic metadata about it. 

## Usage

You'll need a few dependencies:

```bash
pip install psutil pytest
```

And then we provide the following:

 - [trace.py](trace.py): has a very simple tracer class and functions. This could be developed into a more robust class, etc.
 - [test.py](test.py): is our example Python program where we want to trace one or more functions. We don't want to need to add decorators to it, because we don't own the code (potentially)
 - [example.py](example.py): is a simple script that will instantiate our `CommandTracer`, receive a function name of interest, and run the trace.

And then you can run the example program [example.py](example.py) targeting a function from [test.py](test.py).
Normally we would just target a module path, but for this case I'm showing a command tracing example (because likely
we are running something from the command line in HPC).

### Examples

Here we are tracing different functions (at different levels of the call). You'll note for each one, it traces our function of choice!
Also note that the entire program runs still.

```bash
$ python example.py test_trace
```

<details>

<summary>test_trace output</summary>

```console
================================================================================================================================ test session starts =================================================================================================================================
platform linux -- Python 3.8.10, pytest-7.4.0, pluggy-1.2.0
rootdir: /workspaces/PerfFlowAspect/src/python
collected 2 items                                                                                                                                                                                                                                                                    

test.py Inside do not trace
foo
bar
bas
foo
bar
bas
foo
bar
bas
foo
bar
bas
.🟩️ Function test_trace is being traced for event call!
Inside trace
foo
bar
bas
foo
bar
bas
foo
bar
bas
foo
bar
bas
🟩️ Function test_trace is being traced for event return!
.

================================================================================================================================= 2 passed in 0.05s ==================================================================================================================================
{
    "functions": [
        "test_trace"
    ],
    "results": {
        "test_trace": [
            {
                "name": "python3",
                "cpu_start": 0.5,
                "time_start": 1692073435.8288963,
                "time_end": 1692073435.8378818,
                "time_elapsed": 0.008985519409179688,
                "cpu_end": 0.0,
                "cpu_usage": 0.0,
                "mem_usage": 26406.912,
                "pid": 14718,
                "process_name": "python3"
            }
        ]
    },
    "metadata": {
        "test_trace": {
            "function": "test_trace",
            "lineno": 31,
            "stacksize": 3,
            "filename": "/workspaces/PerfFlowAspect/src/python/trace/test.py",
            "args": [],
            "locals": [
                "i"
            ],
            "module": "test",
            "path": "test.test_trace"
        }
    }
}
```

</details>

Here is an example of a nested function within there:

```bash
$ python example.py foo
```

And this also shows a function being called multiple times (in serial)

<details>

<summary>test_trace output</summary>

```console
{
    "functions": [
        "foo"
    ],
    "results": {
        "foo": [
            {
                "name": "python3",
                "cpu_start": 0.53,
                "time_start": 1692073686.826895,
                "time_end": 1692073686.8291821,
                "time_elapsed": 0.002287149429321289,
                "cpu_end": 0.0,
                "cpu_usage": 0.0,
                "mem_usage": 26472.448,
                "pid": 15593,
                "process_name": "python3"
            },
            {
                "name": "python3",
                "cpu_start": 0.53,
                "time_start": 1692073686.829897,
                "time_end": 1692073686.8323753,
                "time_elapsed": 0.002478361129760742,
                "cpu_end": 0.0,
                "cpu_usage": 0.0,
                "mem_usage": 26472.448,
                "pid": 15593,
                "process_name": "python3"
            },
            {
                "name": "python3",
                "cpu_start": 0.53,
                "time_start": 1692073686.8329277,
                "time_end": 1692073686.8352268,
                "time_elapsed": 0.002299070358276367,
                "cpu_end": 0.010000000000000009,
                "cpu_usage": 5.909908107313889e-10,
                "mem_usage": 26472.448,
                "pid": 15593,
                "process_name": "python3"
            },
            {
                "name": "python3",
                "cpu_start": 0.54,
                "time_start": 1692073686.8358603,
                "time_end": 1692073686.8381197,
                "time_elapsed": 0.002259492874145508,
                "cpu_end": 0.0,
                "cpu_usage": 0.0,
                "mem_usage": 26472.448,
                "pid": 15593,
                "process_name": "python3"
            },
            {
                "name": "python3",
                "cpu_start": 0.54,
                "time_start": 1692073686.8457143,
                "time_end": 1692073686.8480897,
                "time_elapsed": 0.002375364303588867,
                "cpu_end": 0.0,
                "cpu_usage": 0.0,
                "mem_usage": 26472.448,
                "pid": 15593,
                "process_name": "python3"
            },
            {
                "name": "python3",
                "cpu_start": 0.54,
                "time_start": 1692073686.8486905,
                "time_end": 1692073686.850965,
                "time_elapsed": 0.0022745132446289062,
                "cpu_end": 0.0,
                "cpu_usage": 0.0,
                "mem_usage": 26472.448,
                "pid": 15593,
                "process_name": "python3"
            },
            {
                "name": "python3",
                "cpu_start": 0.54,
                "time_start": 1692073686.8514028,
                "time_end": 1692073686.85362,
                "time_elapsed": 0.0022172927856445312,
                "cpu_end": 0.010000000000000009,
                "cpu_usage": 5.909908107249647e-10,
                "mem_usage": 26472.448,
                "pid": 15593,
                "process_name": "python3"
            },
            {
                "name": "python3",
                "cpu_start": 0.55,
                "time_start": 1692073686.8538642,
                "time_end": 1692073686.8561532,
                "time_elapsed": 0.0022890567779541016,
                "cpu_end": 0.0,
                "cpu_usage": 0.0,
                "mem_usage": 26472.448,
                "pid": 15593,
                "process_name": "python3"
            }
        ]
    },
    "metadata": {
        "foo": {
            "function": "foo",
            "lineno": 23,
            "stacksize": 3,
            "filename": "/workspaces/PerfFlowAspect/src/python/trace/test.py",
            "args": [
                "msg"
            ],
            "module": "test",
            "path": "test.foo"
        }
    }
}
```

</details>

And here is an example not even in the library! It's from json I think?


```bash
$ python example.py raw_decode
```

<details>

<summary>raw_decode calls</summary>

```console
🟩️ Function raw_decode is being traced for event call!
🟩️ Function raw_decode is being traced for event return!
🟩️ Function raw_decode is being traced for event call!
🟩️ Function raw_decode is being traced for event return!
================================================================================================================================ test session starts =================================================================================================================================
platform linux -- Python 3.8.10, pytest-7.4.0, pluggy-1.2.0
rootdir: /workspaces/PerfFlowAspect/src/python
collected 2 items                                                                                                                                                                                                                                                                    

test.py Inside do not trace
foo
bar
bas
foo
bar
bas
foo
bar
bas
foo
bar
bas
.Inside trace
foo
bar
bas
foo
bar
bas
foo
bar
bas
foo
bar
bas
.🟩️ Function raw_decode is being traced for event call!
🟩️ Function raw_decode is being traced for event return!


================================================================================================================================= 2 passed in 0.04s ==================================================================================================================================
{
    "functions": [
        "raw_decode"
    ],
    "results": {
        "raw_decode": [
            {
                "name": "python3",
                "cpu_start": 0.5,
                "time_start": 1692073855.0309513,
                "time_end": 1692073855.0309908,
                "time_elapsed": 3.9577484130859375e-05,
                "cpu_end": 0.0,
                "cpu_usage": 0.0,
                "mem_usage": 26165.248,
                "pid": 16185,
                "process_name": "python3"
            },
            {
                "name": "python3",
                "cpu_start": 0.51,
                "time_start": 1692073855.032936,
                "time_end": 1692073855.0329714,
                "time_elapsed": 3.528594970703125e-05,
                "cpu_end": 0.0,
                "cpu_usage": 0.0,
                "mem_usage": 26165.248,
                "pid": 16185,
                "process_name": "python3"
            },
            {
                "name": "python3",
                "cpu_start": 0.59,
                "time_start": 1692073855.1352997,
                "time_end": 1692073855.1353357,
                "time_elapsed": 3.600120544433594e-05,
                "cpu_end": 0.0,
                "cpu_usage": 0.0,
                "mem_usage": 26587.136,
                "pid": 16185,
                "process_name": "python3"
            }
        ]
    },
    "metadata": {
        "raw_decode": {
            "function": "raw_decode",
            "lineno": 343,
            "stacksize": 10,
            "filename": "/usr/lib/python3.8/json/decoder.py",
            "args": [
                "self",
                "s",
                "idx"
            ],
            "locals": [
                "obj",
                "end",
                "err"
            ],
            "module": "json.decoder",
            "path": "json.decoder.JSONDecoder.raw_decode"
        }
    }
}
```

</details>

## How does it work?

Using sys settrace, we can define a custom function that has access to events and the
code object for all events (call, return, line, etc) during execution of a program.
This doesn't scale well to, for example, trace and print _every_ function and line
in the entirety of a program, but it works fairly well for a small set! For this quick
demo, we take a simple approach to expect a serial run where if a function is called
(a "call" event) we assume the next "return" event is matched. This may not be true (and likely
will not) in all cases. In these advanced cases, we will need to bring in a unique identifier
to match the two (or some other trick).

Note that I am not super familiar with PerfFlowAspect, but I followed the logic I saw in
the wrapper "around" [here](https://github.com/flux-framework/PerfFlowAspect/blob/4852a48f4ea537296078ab293c731d7a35f704dd/src/python/perfflowaspect/advice_chrome.py#L325-L386).

## Suggested Steps

If this is what perfflow does (and there isn't some other compiled library I'm supposed to be running alongside it)?
I can definitely help to provide a dynamic tracing functionality to PerfFlowAspect, or something else of interest.
My suggestion would be to both have a command line way to target one or more functions, e.g.

```bash
$ perfflow -t test_trace -t bar
```

And possibly a config file (in YAML) that folks can define a more complex set of parameters or setup.
And likely we need to be more detail oriented with respect to data collection and unique identifiers,
and of course the data formats for PerfFlowAspect. I apologize I didn't look around that particular python module further to see what else it is doing -
I'm sure I missed something! I mostly wanted to provide this simple tracing example to see if it 
was of interest. I messed around with it a few months ago for ABI stuffs and thought it was cool :)


## License

HPCIC DevTools is distributed under the terms of the MIT license.
All new contributions must be made under this license.

See [LICENSE](https://github.com/converged-computing/cloud-select/blob/main/LICENSE),
[COPYRIGHT](https://github.com/converged-computing/cloud-select/blob/main/COPYRIGHT), and
[NOTICE](https://github.com/converged-computing/cloud-select/blob/main/NOTICE) for details.

SPDX-License-Identifier: (MIT)

LLNL-CODE- 842614
