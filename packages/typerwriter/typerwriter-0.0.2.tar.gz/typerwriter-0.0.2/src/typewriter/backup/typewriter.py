import inspect
import random
import runpy
import signal
import sys
import time
import typing

from functools import cache
from itertools import islice
from types import CodeType
from typing import Dict, Union, Optional

TOOL_ID = 3  # Choose an unused ID, for example, 3
TOOL_NAME = "typewriter"
SAMPLING_INTERVAL = 0.5
THRESHOLD_TIME = 1.0 # seconds; functions taking longer remain instrumented
EXCLUDED_FUNCTION_NAMES = ["<lambda>", "<genexpr>", "<module>" ]

visited_funcs = set()
sampled_funcs = dict()
visited_funcs_arguments = dict()
visited_funcs_retval = dict()
start_time_funcs = dict()
execution_time_funcs = dict()

def get_full_type_name(type_obj):
    if hasattr(type_obj, '__origin__') and hasattr(type_obj, '__args__'):
        # Handle types from the typing module (e.g., Union, List, etc.)
        origin_name = type_obj.__origin__.__name__
        args_names = ', '.join(get_full_type_name(arg) for arg in type_obj.__args__)
        return f'{origin_name}[{args_names}]'
    else:
        # Handle regular types
        module_name = type_obj.__module__
        type_name = type_obj.__name__
        if module_name == 'builtins':
            return type_name  # No need to include 'builtins' in the name
        return f'{module_name}.{type_name}'

def get_full_type(value):
    if isinstance(value, dict):
        # Randomly sample a key and value from the dictionary
        if value:
            n = random.randint(0, len(value)-1)
            key, val = next(islice(value.items(), n, n + 1))
            return f'dict[{get_full_type(key)}: {get_full_type(val)}]'
        else:
            return 'dict'
    elif isinstance(value, list):
        # Randomly sample an element from the list
        if value:
            n = random.randint(0, len(value)-1)
            elem = value[n]
            return f'list[{get_full_type(elem)}]'
        else:
            return 'list'
    elif isinstance(value, tuple):
        # Recursively get the types of all elements in the tuple
        return f'tuple[{", ".join(type(elem).__name__ for elem in value)}]'
    else:
        return type(value).__name__
        # return get_full_type_name(type(value))
   
    
def enter_function(code: CodeType, instruction_offset):
    if code.co_name in EXCLUDED_FUNCTION_NAMES:
        return sys.monitoring.DISABLE
        
    func_name = code.co_qualname
    filename = code.co_filename

    t = tuple([filename, func_name])
    
    if t in sampled_funcs:
        if execution_time_funcs[t] < THRESHOLD_TIME:
            return sys.monitoring.DISABLE

    start_time_funcs[t] = time.perf_counter_ns()
    execution_time_funcs[t] = THRESHOLD_TIME # for now
    sampled_funcs[t] = code
    visited_funcs.add(t)
    
    # Inspect the call stack to get the arguments of the function
    frame = inspect.currentframe()
    if frame is not None and frame.f_back is not None:
        args, _, _, values = inspect.getargvalues(frame.f_back)
        argtypes = []
        # Visit arguments, collecting type values and names.
        for arg in args:
            value = values[arg]
            full_type_name = get_full_type(value)
            full_type_names = set()
            full_type_names.add(full_type_name)
            argtypes.append((arg, type(value), full_type_names))
        if t in visited_funcs_arguments:
            for i, (arg, _, full_type_name_set) in enumerate(argtypes):
                if i < len(visited_funcs_arguments[t]):
                    _, old_type, old_type_name_set = visited_funcs_arguments[t][i]
                    if full_type_name not in old_type_name_set:
                        old_type_name_set.add(full_type_name_set.pop())
        else:
            visited_funcs_arguments[t] = argtypes
    else:
        pass

    # Continue monitoring for the return so we can get the return value type
    return sys.monitoring.events.C_RETURN


def exit_function(code, instruction_offset, return_value):
    if code.co_name in EXCLUDED_FUNCTION_NAMES:
        return sys.monitoring.DISABLE
        
    func_name = code.co_qualname
    filename = code.co_filename
        
    t = tuple([filename, func_name])
    execution_time_funcs[t] = (time.perf_counter_ns() - start_time_funcs[t]) / 1e9
    
    if t not in visited_funcs_retval:
        visited_funcs_retval[t] = set()
    if type(return_value) not in visited_funcs_retval[t]:
        visited_funcs_retval[t].add(type(return_value))
    return sys.monitoring.DISABLE

def handle_clear_seen_funcs(_signum, _frame):
    sys.monitoring.restart_events()
    sampled_funcs.clear()
    signal.setitimer(signal.ITIMER_REAL, SAMPLING_INTERVAL)

def output_type_signatures(file=sys.stdout):
    # Print all type signatures
    for (filename, func_name) in visited_funcs:
        if filename.startswith("/Library") or filename.startswith("<"):
            continue
        try:
            t = tuple([filename, func_name])
            args = visited_funcs_arguments[t]
            s = f"{filename}:def {func_name}("
            for (index, (argname, argtype, argtype_fullname_set)) in enumerate(args):
                if len(argtype_fullname_set) == 1:
                    argtype_fullname = argtype_fullname_set.pop()
                else:
                    argtype_fullname = 'Union[' + (", ").join(argtype_fullname_set) + ']'
                s += f"{argname}: {argtype_fullname}"
                if index < len(args) - 1:
                    s += ", "
            s += ")"
            if len(visited_funcs_retval[t]) == 1:
                retval_name = get_full_type_name(visited_funcs_retval[t].pop())
            else:
                retval_name = 'Union[' + (", ").join(get_full_type_name(t) for t in visited_funcs_retval[t]) + ']'
            s += f" -> {retval_name}"
            print(s, file=file)
        except KeyError:
            # Something weird happened
            pass
    

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {TOOL_NAME} <script.py> [args...]", file=sys.stderr)
        sys.exit(1)

    script_path = sys.argv[1]
    sys.argv = sys.argv[1:]  # Adjust argv for the script

    sys.monitoring.use_tool_id(TOOL_ID, TOOL_NAME)
    sys.monitoring.set_events(TOOL_ID,
                              sys.monitoring.events.PY_START |
                              sys.monitoring.events.PY_RETURN)

    # Set the callback for the monitoring events
    sys.monitoring.register_callback(TOOL_ID, sys.monitoring.events.PY_START, enter_function)
    sys.monitoring.register_callback(TOOL_ID, sys.monitoring.events.PY_RETURN, exit_function)


    # Set a timer to allow periodic merging of types.
    # Set up the timer signal handler
    signal.signal(signal.SIGALRM, handle_clear_seen_funcs)
        
    # Schedule the first timer event
    signal.setitimer(signal.ITIMER_REAL, SAMPLING_INTERVAL)
        
    # Run the specified script
    runpy.run_path(script_path, run_name="__main__")
    
    # Turn off all monitoring.
    sys.monitoring.register_callback(TOOL_ID, sys.monitoring.events.PY_START, None)
    sys.monitoring.register_callback(TOOL_ID, sys.monitoring.events.PY_RETURN, None)
    
    # Free the tool ID after execution
    sys.monitoring.free_tool_id(TOOL_ID)

    with open("typewriter.out", "w+") as f:
        output_type_signatures(f) # sys.stderr)
    
if __name__ == "__main__":
    main()

