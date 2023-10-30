from django.db import models


class Post(models.Model):
    author = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100)
    content = models.TextField()
    head_image = models.ImageField(
        upload_to='blog/images/%Y/%m/%d/', blank=True)
    # pictures 이미지 리스트로 변경? 게시글에 이미지 여러개 올리는거로
    file_upload = models.FileField(
        upload_to='blog/files/%Y/%m/%d/', blank=True)
    # 파일 업로드 냅둘지 말지??
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    view_count = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL, related_name='posts')
    tags = models.ManyToManyField('Tag', blank=True)
    # like_users 게시글 좋아요 누른사람 manytomany

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
    description = models.TextField()
    is_public = models.BooleanField(default=True)  # 이게 필요한가??
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/category/{self.slug}/'

    class Meta:
        verbose_name_plural = 'Categories'


class Tag(models.Model):
    name = models.CharField(max_length=25, unique=True)
    slug = models.SlugField(max_length=200, db_index=True,
                            unique=True, allow_unicode=True)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

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
    # like_users 댓글 좋아요 누른사람 manytomany, parent_comment_id 대댓글 셀프일대다

    def __str__(self):
        return f'[{self.post}] {self.content} :: {self.author}'

    def get_absolute_url(self):
        return f'/blog/{self.post.pk}/#comment-{self.pk}'

    class Meta:
        ordering = ['id']
