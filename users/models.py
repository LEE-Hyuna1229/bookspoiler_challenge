from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


class User(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=255, unique=True)
    nickname = models.CharField(max_length=255, verbose_name='닉네임', unique=True)
    mbti = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255, verbose_name='휴대전화번호')
    profile_img = models.URLField(max_length=255)
    is_staff = models.BooleanField(default=False, verbose_name='운영진')
    is_paid = models.BooleanField(default=False, verbose_name='챌린지 도전 회원')
    is_down = models.BooleanField(default=False, verbose_name='휴면회원')
    is_active = models.BooleanField(default=True, verbose_name='활동회원')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='가입일자')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일자')
