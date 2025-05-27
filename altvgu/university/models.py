from django.db import models
from django.urls import reverse
from django.utils.text import slugify
# Create your models here.


def translit_to_eng(s: str) -> str:
    d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д':
        'd',
         'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и':
             'i', 'к': 'k',
         'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п':
             'p', 'р': 'r',
         'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х':
             'h', 'ц': 'c', 'ч': 'ch',
         'ш': 'sh', 'щ': 'shch', 'ь': '', 'ы': 'y',
         'ъ': '', 'э': 'r', 'ю': 'yu', 'я': 'ya'}

    return "".join(map(lambda x: d[x] if d.get(x,False) else x, s.lower()))


class PublishedModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(actual = News.Status.actual)

class Category(models.Model):
    name = models.CharField(max_length=100,
    db_index=True,verbose_name='Название' )
    slug = models.SlugField(max_length=255,
    unique=True, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    def __str__(self):
        return self.bio

class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads_model')


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class News(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Старая'
        actual = 1, 'Актуальная'

    tags = models.ManyToManyField(Tag, related_name='news')
    author = models.OneToOneField(Author, on_delete=models.CASCADE, null=True, blank=True)
    objects = models.Manager()
    category =  models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name="Категория")
    published = PublishedModel()
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    #actual =  models.BooleanField(choices=Status.choices, default=Status.DRAFT, verbose_name="Актуальность")
    #actual = models.IntegerField(choices=Status.choices, default=Status.DRAFT, verbose_name="Актуальность")
    actual = models.BooleanField(
        choices=[(False, 'Старая'), (True, 'Актуальная')],
        default=False,
        verbose_name="Актуальность"
    )
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/",default=None, blank=True, null=True,verbose_name="Фото")
    slug = models.SlugField(unique=True, verbose_name="URL", allow_unicode=True)

    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'post_slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        permissions = [
            ("can_publish", "Может публиковать новости"),
            ("can_edit", "Может редактировать новости")
        ]

    def save(self, *args, **kwargs):
        translit_title = translit_to_eng(self.title)
        self.slug = slugify(translit_title)
        super().save(*args, **kwargs)

    class Visibility(models.IntegerChoices):
        PUBLIC = 1, 'Видна всем'
        AUTHENTICATED = 2, 'Только авторизованным'
        PRIVATE = 3, 'Только авторам и администраторам'

    visibility = models.IntegerField(
        choices=Visibility.choices,
        default=Visibility.PUBLIC,
        verbose_name='Видимость'
    )
