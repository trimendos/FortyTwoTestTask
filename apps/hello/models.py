from PIL import Image

from django.db import models


class Profile(models.Model):
    """Stores an instance of the Profile model"""
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birthday = models.DateField()
    email = models.EmailField()
    jabber = models.EmailField()
    skype = models.CharField(max_length=50)
    biography = models.TextField(blank=True)
    contacts = models.TextField(blank=True)
    photo = models.ImageField(
        upload_to='photos', null=True, blank=True, verbose_name=u'Photo')

    def __unicode__(self):
        return u'{last_name} {first_name}'.format(first_name=self.first_name,
                                                  last_name=self.last_name)

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        size = (200, 200)
        if self.photo and (self.photo.width > 200 or self.photo.height > 200):
            filename = self.photo.path
            image = Image.open(filename)
            image.thumbnail(size, Image.ANTIALIAS)
            image.save(filename)


class Request(models.Model):
    """Stores an instance of the http request"""
    datetime = models.DateTimeField(auto_now_add=True)
    url = models.CharField(max_length=150)
    status_code = models.IntegerField(max_length=3)
    method = models.CharField(max_length=10)
    viewed = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)

    class Meta:
        ordering = ['-datetime']

    def __unicode__(self):
        return u'{datetime} {url}'.format(datetime=self.datetime, url=self.url)

    @staticmethod
    def get_unviewed_count():
        """Returns count of unviewed requests"""
        return Request.objects.filter(viewed=False).count()

    @staticmethod
    def update_priority(id, priority):
        """Updates given item with new priority"""
        rq = Request.objects.get(pk=id)
        rq.priority = priority
        rq.save()


class CRUDLog(models.Model):
    action = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    app = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '{0.timestamp}: {0.action} {0.model} from {0.app}'.format(self)
