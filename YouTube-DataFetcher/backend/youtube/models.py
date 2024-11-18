from django.db import models


class Video(models.Model):
    video_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    published_date = models.DateTimeField()
    view_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title} ({self.video_id})"


class Comment(models.Model):
    video = models.ForeignKey(
        Video,
        on_delete=models.CASCADE,
        related_name="comments"  
    )
    comment_id = models.CharField(max_length=50, unique=True)
    text = models.TextField()
    author_name = models.CharField(max_length=255)
    published_date = models.DateTimeField()
    like_count = models.IntegerField(default=0)  

    def __str__(self):
        return f"Comment by {self.author_name} on {self.video.title}"


class Reply(models.Model):
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name="replies"  
    )
    reply_id = models.CharField(max_length=255, unique=True)
    author = models.CharField(max_length=255)
    text = models.TextField()
    published_date = models.DateTimeField()
    like_count = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return f"Reply by {self.author} on comment ID {self.comment.comment_id}"
