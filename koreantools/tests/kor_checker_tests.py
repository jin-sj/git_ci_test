#-*- coding:utf-8 -*-
import os
import string
from unittest import TestCase

from koreantools.utils.korean_utils import KorChecker
class TestKorChecker(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(os.path.dirname(cls.test_dir), "data")
        dictionary_dir = os.path.join(data_dir, "dic_system.txt")
        lookup_dir = os.path.join(data_dir, "common_errors.json")
        cls.kor = KorChecker(dictionary_dir, lookup_dir)

    def test_lookup_table(cls):
        token = "않해"
        expected_token = "안 해"
        result = cls.kor.fix_korean_spelling(token)
        cls.assertEqual(result, expected_token)

    def test_dictionary(cls):
        token = "핸드폰"
        expected_token = "핸드폰"
        result = cls.kor.fix_korean_spelling(token)
        cls.assertEqual(result, expected_token)

    def test_name(cls):
        token = "이승철"
        expected_token = "이승철"
        result = cls.kor.fix_korean_spelling(token)
        cls.assertEqual(result, expected_token)

    def test_not_found(cls):
        # Expect to see logs for words that weren't found
        token = "얎"
        expected_token = "얎"
        result = cls.kor.fix_korean_spelling(token)
        cls.assertEqual(result, expected_token)

