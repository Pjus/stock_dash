from django.db import models
from django import forms
from django.contrib.auth.models import User

from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
    
class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    subject = models.CharField(max_length=200)
    content = RichTextUploadingField(
                                        blank=True, 
                                        null=True,
                                        external_plugin_resources=[(
                                            'youtube',
                                            '/static/vendor/ckeditor_plugins/youtube/youtube/',
                                            'plugin.js',
                                        )]

                                    )
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_question', default=None, blank=True)  # 추천인 추가
    hide = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.subject


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_answer')


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question  # 사용할 모델
        fields = ['subject', 'content']  # QuestionForm에서 사용할 Question 모델의 속성



