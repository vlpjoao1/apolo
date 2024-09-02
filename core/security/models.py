from datetime import datetime

from crum import get_current_request
from django.db import models
from django.forms import model_to_dict

from core.security.choices import LOGIN_TYPE
from core.user.models import User


# Create your models here.
class AccessUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    time = models.TimeField(default=datetime.now)
    ip_address = models.CharField(max_length=50)
    type = models.CharField(max_length=20, choices=LOGIN_TYPE, default=LOGIN_TYPE[0][0])

    def __str__(self):
        return self.ip_address

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        try:
            request = get_current_request()
            self.ip_address = request.META['REMOTE_ADDR']
        except:
            pass
        super(AccessUser, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        item['type'] = {'id':self.type, 'name':self.get_type_display()}
        item['user'] = self.user.toJSON()
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['time'] = self.time.strftime('%H:%M:%S')
        return item

    class Meta:
        verbose_name = 'Access User'
        verbose_name_plural = 'Access Users'
        ordering = ['id']
        default_permissions = ()
        permissions = (
            ('view_access_user', 'can view access user'),
            ('delete_access_user', 'can delete access user'),
        )
