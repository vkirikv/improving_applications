from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Status(models.Model):
    title = models.CharField(max_length=50, verbose_name='Name')

    class Meta:
        verbose_name_plural = 'Status'

    def __str__(self):
        return self.title


class App(models.Model):
    title = models.CharField(max_length=50, verbose_name='App Name')
    slug = models.SlugField(unique=True, verbose_name='Relative Address')
    owner = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='owner%(app_label)s_%(class)s_related',
        verbose_name='Owner'
    )
    developer = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='developer%(app_label)s_%(class)s_related',
        verbose_name='Developer',
    )

    class Meta:
        verbose_name_plural = 'App Names'

    def __str__(self):
        return self.title


class Suggestion(models.Model):
    title = models.CharField(max_length=50, verbose_name='Suggestion Name')
    author = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='%(app_label)s_%(class)s_related',
        verbose_name='Author',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Publish Date',
    )
    app = models.ForeignKey(
        App,
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s_related',
        verbose_name='App',
    )
    description = models.TextField(verbose_name='Description')
    status = models.ManyToManyField(
        Status,
        blank=False,
        related_name='%(app_label)s_%(class)s_related',
    )
    image = models.ImageField(
        'Image',
        upload_to='suggestion/',
        blank=True,
    )

    class Meta:
        verbose_name_plural = 'Suggestion Names'

    def __str__(self):
        return self.title


class Decision(models.Model):
    author = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='%(app_label)s_%(class)s_related',
        verbose_name='Author',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Publish Date',
    )
    suggestion = models.ForeignKey(
        Suggestion,
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s_related',
    )
    note = models.TextField(verbose_name='Decision')


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='%(app_label)s_%(class)s_related',
        verbose_name='Author',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Publish Date',
    )
    suggestion = models.ForeignKey(
        Suggestion,
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s_related',
    )
    note = models.TextField(verbose_name='Comment')
