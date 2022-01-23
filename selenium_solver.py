from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

from word_bank import WordBank, DoesNotContain, ContainedElsewhere, CorrectLocation
from puzzle_solver import read_source_file


class SeleniumSolver:

    def __init__(self, driver, word_bank: WordBank):
        self.driver = driver
        self.word_bank = word_bank

    def load_wordle(self):
        self.driver.get("https://www.powerlanguage.co.uk/wordle/")
        time.sleep(3)
        body_element = self.driver.find_element(By.TAG_NAME, "body")
        body_element.click()

    def enter_guess(self, word: str):
        actions = ActionChains(self.driver)
        for char in word:
            actions.send_keys(char)
            actions.perform()
        actions.send_keys(Keys.ENTER)
        actions.perform()

    def clear_guess(self):
        actions = ActionChains(self.driver)
        for i in range(5):
            actions.send_keys(Keys.BACKSPACE)
            actions.perform()

    def _get_shadow_root(self, element):
        return self.driver.execute_script('return arguments[0].shadowRoot', element)

    def read_row(self, guess: str, n: int):
        constraints = set()
        game_app = driver.find_element(By.CSS_SELECTOR, 'body > game-app')
        game = self._get_shadow_root(game_app).find_element(By.CSS_SELECTOR, '#game')
        row = game.find_element(By.CSS_SELECTOR, f'#board > game-row:nth-child({n + 1})')
        tiles = self._get_shadow_root(row).find_elements(By.CSS_SELECTOR, f'div > game-tile')
        for idx, tile in enumerate(tiles):
            tile_type = tile.get_attribute('evaluation')
            if tile_type == 'absent':
                constraints.add(DoesNotContain(guess[idx]))
            elif tile_type == 'present':
                constraints.add(ContainedElsewhere(guess[idx], idx))
            elif tile_type == 'correct':
                constraints.add(CorrectLocation(guess[idx], idx))
        return constraints

    def solve(self):
        count = 0
        self.load_wordle()
        constraints = set()
        while count < 6:
            guess_word_exists = False
            while not guess_word_exists:
                if count == 0:
                    guess = self.word_bank.first_guess()
                else:
                    guess = self.word_bank.guess(list(constraints))
                self.enter_guess(guess)
                time.sleep(3)
                new_constraints = self.read_row(guess, count)
                if len(new_constraints) > 0:
                    guess_word_exists = True
                else:
                    self.clear_guess()
                constraints = constraints.union(new_constraints)
            count += 1


if __name__ == '__main__':
    source_words = read_source_file("five_letter_words.txt")
    bank = WordBank.from_word_list(source_words)
    driver = webdriver.Chrome(executable_path="./chromedriver")
    SeleniumSolver(driver, bank).solve()