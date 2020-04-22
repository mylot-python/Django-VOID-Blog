from django import forms

from .models import Comments


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        exclude = ['is_delete', 'create_time', 'update_time']
        error_messages = {
            'author': {
                'max_length': '亲, 名字长度不能超过10位数哦',
                'required': '亲, 名字不能为空哦',
            },
            'content': {
                'required': '亲, 内容不能为空哦'
            },
            'mail': {
                'required': '亲, 邮箱不能为空哦'
            }
        }