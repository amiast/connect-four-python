# Connect Four

Play Connect Four in your CLI with a friend or with a computer! Featuring:

- **Customizable board dimension** - things get wild in a 20 x 20 board
- **Intellegent Auto-Player implementing naive look-ahead strategy** - it runs in $O(h^2w^{d+2})$ time, but it's trying its best...!

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)

## Prerequisites

- Python 3.12+

## Installation

Clone this repository to your machine and navigate to the project directory.
You can find help on doing this [here](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository).


(Optional but recommended) set up a virtual environment in the same directory:
```
# Linux / macOS
$ python3 -m venv .venv
$ . .venv/bin/activate

# Windows
> py -3 -m venv .venv
> .venv\Scripts\activate
```

Next, install the python package using pip.

```
$ pip install .
```

Now you are ready to play!

## Usage

To start playing with an auto-player, use the following command:

```
$ play-cf
```

You can pass the following options to customize your game:

| Option     | Value                          | Description |
| ---------- | ------------------------------ | ----------- |
| `--p1`     | `manual`, `random` or a number | Indicates whether player 1 is controlled manually or by a bot. <br> A `random` player makes decisions randomly. <br> A number indicates the number of moves the auto-player should compute. |
| `--p2`     | `manual`, `random` or a number | Option for player 2; see above.          |
| `--width`  | a number                       | The number of columns in the game board. |
| `--height` | a number                       | The number of rows in the game board.    |

For example, the following command initates a game between two auto-players that compute 6 moves in each turn.

```
$ play-cf --p1 6 --p2 6
```

To see detailed help, use

```
$ play-cf --help
```

## Testing

To run the tests provided in the `tests` directory, install the necessary modules first:

```
$ pip install -r test_requirements.txt
```

Then run the tests with

```
$ coverage run -m pytest
```

To generate a report, either use

```
$ coverage report
```

or

```
$ coverage html
```
