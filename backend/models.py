from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


DB_TYPES = (
    ('psql', 'PostgreSQL'),
    ('mysql', 'MySQL'),
    ('mongo', 'MongoDB'),
)


class DB_details(models.Model):
    connection_name = models.CharField(max_length=100, blank=False, null=False,
                                       unique=True)
    db_type = models.CharField(max_length=25, choices=DB_TYPES, blank=False,
                               null=False)
    name = models.CharField(max_length=200, blank=False, null=False)
    address = models.CharField(max_length=500, blank=False, null=False)
    password = models.CharField(max_length=200, blank=False, null=False)
    username = models.CharField(max_length=200, blank=False, null=False)
    port = models.IntegerField(default=0)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=False, null=True)

    def __str__(self):
        return self.name


class Charts(models.Model):
    database_id = models.ForeignKey(DB_details, on_delete=models.CASCADE,
                                    related_name="db_details")
    connection_name = models.CharField(max_length=100, blank=False, null=False,
                                       unique=True)
    table_name = models.CharField(max_length=100, blank=False, null=False)
    column_name = models.CharField(max_length=100, blank=False, null=False)

    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.table_name+"_"+self.column_name+"_"+str(self.database_id))

        super(Charts, self).save(*args, **kwargs)

    def __str__(self):
        return self.slug

