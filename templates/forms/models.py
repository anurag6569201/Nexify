from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime

class Form(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title

class Question(models.Model):
    TEXT = 'TEXT'
    MULTIPLE_CHOICE = 'MC'
    SHORT_ANSWER = 'SA'
    LONG_ANSWER = 'LA'
    DROP_DOWN = 'DD'
    DATE_TIME = 'DT'

    QUESTION_TYPES = [
        (TEXT, 'Text'),
        (MULTIPLE_CHOICE, 'Multiple Choice'),
        (SHORT_ANSWER, 'Short Answer'),
        (LONG_ANSWER, 'Long Answer'),
        (DROP_DOWN, 'Dropdown'),
        (DATE_TIME, 'Date and Time'),
    ]

    form = models.ForeignKey(Form, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    question_type = models.CharField(choices=QUESTION_TYPES, max_length=20, default=TEXT)
    choices = models.TextField(blank=True, null=True)  # Store choices as comma-separated values

    def __str__(self):
        return self.text

    def get_choices(self):
        """Utility method to get choices as a list for multiple choice or dropdown questions."""
        if self.question_type in [self.MULTIPLE_CHOICE, self.DROP_DOWN] and self.choices:
            return self.choices.split(',')
        return []
    
class Response(models.Model):
    form = models.ForeignKey(Form, related_name='responses', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Response to {self.form.title} on {self.created_at}'

class Answer(models.Model):
    response = models.ForeignKey(Response, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    answer_text = models.TextField(blank=True, null=True)  # Store the answer as text, regardless of question type

    def __str__(self):
        return f'Answer to {self.question.text}'

    def clean(self):
        """Custom validation to ensure answer matches question type."""
        if self.question.question_type in [Question.MULTIPLE_CHOICE, Question.DROP_DOWN]:
            if self.answer_text not in self.question.get_choices():
                raise ValidationError(f"Invalid choice for {self.question.question_type} question.")
        elif self.question.question_type == Question.DATE_TIME:
            try:
                datetime.strptime(self.answer_text, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                raise ValidationError("Invalid date and time format. Use 'YYYY-MM-DD HH:MM:SS' format.")
