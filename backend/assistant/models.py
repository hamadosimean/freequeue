from django.db import models
from django.contrib.auth import get_user_model
import uuid
from general_settings.utils import TimeStampedModel
# Create your models here.

User = get_user_model()


# --------------------------------
# Question model
# --------------------------------
class Question(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField()

    def __str__(self):
        return self.question


# --------------------------------
# Answer model
# --------------------------------
class Answer(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()

    def __str__(self):
        return self.answer
