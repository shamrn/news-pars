from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=200)


class News(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    created = models.DateTimeField()
    title = models.CharField(max_length=200)
    short_desc = models.TextField()
    desc = models.TextField()
    img = models.ImageField(upload_to=f'img/')

    class Meta:
        ordering = ('-created',)