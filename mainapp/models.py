# Create your models here.
from django.db import models

class News(models.Model):
    title = models.CharField(max_length=256, verbose_name='Title_verbose')
    preambule = models.CharField(max_length=1024, verbose_name='Preambule_verbose')
    body = models.TextField(blank=True, null=True, verbose_name='Body_verbose')
    body_as_markdown = models.BooleanField(default=False, verbose_name='As markdown verbose')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Created verbose', editable=False)
    updated = models.DateTimeField(auto_now=True, verbose_name='Update_verbose', editable=False)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.pk}  {self.title}'

    def delete(self, *args):
        self.deleted = True
        self.save()
#


