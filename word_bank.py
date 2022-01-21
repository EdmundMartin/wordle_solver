from typing import Dict, List, Set
from string import ascii_lowercase
from random import choice
from typing import Protocol


class Constraint(Protocol):
    def passes_constraint(self, word: str) -> bool:
        ...


class DoesNotContain:
    def __init__(self, letter: str):
        self.letter = letter

    def passes_constraint(self, word: str) -> bool:
        return self.letter not in word


class ContainedElsewhere:
    def __init__(self, letter: str, idx: int):
        self.letter = letter
        self.idx = idx

    def passes_constraint(self, word: str) -> bool:
        return word[self.idx] != self.letter and self.letter in word


class CorrectLocation:
    def __init__(self, letter: str, idx: int):
        self.letter = letter
        self.idx = idx

    def passes_constraint(self, word: str) -> bool:
        return word[self.idx] == self.letter


class Entry:
    def __init__(self, char: str):
        self.char = char
        self.indexes = {0: set(), 1: set(), 2: set(), 3: set(), 4: set()}

    def add_word(self, target_word):
        for idx, char in enumerate(target_word):
            if char == self.char:
                self.indexes[idx].add(target_word)

    def __str__(self):
        return f"<Entry: {self.indexes}>"


class WordBank:
    def __init__(self):
        self.initial_guess = "works"
        self.all_words = set()
        self.entries: Dict[str, Entry] = {}
        for char in ascii_lowercase:
            self.entries[char] = Entry(char)

    @classmethod
    def from_word_list(cls, word_list: List[str]):
        bank = cls()
        first_guesses = []
        for word in word_list:
            if len(set(word)) == 5:
                first_guesses.append(word)
            bank.all_words.add(word)
            for char in word:
                bank.entries[char].add_word(word)
        bank.initial_guess = choice(first_guesses)
        return bank

    def first_guess(self) -> str:
        return self.initial_guess

    def _all_words_for_different_idx_constraint(
        self, constraint: ContainedElsewhere
    ) -> Set[str]:
        results = set()
        for key, value in self.entries[constraint.letter].indexes.items():
            if key == constraint.idx:
                continue
            results = results.union(value)
        return results

    def _all_words_for_same_idx_constraint(
        self, constraint: CorrectLocation
    ) -> Set[str]:
        return self.entries[constraint.letter].indexes[constraint.idx]

    def _get_candiates(self, constraints: List[Constraint]) -> Set[str]:
        unique_words = set()
        if any(
            [
                isinstance(c, ContainedElsewhere)
                or isinstance(c, CorrectLocation)
                for c in constraints
            ]
        ):
            for constraint in constraints:
                if isinstance(constraint, ContainedElsewhere):
                    unique_words = unique_words.union(
                        self._all_words_for_different_idx_constraint(constraint)
                    )
                if isinstance(constraint, CorrectLocation):
                    unique_words = unique_words.union(
                        self._all_words_for_same_idx_constraint(constraint)
                    )
        else:
            return self.all_words
        return unique_words

    def possible_words(self, constraints: List[Constraint]) -> Set[str]:
        unique_words = self._get_candiates(constraints)
        filtered_words = set()
        for word in unique_words:
            if all([constraint.passes_constraint(word) for constraint in constraints]):
                filtered_words.add(word)
        return filtered_words

    def guess(self, constraints: List[Constraint]) -> str:
        results = self.possible_words(constraints)
        print(f'Found {len(results)} candidate words')
        return choice(list(results))
