import inspect
import random
import runpy
import signal
import sys
import time
import typing

from functools import cache
from itertools import islice
from types import CodeType, FrameType
from typing import Any, Dict, List, Optional, Set, Tuple, Type, Union

# Below is to mollify mypy.
try:
    import sys.monitoring  # type: ignore
except:
    pass

TOOL_ID = 3
TOOL_NAME = "typewriter"
SAMPLING_INTERVAL = 1.0
THRESHOLD_TIME = 1.0  # seconds; functions taking longer remain instrumented
EXCLUDED_FUNCTION_NAMES = ["<lambda>", "<genexpr>", "<module>"]

visited_funcs: Set[Tuple[str, str]] = set()
sampled_funcs: Set[Tuple[str, str]] = set()
visited_funcs_arguments: Dict[
    Tuple[str, str], List[Tuple[str, Type[Any], Set[str]]]
] = dict()
visited_funcs_retval: Dict[Tuple[str, str], Set[Type[Any]]] = dict()
start_time_funcs: Dict[Tuple[str, str], float] = dict()
execution_time_funcs: Dict[Tuple[str, str], float] = dict()


def get_full_type_name(type_obj: Type[Any]) -> str:
    """
    This function takes a type object and returns its fully-qualified name,
    complete with details about generic arguments for generic types,
    and skipping the inclusion of 'builtins' as a prefix for builtin types.

    Args:
        type_obj (Type[Any]): The type object to process.

    Returns:
        str: Fully-qualified name of the given type.

    """
    # Check if the type object has '__origin__' and '__args__' attributes,
    # which would indicate that it's a composite type from the typing module
    # (for example, Union, List, etc.)
    if hasattr(type_obj, "__origin__") and hasattr(type_obj, "__args__"):
        # If it's a composite type, extract the base type name and
        # recursively get the full type names for its arguments.
        origin_name = type_obj.__origin__.__name__
        args_names = ", ".join((get_full_type_name(arg) for arg in type_obj.__args__))  # type: ignore
        # Construct the final type name with arguments enclosed in brackets.
        return f"{origin_name}[{args_names}]"
    else:
        # If it's a regular (non-composite) type, just extract its module name
        # and type name
        # Extract the module and type names
        module_name = type_obj.__module__
        type_name = type_obj.__name__
        # If the type is a built-in Python type,
        # we don't need to prefix it with 'builtins'.
        if module_name == "builtins":
            return type_name
        return f"{module_name}.{type_name}"


def get_full_type(value: Union[Dict, List, Tuple, Any]) -> str:
    """
    get_full_type function takes a value as input and returns a string representing the type of the value.

    If the value is of type dictionary, it randomly selects a pair of key and value from the dictionary
    and recursively determines their types.

    If the value is a list, it randomly selects an item from the list and
    determines its type recursively.

    If the value is a tuple, it determines the types of all elements in the tuple.

    For other types, it returns the name of the type.
    """
    if isinstance(value, dict):
        # Checking if the value is a dictionary
        if value:
            # If the dictionary is non-empty
            # we sample one of its items randomly.
            n = random.randint(0, len(value) - 1)
            # Here we are using islice with a starting position n and stopping at n + 1
            # to get a random key-value pair from the dictionary
            key, val = next(islice(value.items(), n, n + 1))
            # We return the type of the dictionary as 'dict[key_type: value_type]'
            return f"dict[{get_full_type(key)}: {get_full_type(val)}]"
        else:
            # If the dictionary is empty, we just return 'dict' as the type
            return "dict"
    elif isinstance(value, list):
        # Checking if the value is a list
        if value:
            # If the list is non-empty
            # we sample one of its elements randomly
            n = random.randint(0, len(value) - 1)
            elem = value[n]
            # We return the type of the list as 'list[element_type]'
            return f"list[{get_full_type(elem)}]"
        else:
            # If the list is empty, we return 'list'
            return "list"
    elif isinstance(value, tuple):
        # Checking if the value is a tuple
        # Here we are returning the types of all elements in the tuple
        return f"tuple[{', '.join((type(elem).__name__ for elem in value))}]"
    else:
        # If the value passed is not a dictionary, list, or tuple,
        # we return the type of the value as a string
        return type(value).__name__


