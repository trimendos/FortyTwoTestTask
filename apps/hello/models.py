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

    def __unicode__(self):
        return u'{last_name} {first_name}'.format(first_name=self.first_name,
                                                  last_name=self.last_name)


class Request(models.Model):
    pass
