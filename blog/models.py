from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    post_date = models.DateTimeField(default=timezone.now)
    post_update = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

#python manage.py makemigration
# python manage.py sqlmigrate blog 0001
# python manage.py migrate
# python manage.py creatsuperuser
#  motdepasse : admin_123456

    def __str__(self):
      return self.title

    def get_absolute_url(self):
        #return '/detail/{}'.format(self.pk)
        return reverse('detail', args=[self.pk])


    class Meta :
        ordering = ('-post_date',)



class Comment(models.Model):
    name = models.CharField(max_length=50 , verbose_name='le nom')
    email = models.EmailField(verbose_name='email')
    body = models.TextField( verbose_name='comment')
    coment_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    post =models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    def __str__(self):
      return '{} à commenté sur la {}.'.format(self.name, self.post)

    class Meta:
        # from newest to oldest
       ordering = ('-coment_date',)

