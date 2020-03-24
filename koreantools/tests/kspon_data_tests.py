#-*- coding:utf-8 -*-
from unittest import TestCase

from koreantools.utils.korean_utils import clean_kspon, replace_number_token, remove_erroneous_tags

class TestKspon(TestCase):
    def test_remove_erroneous(self):
        raw_token = "o/ b/ 그게 가정의 아이들과 가정의 모습이야? b/"
        expected_token = "그게 가정의 아이들과 가정의 모습이야?"

        self.assertEqual(remove_erroneous_tags(raw_token), expected_token)

    def test_remove_erroneous2(self):
        raw_token = "o/ 그래가지고 진짜 차 사야겠다 아니 뭐/ 차 안 되면 스쿠터라도 타야되겠다 막/ 그런 생각 들더라구 그래서 운전은 하는 게 좋은 거 같애 진짜 b/"
        expected_token = "그래가지고 진짜 차 사야겠다 아니 뭐 차 안 되면 스쿠터라도 타야되겠다 막 그런 생각 들더라구 그래서 운전은 하는 게 좋은 거 같애 진짜"

    def test_replace_number(self):
        raw_token = "o/ 나도 몰라. 나 그/ (3G)/(쓰리 쥐)* 하나도 안 봤음. 어."
        expected_token = "o/ 나도 몰라. 나 그/ 3G* 하나도 안 봤음. 어."
        self.assertEqual(replace_number_token(raw_token), expected_token)

    def test_replace_number2(self):
        raw_token = "o/ b/ 그게 (0.1프로)/(영 점 일 프로) 가정의 아이들과 가정의 모습이야? b/"
        expected_token = "o/ b/ 그게 0.1프로 가정의 아이들과 가정의 모습이야? b/"
        self.assertEqual(replace_number_token(raw_token), expected_token)

    def test_long_text(self):
        raw_token = "기능사는 b/ 가서 일을 하는 사람들이고 b/ 내가 만약 기사랑 기능장이 있어 b/ 그럼 회사에서 연락이 와. 아 우리 회사에 그냥 들어오고 일은 안 해도 된다 그 대신 한 달에 (150)/(백 오십) 씩 주겠다 말을 해."
        expected_token = "기능사는 가서 일을 하는 사람들이고 내가 만약 기사랑 기능장이 있어 그럼 회사에서 연락이 와. 아 우리 회사에 그냥 들어오고 일은 안 해도 된다 그 대신 한 달에 150 씩 주겠다 말을 해."
        clean_token = clean_kspon(raw_token)
        self.assertEqual(clean_token, expected_token)

    def test_clean(self):
        raw_token = "o/ b/ 그게 (0.1프로)/(영 점 일 프로) 가정의 아이들과 (3G)/(쓰리 쥐)* 가정의 모습이야? b/"
        expected_token = "그게 0.1프로 가정의 아이들과 3G 가정의 모습이야?"
        clean_token = clean_kspon(raw_token)
        self.assertEqual(clean_token, expected_token)

