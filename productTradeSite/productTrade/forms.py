from django.forms import ModelForm
from django import forms
from productTrade.models import Member, Content, Comment
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, AuthenticationForm
from django.contrib.auth import get_user_model

from django.contrib.auth.hashers import check_password
        
class ContentForm(ModelForm):
    class Meta:
        model = Content
        fields = ["writer_id", "title", "text", "image"]
        labels = {
            "title": _('제목'),
            "text": _('내용'),
            "image": _('사진'),
            
        }
        help_texts = {
            "title": _('제목을 입력하세요.'),
            "text": _('내용을 입력하세요.'),
            "image": _('사진을 업로드하세요.'),
        }
        widgets = {
            'writer_id': forms.HiddenInput(),
        }
        
        
class RegisterForm(UserCreationForm):
    class Meta:
        model = Member
        fields = ["name", "mobile", "username", "password1", "password2"]
        labels = {
            "name": _('이름'),
            "mobile": _('전화번호'),
            "username": _('아이디'),
            "password1": _('비밀번호'),
            "password2": _('비밀번호 확인'),
        }
        help_texts = {
            "name": _('이름을 입력해주세요.'),
            "mobile": _('전화번호를 입력해주세요. ex)010-1234-5678'),
            "username": _('아이디를 15자 이내로 입력해주세요.'),
            "password1": _('비밀번호를 20자 이내로 입력해주세요.'),
            "password2": _('비밀번호를 다시 입력해주세요.'),
        }
        widgets = {
        }
        error_messages = {
            "name" : {
                "max_length": _('이름이 너무 깁니다. 30자 이하로 해주세요.')
            },
            "password1" : {
                "max_length": _('비밀번호가 너무 깁니다. 20자 이하로 해주세요.')
            },
            "mobile" : {
                "max_length": _('전화번호를 제대로 입력해주세요.')
            },
        }
       
    
    
class LoginForm(AuthenticationForm):
    class Meta:
        model = Member
        fields = ["username", "password"]
        
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        for fieldname in ['username']:
            self.fields[fieldname].label = '아이디'
        for fieldname in ['password']:
            self.fields[fieldname].label = '비밀번호'
            

class UserUpdateForm(UserChangeForm):
    password = None
    
    class Meta:
        model = get_user_model()
        fields = ["name", "mobile"]
        
        
class PasswordUpdateForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(PasswordUpdateForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].label = '기존 비밀번호'
        self.fields['old_password'].widget.attrs.update({
            'class': 'form-control',
            'autofocus': False,
        })
        self.fields['new_password1'].label = '새 비밀번호'
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['new_password2'].label = '새 비밀번호 확인'
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
        })
       
    
class CheckPasswordForm(forms.Form):
    password = forms.CharField(label='비밀번호', widget=forms.PasswordInput(
        attrs={'class': 'form-control',}), 
    )
    # 현재 접속중인 사용자의 password를 가져오기 위한 init
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
    
    # form에 입력된 password 값과 init으로 생성된 현재 사용자의 password 비교
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = self.user.password
        
        if password:
            if not check_password(password, confirm_password):
                self.add_error('password', '비밀번호가 일치하지 않습니다.')
        
             
class CommentForm(ModelForm):
        class Meta:
            model = Comment
            fields = ["content_id", "commenter_id", "text"]
            labels = {
                "text": _('댓글'),
            }
            help_texts = {


            }
            widgets = {
                'content_id': forms.HiddenInput(),
                'commenter_id': forms.HiddenInput(),
                'text': forms.TextInput(
                    attrs={
                        'class': 'comment-form-control',
                        'placeholder': '댓글을 입력하세요.'
                    }
                ),
            }
            error_messages = {
                "text" : {
                },
            }