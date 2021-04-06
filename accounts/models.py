from django.db import models
from django.apps import apps


class Author(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    def update_rating(self):
        Post = apps.get_model('news.Post')
        Comment = apps.get_model('news.Comment')

        new_rating = 0

        # Author's posts
        for post in Post.objects.filter(author=self):
            new_rating += post.rating
        new_rating *= 3

        # Author's comments
        for comment in Comment.objects.filter(user=self.user):
            new_rating += comment.rating

        # Comments to author's posts (except his own)
        for post in Post.objects.filter(author=self):
            for comment in Comment.objects.filter(post=post):
                if comment.user != self.user:
                    new_rating += comment.rating

        self.rating = new_rating
        self.save()
