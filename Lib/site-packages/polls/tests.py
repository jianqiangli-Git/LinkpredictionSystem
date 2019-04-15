from django.test import TestCase

# Create your tests here.
import datetime
from django.utils import timezone

from .models import Question


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

# manage.py test polls 在polls应用中查找tests
# 发现 django.test.TestCase 类的子类
# 为了测试的目的创建一个特殊的数据库
# 查找test方法--它的名字是以test开头的
# 在 test_was_published_recently_with_future_question 中创建一个 Question 实例他的 pub_date field 是30天后
# 使用 assertIs() 方法,发现 was_published_recently() 返回 True,而我们想要他返回 False
