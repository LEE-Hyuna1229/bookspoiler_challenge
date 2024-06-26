from django.db import models
from users.models import User
from books.models import Book

# Create your models here.
class ChallengeInfo(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True) # 자동으로 생성되었는지 여부
    updated_at = models.DateTimeField(auto_now=True)

class ChallengeSpoiler(models.Model):
    challenge_info = models.ForeignKey(ChallengeInfo, on_delete=models.CASCADE)
    day = models.IntegerField() 
    title = models.CharField(max_length=225)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DoItComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challengespoiler_info = models.ForeignKey(ChallengeSpoiler, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)