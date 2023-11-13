from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class Post(models.Model):
    author = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100)
    content = RichTextUploadingField()
    head_image = models.ImageField(
        upload_to='blog/images/%Y/%m/%d/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    view_count = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(
        'Category', null=True, on_delete=models.SET_NULL, related_name='posts')
    tags = models.ManyToManyField('Tag', blank=True)
    like = models.ManyToManyField(
        'accounts.User', related_name='post_likes', blank=True)

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return f'[{self.pk}] {self.title} :: {self.author}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'

    def get_file_name(self):
        return self.file_upload.name.split('/')[-1]

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]


class Category(models.Model):
    name = models.CharField(max_length=25, unique=True)
    slug = models.SlugField(max_length=200, db_index=True,
                            unique=True, allow_unicode=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/category/{self.slug}/'


class Tag(models.Model):
    name = models.CharField(max_length=25, unique=True)
    slug = models.SlugField(max_length=200, db_index=True,
                            unique=True, allow_unicode=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}/'


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    like = models.ManyToManyField(
        'accounts.User', related_name='comment_likes', blank=True)

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return f'[{self.post}] {self.content} :: {self.author}'

    def get_absolute_url(self):
        return f'/blog/{self.post.pk}/#comment-{self.pk}'
