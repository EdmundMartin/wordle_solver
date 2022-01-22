from word_bank import (
    WordBank,
    CorrectLocation,
    ContainedElsewhere,
    DoesNotContain,
)
from typing import List


def read_source_file(filename: str) -> List[str]:
    results = []
    with open(filename, "r") as input_file:
        for line in input_file:
            results.append(line.strip())
    return results


class Solver:
    def __init__(self, word_bank: WordBank):
        self.word_bank = word_bank
        self.all_constraints = set()

    def solve(self):
        first_guess = self.word_bank.first_guess()
        print("First Guess: {}".format(first_guess))
        while True:
            print('Awaiting Input: ')
            user_input = input()
            inputs = user_input.split(" ")
            try:
                if inputs[0] == "guess":
                    guess = self.word_bank.guess(list(self.all_constraints))
                    print(f"Next Guess is: {guess}")
                elif inputs[0] == "missing":
                    self.all_constraints.add(DoesNotContain(inputs[1]))
                elif inputs[0] == "elsewhere":
                    self.all_constraints.add(
                        ContainedElsewhere(inputs[1], int(inputs[2]))
                    )
                elif inputs[0] == "correct":
                    self.all_constraints.add(
                        CorrectLocation(inputs[1], int(inputs[2]))
                    )
                elif inputs[0] == "solved":
                    return
            except Exception:
                print("Invalid Input please try again")


if __name__ == "__main__":
    source_words = read_source_file("five_letter_words.txt")
    bank = WordBank.from_word_list(source_words)
    solver = Solver(bank)
    solver.solve()
