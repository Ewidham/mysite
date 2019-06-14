import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length = 200)
    pub_date = models.DateTimeField('date published')
    nr_of_votes = models.IntegerField(default = 1)

    def choice_ordered_by_votes(self):
        return sorted(self.choice_set.all(), key=lambda a: -a.vote_count)

    def __str__(self):
        return self.question_text
    
    def was_published_recently(self):
        now = timezone.now()
        return (now - datetime.timedelta(days=1) <= self.pub_date <= now)

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = "Published recently?"

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length = 200)
    added = models.DateTimeField("date added", default=timezone.now())

    def _get_vote_count(self):
        return self.vote_set.all().count()
    vote_count = property(_get_vote_count)

    class Meta:
        ordering = ['-choice_text']

    def __str__(self):
        return self.choice_text

class Vote(models.Model):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    voter = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        #return "{} - {}".format(unicode(self.voter.username), unicode(self.choice.choice_text))
        return self.voter.username + " - " + self.choice.choice_text