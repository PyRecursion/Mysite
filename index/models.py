from django.db import models

# Create your models here.


class Story(models.Model):
    name=models.CharField(max_length=20,)
    author=models.CharField(max_length=20,null=True)
    last_time=models.CharField(max_length=20,null=True)

    def __repr__(self):
        return self.name
    __str__=__repr__

    class Meta:
        db_table="story"



class Story_text(models.Model):
    story_dirname=models.CharField(max_length=50)
    content_path=models.CharField(max_length=50,null=True)
    story=models.ForeignKey(Story)

    def __repr__(self):
        return self.story_dirname
    __str__=__repr__

    class Meta:
        db_table="story_text"



class ImageType(models.Model):
    type=models.CharField(max_length=20)

    def __repr__(self):
        return self.type

    __str__ = __repr__

    class Meta:
        db_table = "imagetype"



class Images(models.Model):
    link=models.CharField(max_length=20)
    type=models.ForeignKey(ImageType)
    def __repr__(self):
        return self.link
    __str__ = __repr__

    class Meta:
        db_table = "images"


class User(models.Model):
    loginname=models.CharField(max_length=20)
    name=models.CharField(max_length=20)
    password=models.CharField(max_length=30)

    def __repr__(self):
        return self.loginname
    __str__ = __repr__

    class Meta:
        db_table = "user"


class Music(models.Model):
    songname=models.CharField(max_length=20)
    singer=models.CharField(max_length=20)
    link=models.CharField(max_length=200)
    def __repr__(self):
        return self.songname
    __str__ = __repr__

    class Meta:
        db_table = "music"


class Music_like(models.Model):
    user=models.ForeignKey(User)
    music=models.ForeignKey(Music)

    class Meta:
        db_table = "music_like"


class Story_history(models.Model):
    click_time=models.DateTimeField()
    story_historylink=models.CharField(max_length=100)
    user=models.ForeignKey(Music)

    class Meta:
        db_table = "story_history"


class Topic(models.Model):
    title=models.CharField(max_length=50)
    content=models.TextField()
    publishtime=models.DateTimeField()
    user=models.ForeignKey(User)

    class Meta:
        db_table = "topic"


class UserImages(models.Model):
    images = models.ImageField(upload_to="static/upload/", null=True)
    topic=models.ForeignKey(Topic)

    class Meta:
        db_table="userImages"

class Comment(models.Model):
    comment_text=models.TextField()
    comment_time = models.DateTimeField()
    topic=models.ForeignKey(Topic)
    comment_userid=models.ForeignKey(User,db_column="comment_userid")

    class Meta:
        db_table="comment"

class Reply(models.Model):
    comment=models.ForeignKey(Comment) #恢复属于哪条评论
    reply_type=models.BooleanField() #回复属于回复主题(reply_id=commit_id)还是其他人的回复
    reply_id=models.IntegerField() #回复的评论的ID或回复的ID
    reply_content=models.CharField(max_length=255) #回复内容
    from_uid=models.ForeignKey(User,db_column="form_uid")  #写这条回复的用户
    to_uid=models.IntegerField() #回复对象
    reply_datetime=models.DateTimeField()

    class Meta:
        db_table="reply"


