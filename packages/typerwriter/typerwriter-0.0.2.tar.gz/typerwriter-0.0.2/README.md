# Typerwriter

Typerwriter is a Python tool that generates types for your function
arguments and return values. It produces much the same results as
Instagram's `monkeytype`, while being both more flexible and
**vastly** more efficient. Unlike `monkeytype`, which can slow down
your code more than tenfold and cause it to consume huge amounts of
memory, `typerwriter` lets your code run at nearly full speed with
almost no memory overhead.

## `typerwriter`: high performance

In the below example drawn from the pyperformance benchmark suite,
`monkeytype` runs **30x slower** than the original program or when
running with `typerwriter` (which runs under 3% slower).

```bash
% python3 bm_mdp          
Time elapsed:  6.106977417017333
% typerwriter bm_mdp
Time elapsed:  6.299191833997611
% monkeytype run bm_mdp
Time elapsed:  184.57902495900635
```

# `typerwriter`: low memory consumption

With `monkeytype`, this program also consumes 5GB of RAM; the original
consumes just 21MB. That's an over **200x** increase in memory
consumption. `monkeytype` also leaves behind a 3GB SQLite file.

By contrast, `typerwriter`'s memory consumption is just a small
increment over the original program: it consumes about 24MB, just 15%
more.

_NOTE: this is an alpha release and is not production ready._

## Requirements

- Python 3.12 or higher

## Installation

```bash
python3 -m pip install typerwriter
```

## Usage

To use Typerwriter, simply run your script with `typerwriter` instead of `python3`:

```bash
typerwriter your_script.py [args...]
```

This will execute `your_script.py` with Typerwriter's monitoring enabled. The type signatures of all functions will be recorded and output to a file named `typerwriter.out`. Each line represents a function signature in the following format:

```
filename:def function_name(arg1: arg1_type, arg2: arg2_type, ...) -> return_type
```

## Contributing

Contributions are welcome! Feel free to submit pull requests or report issues [on the GitHub repository](https://github.com/plasma-umass/typerwriter).

## License

This project is licensed under the Apache License. See the [LICENSE](LICENSE) file for details.