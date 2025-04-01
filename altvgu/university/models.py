from django.db import models
from django.urls import reverse
# Create your models here.

class PublishedModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(actual = News.Status.actual)

class Category(models.Model):
    name = models.CharField(max_length=100,
    db_index=True)
    slug = models.SlugField(max_length=255,
    unique=True, db_index=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)


class News(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Старая'
        actual = 1, 'Актуальная'

    tags = models.ManyToManyField(Tag, related_name='news')
    author = models.OneToOneField(Author, on_delete=models.CASCADE, null=True, blank=True)
    objects = models.Manager()
    category =  models.ForeignKey('Category', on_delete=models.CASCADE)
    published = PublishedModel()
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    actual =  models.BooleanField(choices=Status.choices, default=Status.DRAFT)
    slug = models.SlugField(unique=True, verbose_name="URL")

    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'post_slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"


