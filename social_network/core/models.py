from django.db import models


class CreateModel(models.Model):
    """Абстрактная модель. Добавляет дату создания."""
    created = models.DateTimeField(
        'дата создания',
        auto_now_add=True
    )

    class Meta:
        """абстрактная модель"""
        abstract = True
