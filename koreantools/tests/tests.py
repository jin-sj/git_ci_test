#-*- coding:utf-8 -*-

import string
from unittest import TestCase

from koreantools.korean_parser import KoreanParser
from koreantools.constants import MARKERS

class TestPen(TestCase):
    def test_penning_length(self):
        parser = KoreanParser()
        text = '야! 너두 영어 할 수 있어. 왜? 그냥 그래. 바보야, 자신감을 가져.'
        actual_stripped_text, actual_mapping = parser.penning(text)
        self.assertTrue(len(actual_stripped_text) == len(actual_mapping) - 1,
                        msg="len(stripped)={}, len(mapping)={}".format(len(actual_stripped_text), len(actual_mapping)))

    def test_split_token_timestamp(self):
        token = "[time:0.7]자리잡았어요?"
        head_marker = "[time:0.7]"
        stripped_token = "자리잡았어요"
        end_marker = "?"
        actual_head_marker, actual_stripped_token, actual_end_marker = KoreanParser.split_token(token)
        self.assertEqual(head_marker, actual_head_marker,
                         msg="Head markers differ: {} != {}".format(head_marker, actual_head_marker))
        self.assertEqual(stripped_token, actual_stripped_token,
                         msg="Stripped tokens differ: {} != {}".format(stripped_token, actual_stripped_token))
        self.assertEqual(end_marker, actual_end_marker,
                         msg="End markers differ: {} != {}".format(end_marker, actual_end_marker))

    def test_split_token_markers(self):
        for marker in MARKERS:
            token = marker
            head_marker = marker
            stripped_token = ""
            end_marker = ""
            actual_head_marker, actual_stripped_token, actual_end_marker = KoreanParser.split_token(token)
            self.assertEqual(head_marker, actual_head_marker,
                             msg="Head markers differ: {} != {}".format(head_marker, actual_head_marker))
            self.assertEqual(stripped_token, actual_stripped_token,
                             msg="Stripped tokens differ: {} != {}".format(stripped_token, actual_stripped_token))
            self.assertEqual(end_marker, actual_end_marker,
                             msg="End markers differ: {} != {}".format(end_marker, actual_end_marker))


    def test_repeated_markers(self):
        text = '야! 너두 [unsure] [unsure] 영어 할 수 있어. 왜? 그냥 그래. 바보야, 자신감을 가져.'
        expected_stripped_text = ['야', '너두', '영어', '할', '수', '있어', '왜', '그냥', '그래', '바보야', '자신감을', '가져']
        expected_mapping = ['', '! ', ' [unsure] [unsure] ', ' ', ' ', ' ', '. ', '? ', ' ', '. ', ', ', ' ', '.']

        parser = KoreanParser()
        actual_stripped_text, actual_mapping = parser.penning(text)
        self.assertListEqual(expected_stripped_text, actual_stripped_text)
        self.assertListEqual(expected_mapping, actual_mapping)


    def test_penning_punctuation(self):
        text = '야! 너두 영어 할 수 있어. 왜? 그냥 그래. 바보야, 자신감을 가져.'
        expected_stripped_text = ['야', '너두', '영어', '할', '수', '있어', '왜', '그냥', '그래', '바보야', '자신감을', '가져']
        expected_mapping = ['',
                            '! ',
                            ' ',
                            ' ',
                            ' ',
                            ' ',
                            '. ',
                            '? ',
                            ' ',
                            '. ',
                            ', ',
                            ' ',
                            '.']

        parser = KoreanParser()
        actual_stripped_text, actual_mapping = parser.penning(text)
        self.assertListEqual(expected_stripped_text, actual_stripped_text)
        self.assertListEqual(expected_mapping, actual_mapping)

    def test_penning_markers(self):
        text = '[SPEAKER 1:] 야! 너두 영어 할 [unsure] 수 있어. 왜? 그냥 그래. 바보야, 자신감을 가져 ...'
        expected_stripped_text = ['야', '너두', '영어', '할', '수', '있어', '왜', '그냥', '그래', '바보야', '자신감을', '가져']
        expected_mapping = ['[SPEAKER 1:] ',
                            '! ',
                            ' ',
                            ' ',
                            ' [unsure] ',
                            ' ',
                            '. ',
                            '? ',
                            ' ',
                            '. ',
                            ', ',
                            ' ',
                            ' ...']

        parser = KoreanParser()
        actual_stripped_text, actual_mapping = parser.penning(text)
        self.assertListEqual(expected_stripped_text, actual_stripped_text)
        self.assertListEqual(expected_mapping, actual_mapping)

    def test_penning_timestamp(self):
        text = '[time:0.7]자리잡았어요? [time:3.0]그렇다면 [time:3.8]잠깐만요. [time:13.5]그럼 [time:14.0]시작해 [time:14.3]볼까요.'
        expected_stripped_text = ["자리잡았어요", "그렇다면", "잠깐만요", "그럼", "시작해", "볼까요"]
        expected_mapping = ["[time:0.7]", "? [time:3.0]", " [time:3.8]", ". [time:13.5]", " [time:14.0]", " [time:14.3]",
                            "."]
        parser = KoreanParser()
        actual_stripped_text, actual_mapping = parser.penning(text)
        self.assertListEqual(expected_stripped_text, actual_stripped_text)
        self.assertListEqual(expected_mapping, actual_mapping)

    def test_digit(self):
        text = "[time:0.1]50. [time:0.7]자리잡았어요? [time:3.0]그렇다면 [time:3.8]잠깐만요. [time:13.5]그럼 [time:14.0]시작해 [time:14.3]볼까요."
        expected_stripped_text = ["50", "자리잡았어요", "그렇다면", "잠깐만요", "그럼", "시작해", "볼까요"]
        expected_mapping = ["[time:0.1]", ". [time:0.7]", "? [time:3.0]", " [time:3.8]", ". [time:13.5]", " [time:14.0]",
                            " [time:14.3]", "."]
        parser = KoreanParser()
        actual_stripped_text, actual_mapping = parser.penning(text)
        self.assertListEqual(expected_stripped_text, actual_stripped_text)
        self.assertListEqual(expected_mapping, actual_mapping)

