from django.db import models
from django.contrib.auth.models import User


DB_TYPES = (
    ('psql', 'PostgreSQL'),
    ('mysql', 'MySQL'),
    ('mongo', 'MongoDB'),
)


class DB_details(models.Model):
    connection_name = models.CharField(max_length=100, blank=False, null=False)
    db_type = models.CharField(
        max_length=25, choices=DB_TYPES, blank=False, null=False)
    name = models.CharField(max_length=200, blank=False, null=False)
    address = models.CharField(max_length=500, blank=False, null=False)
    password = models.CharField(max_length=200, blank=False, null=False)
    username = models.CharField(max_length=200, blank=False, null=False)
    port = models.IntegerField(default=0)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=False, null=True)

    def __str__(self):
        return self.name