def enter_function(code: CodeType, instruction_offset: int) -> str:
    """
    Process the function entry point, perform monitoring related operations,
    and manage the profiling of function execution.

    Args:
        code : CodeType object,
        instruction_offset (int): offset of the instruction,

    Returns:
        str: Status of monitoring
    """
    # Check if code.co_name is in EXCLUDED_FUNCTION_NAMES
    if code.co_name in EXCLUDED_FUNCTION_NAMES:
        # If the function name is in the excluded list, disable sys monitoring
        return sys.monitoring.DISABLE
    func_name = code.co_qualname
    filename = code.co_filename
    t = (filename, func_name)
    # If function details are already present in sampled_funcs
    if t in sampled_funcs:
        # AND the time to execute this function is less than THRESHOLD_TIME, the monitor will be disabled.
        if execution_time_funcs[t] < THRESHOLD_TIME:
            return sys.monitoring.DISABLE
    # Set start time of this function in the start_time_funcs dictionary
    start_time_funcs[t] = time.perf_counter_ns()
    # Assume the function takes THRESHOLD_TIME to execute, we'll modify this later when the function returns
    execution_time_funcs[t] = THRESHOLD_TIME
    sampled_funcs.add(t)
    # Add this function to visited_funcs
    visited_funcs.add(t)
    # To get arguments of the function we need to inspect the call stack
    frame = inspect.currentframe()
    # If the frame exists and it has a previous frame
    if frame is not None and frame.f_back is not None:
        args, _, _, values = inspect.getargvalues(frame.f_back)
        argtypes = []
        # Fetch function's arguments' types and values.
        for arg in args:
            value = values[arg]
            full_type_name = get_full_type(value)
            full_type_names = set()
            full_type_names.add(full_type_name)
            argtypes.append((arg, type(value), full_type_names))
        # If the function's arguments were recorded before
        if t in visited_funcs_arguments:
            for i, (arg, _, full_type_name_set) in enumerate(argtypes):
                if i < len(visited_funcs_arguments[t]):
                    _, old_type, old_type_name_set = visited_funcs_arguments[t][i]
                    # If the type of argument has changed
                    if full_type_name not in old_type_name_set:
                        # Update the type in the argument type set
                        old_type_name_set.add(full_type_name_set.pop())
        else:
            # If the function's arguments were not recorded before, start recording
            visited_funcs_arguments[t] = argtypes
    else:
        # If the frame does not exist or it does not have a previous frame, pass control
        pass
    # Continue monitoring for the return so we can get the return value type
    return sys.monitoring.events.C_RETURN


def exit_function(code: CodeType, instruction_offset: int, return_value: Any) -> int:
    """
    Function to gather statistics on a function call and determine
    whether it should be excluded from profiling, when the function exits.

    - If the function name is in the excluded list, it will disable the monitoring right away.
    - Otherwise, it calculates the execution time of the function, adds the type of the return value to a set for that function,
      and then disable the monitoring.

    Args:
    code (CodeType): bytecode of the function.
    instruction_offset (int): position of the current instruction.
    return_value (Any): return value of the function.

    Returns:
    int: indicator whether to continue the monitoring, always returns sys.monitoring.DISABLE in this function.
    """
    # Check if the function name is in the excluded list
    if code.co_name in EXCLUDED_FUNCTION_NAMES:
        return sys.monitoring.DISABLE
    func_name = code.co_qualname
    filename = code.co_filename
    t = (filename, func_name)
    # Calculate execution time
    execution_time_funcs[t] = (
        time.perf_counter_ns() - start_time_funcs[t]
    ) / 1000000000.0
    # Initialize if the function is first visited
    if t not in visited_funcs_retval:
        visited_funcs_retval[t] = set()
    # Add return value type to the set for the function
    if type(return_value) not in visited_funcs_retval[t]:
        visited_funcs_retval[t].add(type(return_value))
    return sys.monitoring.DISABLE


