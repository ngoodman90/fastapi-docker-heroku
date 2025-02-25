from dataclasses import dataclass
from typing import List, Set

from .anagram_checker import is_word_avaliable, get_steal, get_needed_letters
from .exceptions import InvalidWordException, MissingLettersForWordException, NoLettersLeftException
from .player import Player


@dataclass
class OrderedLetter(object):
    letter: str
    letterID: int


class Board(object):
    def __init__(self, letter_order: List[str], dictionary: Set[str]):
        self._remainining_letters = [OrderedLetter(
            letter, letterID) for letterID, letter in enumerate(letter_order)]
        self._dictionary = dictionary
        self._current_letters = list()  # type: list[OrderedLetter]

    def current_letters(self):
        return [ordered_letter.letter for ordered_letter in self._current_letters]

    def current_ordered_letters(self):
        return self._current_letters

    def _remove_letter(self, letter: str):
        for ordered_letter in self._current_letters:
            if ordered_letter.letter == letter:
                self._current_letters.remove(ordered_letter)
                return
        raise RuntimeError("Invalid letters state")

    def _remove_letters(self, letters: List[str]):
        for letter in letters:
            self._remove_letter(letter)

    def _check_valid_word(self, word):
        if word not in self._dictionary:
            raise InvalidWordException(word)

    def take_word(self, player: Player, word):
        self._check_valid_word(word)
        if is_word_avaliable(word, self.current_letters()):
            self._remove_letters(word)
            player.add_word(word)
        else:
            raise MissingLettersForWordException(word)

    def steal_word(self, word, current_player: Player, target_player: Player):
        self._check_valid_word(word)
        stolen_word = get_steal(
            word, target_player.words, self.current_letters())
        target_player.remove_word(stolen_word)
        current_player.add_word(word)
        self._remove_letters(letters=get_needed_letters(stolen_word, word))

    def flip_letter(self):
        if len(self._remainining_letters) == 0:
            raise NoLettersLeftException()
        result_letter = self._remainining_letters.pop()
        self._current_letters.append(result_letter)
        return result_letter

    def remaining_letters_count(self):
        return len(self._remainining_letters)
