from django.db import models
from django.utils import timezone
import datetime

# Create your models here.


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    author = models.CharField(max_length=30)

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        # returns false if the question was published in the future(that is not possible)
        return timezone.now() >= self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Comments(models.Model):
    com_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=350)
    comment_author = models.CharField(max_length=30)
    pub_date = models.DateTimeField('date published')


def __str__(self):
    return self.comment_text