def handle_clear_seen_funcs(_signum: int, _frame: Optional[FrameType]) -> None:
    """
    This function handles the task of clearing the seen functions.
    Called when a particular signal is received.

    Args:
        _signum: The signal number
        _frame: The current stack frame
    """
    # Restarting the system monitoring events
    sys.monitoring.restart_events()
    # Clearing the sampled functions
    sampled_funcs.clear()
    # Setting a timer. When the timer expires, the signal will be sent to the process
    signal.setitimer(signal.ITIMER_REAL, SAMPLING_INTERVAL)


def output_type_signatures(file=sys.stdout):
    # Print all type signatures
    for filename, func_name in visited_funcs:
        if filename.startswith("/Library") or filename.startswith("<"):
            continue
        try:
            t = tuple([filename, func_name])
            args = visited_funcs_arguments[t]
            s = f"{filename}:def {func_name}("
            for index, (argname, argtype, argtype_fullname_set) in enumerate(args):
                if len(argtype_fullname_set) == 1:
                    argtype_fullname = argtype_fullname_set.pop()
                else:
                    argtype_fullname = "Union[" + ", ".join(argtype_fullname_set) + "]"
                s += f"{argname}: {argtype_fullname}"
                if index < len(args) - 1:
                    s += ", "
            s += ")"
            if len(visited_funcs_retval[t]) == 1:
                retval_name = get_full_type_name(visited_funcs_retval[t].pop())
            else:
                retval_name = (
                    "Union["
                    + ", ".join(
                        (get_full_type_name(t) for t in visited_funcs_retval[t])
                    )
                    + "]"
                )
            s += f" -> {retval_name}"
            print(s, file=file)
        except KeyError:
            # Something weird happened
            pass


def main() -> None:
    """
    This function defines the entry point of the program.
    It checks the command line arguments, sets up monitoring, registers callbacks
    sets timers for periodic clearing, executes the script given as argument,
    turns off monitoring, and finally writes out the type signatures.
    """
    # Check if the number of command line arguments is valid.
    if len(sys.argv) < 2:
        print(f"Usage: {TOOL_NAME} <script.py> [args...]", file=sys.stderr)
        sys.exit(1)
    script_path = sys.argv[1]
    # Adjust the command line arguments for the script.
    sys.argv = sys.argv[1:]
    # Use the condition monitoring tool with the given tool identifier and name.
    sys.monitoring.use_tool_id(TOOL_ID, TOOL_NAME)
    # Set the events for monitoring.
    sys.monitoring.set_events(
        TOOL_ID, sys.monitoring.events.PY_START | sys.monitoring.events.PY_RETURN
    )
    # Register callbacks for the monitoring events.
    sys.monitoring.register_callback(
        TOOL_ID, sys.monitoring.events.PY_START, enter_function
    )
    sys.monitoring.register_callback(
        TOOL_ID, sys.monitoring.events.PY_RETURN, exit_function
    )
    # Set up a timer to allow periodic merging of types, set the signal handler for timer signal.
    signal.signal(signal.SIGALRM, handle_clear_seen_funcs)
    # Schedule the first timer event.
    signal.setitimer(signal.ITIMER_REAL, SAMPLING_INTERVAL)
    # Run the script specified in the command line arguments.
    runpy.run_path(script_path, run_name="__main__")
    # We register None callbacks (i.e., turning off callbacks) to stop monitoring.
    sys.monitoring.register_callback(TOOL_ID, sys.monitoring.events.PY_START, None)
    sys.monitoring.register_callback(TOOL_ID, sys.monitoring.events.PY_RETURN, None)
    # Free the tool ID after execution of script.
    sys.monitoring.free_tool_id(TOOL_ID)
    # At the end of the script, we output the type signatures we have monitored so far.
    with open("typewriter.out", "w+") as f:
        output_type_signatures(f)


if __name__ == "__main__":
    main()
