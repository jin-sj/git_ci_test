import logging
import json
import re
import sys

from typing import Dict
from konlpy.tag import Okt

NOUN = "Noun"

log_path = "/tmp/kor_checker_logging.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)-5.5s] %(message)s",
    handlers=[
        logging.FileHandler("{0}".format(log_path)),
        logging.StreamHandler(sys.stdout)
    ])

LOG = logging.getLogger(__name__)

def replace_double_space(token: str) -> str:
    """ Finds and replaces all double or more spaces

        Args:
            token (str): Token to inspect
        Returns:
            token with double or more spaces replaced with single space
    """
    return re.sub(r"\s{2,}", " ", token).strip()

def remove_erroneous_tags(token: str) -> str:
    """ Removes erroneous tags found in the transcript

        Args:
            token (str): Token to inspect

        Returns:
            Token with tags removed
    """
    replaced = token
    erroneous_tags = [r"n/", r"b/", r"o/", r"\/", r"\+", r"\*"]
    for tag in erroneous_tags:
        replaced = re.sub(tag, "", replaced)
    return replaced.strip() # remove trailing whitespace

def replace_number_token(token: str) -> str:
    """ Replaces number annotations eg. '(150)/(백오십)' to '150'

        Args:
            token (str): Token to inspect

        Returns:
            Token with number annotation removed
    """
    pattern = r"\([가-힣\s\.\d\w]+\)\/\([가-힣\s\.\d]+\)"
    matches = re.findall(pattern, token)
    for match in matches:
        replace = get_replace_number_token(match)
        token = token.replace(match, replace)
    return token

def get_replace_number_token(token: str) -> str:
    """ Finds the desired original number annotation

        Args:
            token (str): Token to inspect

        Returns:
            Original number annotation
    """
    replace = ""
    for char in token:
        if char == '(':
            continue
        elif char == ')':
            break
        replace += char
    return replace

def clean_kspon(token: str) -> str:
    """ Cleans transcription from kspon data

        Args:
            token (str): Token to inspect

        Returns:
            Cleaned token
    """
    token = replace_number_token(token)
    token = remove_erroneous_tags(token)
    token = replace_double_space(token)
    return token

class KorChecker:
    def __init__(self, path_to_dictionary: str, path_to_lookup_table: str) -> Dict[str, str]:
        self._dictionary = self._read_dictionary(path_to_dictionary)
        self._lookup_table = self._read_lookup_table(path_to_lookup_table)
        self._okt = Okt()

    def _read_dictionary(self, path_to_dictionary: str) -> Dict[str, str]:
        data = {}
        with open(path_to_dictionary) as reader:
            line = reader.readline()
            word = ""
            pos = ""
            while line:
                split = line.split()
                word, pos = split[0], split[1]
                data[word] = pos
                line = reader.readline()
        return data

    def _read_lookup_table(self, path_to_lookup_table: str) -> Dict[str, str]:
        with open(path_to_lookup_table) as json_file:
            data = json.load(json_file)
        return data

    def _check_lookup_table(self, word: str) -> bool:
        return word in self._lookup_table

    def _check_dictionary(self, word: str) -> bool:
        return word in self._dictionary

    def fix_korean_spelling(self, word: str) -> str:
        fixed_word = ""
        if word in self._lookup_table:
            return self._lookup_table[word]
        if word in self._dictionary:
            return word
        tagging = self._okt.pos(word)
        for token, tag in tagging:
            if tag == NOUN:
                if self._check_dictionary(token):
                    fixed_word += token
                elif self._check_lookup_table(token):
                    fixed_word += self._lookup_table[token]
                else:
                    LOG.error("%s not found in the dictionary", token)
                    return token
            else:
                fixed_word += token
        return fixed_word
