from django.db import models

class Video(models.Model):
    video_id = models.CharField(max_length=255, unique=True)  # Store unique video IDs
    title = models.CharField(max_length=255)  # Video title

    def __str__(self):
        return self.title

class Comment(models.Model):
    video = models.ForeignKey(Video, related_name="comments", on_delete=models.CASCADE)
    comment_id = models.CharField(max_length=255, unique=True)
    text = models.TextField()
    

    def __str__(self):
        return f"Comment by {self.text}"

class Reply(models.Model):
    comment = models.ForeignKey(Comment, related_name="replies", on_delete=models.CASCADE)
    reply_id = models.CharField(max_length=255, unique=True)
    author = models.CharField(max_length=255)
    text = models.TextField()

    def __str__(self):
        return f"Reply by {self.author} to comment {self.comment.comment_id}"
