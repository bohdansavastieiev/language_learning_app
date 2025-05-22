import uuid

from django.db import models
from django.conf import settings


class AbstractBaseModel(models.Model):
    """
    An abstract base model with created_at and updated_at fields.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Language(AbstractBaseModel):
    """
    Represents a language (e.g., English, Spanish).
    """
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    is_active = models.BooleanField(default=True, help_text="Is this language available for selection?")

    def __str__(self):
        return self.name


class UserProfile(AbstractBaseModel):
    """
    Stores additional profile information for a user.
    Linked one-to-one with Django's built-in User model.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    native_language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='native_profiles')
    def __str__(self):
        return f"Profile of {self.user.username}"


class Dictionary(AbstractBaseModel):
    """
    Represents a collection of words, belonging to a user and a specific language.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='dictionaries')
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='dictionaries')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ('user', 'language', 'name')
        verbose_name_plural = "Dictionaries"

    def __str__(self):
        return f"{self.name} ({self.language.code}) for {self.user.username}"


class Word(AbstractBaseModel):
    """
    Represents a word entry within a dictionary.
    """
    dictionary = models.ForeignKey(Dictionary, on_delete=models.CASCADE, related_name='words')
    text = models.CharField(max_length=255)
    translation = models.CharField(max_length=255)
    example_sentence = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('dictionary', 'text')

    def __str__(self):
        return f"{self.text} ({self.dictionary.language.code})"
