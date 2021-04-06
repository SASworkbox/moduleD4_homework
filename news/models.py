from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(
        'accounts.Author', on_delete=models.CASCADE, verbose_name="Автор")
    post_type = models.CharField(
        max_length=1,
        choices=[
            ('A', 'Article'),
            ('N', 'News')
        ],
        default='N'
    )
    posted = models.DateTimeField(
        auto_now_add=True, verbose_name="Опубликованно")
    category = models.ManyToManyField(
        Category, through='PostCategory', verbose_name="Категория")
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Контент")
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.title} ({self.posted.ctime()})'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        if len(self.content) < 124:
            return self.content
        # Without word breaking if possible
        return self.content[:124].rsplit(' ', 1)[0] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    text = models.TextField()
    posted = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.text

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
