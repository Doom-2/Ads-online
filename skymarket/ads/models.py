from django.core.validators import MinValueValidator, MinLengthValidator
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Ad(models.Model):
    title = models.CharField(max_length=200, validators=[MinLengthValidator(8)])
    price = models.IntegerField(validators=[MinValueValidator(0)])
    description = models.CharField(max_length=1000, null=True, blank=True)
    author = models.ForeignKey(User, related_name='ads', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='ad_images/', null=True, blank=True)

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @property
    def author_first_name(self):
        return self.author.first_name

    @property
    def author_last_name(self):
        return self.author.last_name

    @property
    def phone(self):
        return str(self.author.phone)


class Comment(models.Model):
    text = models.CharField(max_length=1000)
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["-created_at"]

    def __str__(self):
        return self.text

    @property
    def author_first_name(self):
        return self.author.first_name

    @property
    def author_last_name(self):
        return self.author.last_name

    @property
    def author_image(self):
        return self.author.image.url if self.author.image else None
