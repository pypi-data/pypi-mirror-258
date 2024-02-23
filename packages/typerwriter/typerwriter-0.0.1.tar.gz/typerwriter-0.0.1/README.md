# Typewriter

Typewriter is a Python tool that generates types for your function
arguments and return values. It produces much the same results as
Instagram's `monkeytype`, while being both more flexible and
**vastly** more efficient. Unlike `monkeytype`, which can slow down
your code more than tenfold and cause it to consume huge amounts of
memory, `typewriter` lets your code run at nearly full speed with
almost no memory overhead.

## `typewriter`: high performance

In the below example drawn from the pyperformance benchmark suite,
`monkeytype` runs **30x slower** than the original program or when
running with `typewriter` (which runs under 3% slower).

```bash
% python3 bm_mdp          
Time elapsed:  6.106977417017333
% typewriter bm_mdp
Time elapsed:  6.299191833997611
% monkeytype run bm_mdp
Time elapsed:  184.57902495900635
```

# `typewriter`: low memory consumption

With `monkeytype`, this program also consumes 5GB of RAM; the original
consumes just 21MB. That's an over **200x** increase in memory
consumption. `monkeytype` also leaves behind a 3GB SQLite file.

By contrast, `typewriter`'s memory consumption is just a small
increment over the original program: it consumes about 24MB, just 15%
more.

_NOTE: this is an alpha release and is not production ready._

## Requirements

- Python 3.12 or higher

## Installation

```bash
python3 -m pip install typewriter
```

## Usage

To use Typewriter, simply run your script with `typewriter` instead of `python3`:

```bash
typewriter your_script.py [args...]
```

This will execute `your_script.py` with Typewriter's monitoring enabled. The type signatures of all functions will be recorded and output to a file named `typewriter.out`. Each line represents a function signature in the following format:

```
filename:def function_name(arg1: arg1_type, arg2: arg2_type, ...) -> return_type
```

## Contributing

Contributions are welcome! Feel free to submit pull requests or report issues [on the GitHub repository](https://github.com/plasma-umass/typewriter).

## License

This project is licensed under the Apache License. See the [LICENSE](LICENSE) file for details.