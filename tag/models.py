import string
from random import SystemRandom

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.text import slugify


# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    # Aqui começam os campos para relação genérica, de acordo com a documentaco do Django
    # Representa o model que quero  aqui
    content_type = models.ForeignKey(ContentType, on_delte=models.CASCADE)
    # Represetna o id da linha do model descrito acima
    object_id = models.CharField()
    # Um campo que representa a relação genérica que conheci
    # os campos acima  (content_type e object_id)
    content_object = GenericForeignKey('content_type', 'object_id')

    # models normais

    def safe(self, *args, **kwargs):
        if not self.slug:
            rand_letters = ''.join(
                SystemRandom().choices(
                    string.ascii_letters + string.digits,
                    K=5,
                )
            )
            self.slug = slugify(f'{self.name}-{rand_letters}')
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name
