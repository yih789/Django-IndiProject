from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Member(AbstractUser):
    username = models.CharField(max_length=15, primary_key=True) # 기본키 # 사용자 ID
    name = models.CharField(max_length=30) # 사용자 이름
    mobile = models.CharField(max_length=15)  # 전화 번호: unique
    updated_at = models.DateTimeField(auto_now=True)

    # 총 필드
    # ['username', 'name', 'mobile', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'updated_at', 'email', 'first_name', 'last_name', 'password']
    #list_display = ('username', 'name', 'mobile')
    class Meta:
        unique_together = (('username', 'mobile'),)


class DropoutMember(models.Model):
    user_id = models.CharField(max_length=15) # 아이디
    name = models.CharField(max_length=30) # 사용자 이름
    mobile = models.CharField(max_length=15) # 휴대전화

    joined_at = models.DateTimeField() # 회원가입일
    dropouted_at = models.DateTimeField(auto_now_add=True) # 탈퇴일


class Content(models.Model):     
    writer_id = models.ForeignKey(Member, null=True, on_delete=models.SET_NULL) # 외래키
    title = models.CharField(max_length=50)
    text = models.TextField()
    
    image = models.ImageField(upload_to='productTrade/contentImages/', null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
  
    
class Comment(models.Model):
    content_id = models.ForeignKey(Content, on_delete=models.CASCADE) # 외래키
    commenter_id = models.ForeignKey(Member, null=True, on_delete=models.SET_NULL) # 외래키
    
    
    text = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
