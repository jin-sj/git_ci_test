"""Support preprocessing of various formats of korean text data"""
import re
from typing import List, Tuple

class KoreanParser:
    """Support preprocessing of various formats of korean text data"""
    def fix_spelling(self, word: str) -> str:
        return word

    def fix_spacing(self, text: str) -> str:
        """ Fixes spacing problems ins korean text.

        Args:
            text (str): Original text to fix spacing

        Returns:
            fixed_text (str): Text with spacing fixes
        """
        return text

    def penning(self, text: str) -> Tuple[List[str], List[str]]:
        """ Creates a mapping of punctuation and markers from original to stripped text

        Args:
            text (str): Original text to map

        Returns:
            stripped_tokens: relevant tokens without punctuation, markers
            punctuation_mapping: mapping back to original

        Raises:
            None
        """
        stripped_tokens = []
        punctuation_mapping = []
        original = text.split(' ')
        speaker = ' '.join(original[:2])
        # Check if sentence starts with [SPEAKER 1:]
        if re.match(r"\[SPEAKER \d+?\:]", speaker):
            punctuation_mapping.append("%s" % speaker)
            original = original[2:]
        for i, token in enumerate(original):
            prev = None
            if len(punctuation_mapping) > 0:
                prev = punctuation_mapping[-1]
            head_marker, stripped_token, end_marker = KoreanParser.split_token(token)
            if stripped_token:
                stripped_tokens.append(stripped_token)
                if i == 0 and len(punctuation_mapping) == 0:
                    punctuation_mapping.append(head_marker)
                else: # Marker in somewhere in between
                    punctuation_mapping[-1] = "%s %s" % (prev, head_marker)
                punctuation_mapping.append(end_marker)
            else: # no text, only marker found
                if i == 0 and len(punctuation_mapping) == 0:
                    punctuation_mapping.append("%s " % head_marker)
                else:
                    punctuation_mapping[-1] = "%s %s" % (prev, head_marker)

        return stripped_tokens, punctuation_mapping

    @staticmethod
    def split_token(token: str) -> Tuple[str, str, str]:
        """ Strip a token from markers and puncutation so that only relevant text remains

        Args:
            token (str): Token with markers, punctuation

        Returns:
            head_marker (str): Any marker preceding the text
            stripped_token (str): Relevant text w/o markers and punctuation
            end_marker (str): Any marker/punctuation after the text

        Raises:
            None
        """
        head_marker, stripped_token, end_marker = "", "", ""
        if not token:
            return head_marker, stripped_token, end_marker

        marker_pattern = r"^(\[\w+\])?(\.{3})?(-{2})?$"
        marker_matcher = re.match(marker_pattern, token)
        if marker_matcher:
            return marker_matcher.group(), "", ""

        # Need to consider:
        # token with only number
        # token with only non-korean
        # token with timestamp + number
        # token with timestamp + non-korean

        timestamp_pattern = r"(\[time:\d+?\.\d+?\])"
        timestamp_matcher = re.match(timestamp_pattern, token)
        if timestamp_matcher:
            result = re.split(timestamp_pattern, token)
            recursive_head_marker, recursive_stripped_token, recursive_end_marker =\
                    KoreanParser.split_token(result[2])
            head_marker = "".join([result[1], recursive_head_marker])
            stripped_token = recursive_stripped_token
            end_marker = recursive_end_marker
            return head_marker, stripped_token, end_marker

        korean_pattern = r"([가-힣\d]+)"
        korean_matcher = re.search(korean_pattern, token)
        if korean_matcher:
            result = re.split(korean_pattern, token)
            return result[0], result[1], result[2]

        return head_marker, stripped_token, end_marker
