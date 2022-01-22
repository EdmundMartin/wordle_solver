
# Simple Wordle Solver

Makes use of a English wordlist and applies constraints based on user input. Typically, solves puzzles within 3 - 5
guesses, highly dependent on set of constraints revealed by first guess.

Example usage
```
-> python puzzle_solver.py
First Guess: think
Awaiting Input: 
missing t
Awaiting Input: 
missing h
Awaiting Input: 
elsewhere i 2
Awaiting Input: 
elsewhere n 3
Awaiting Input: 
missing k
Awaiting Input: 
guess
Found 390 candidate words
Next Guess is: miner
Awaiting Input: 
missing m
Awaiting Input: 
missing r
Awaiting Input: 
correct i 1
Awaiting Input: 
correct n 2
Awaiting Input: 
elsewhere e 3
Awaiting Input: 
guess
Found 9 candidate words
Next Guess is: pince
Awaiting Input: 
guess
Found 9 candidate words
Next Guess is: winge
```

## TODO
* Add Selenium client - allowing for solving puzzles with zero user input
* Proper CLI Interface