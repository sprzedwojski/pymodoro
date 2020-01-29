# Pymodoro

Pomodoro timer for macOS, which turns on the DND (Do Not Disturb) mode for the pomodoro's duration.

### Prerequisites

#### do-not-disturb-cli

This project uses the [`do-not-disturb-cli`](https://github.com/sindresorhus/do-not-disturb-cli)
node.js program to control the macOS DND mode.

You need to have it installed globally for Pymodoro to work correcty.

```
$ npm install --global do-not-disturb-cli
```

#### Python 3

To run Pymodoro you need to have [Python 3 installed](https://www.python.org/downloads/).

### Usage

Run Pymodoro from the command line, passing in a single argument
specifying the duration of the pomodoro.

Pymodoro will enable the DND macOS mode for that time to block all
notifications and allow you to work peacefully.

Example use:
```
$ python3 pymodoro.py 25
```

Output:
```
Pomodoro started, you have 25 minutes
DND on
25 minutes left
24 minutes left
23 minutes left
22 minutes left
21 minutes left
20 minutes left
19 minutes left
18 minutes left
17 minutes left
16 minutes left
15 minutes left
14 minutes left
13 minutes left
12 minutes left
11 minutes left
10 minutes left
9 minutes left
8 minutes left
7 minutes left
6 minutes left
5 minutes left
4 minutes left
3 minutes left
2 minutes left
1 minutes left
Pomodoro finished
DND off
```
