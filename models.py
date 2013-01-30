# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class RestoreActions(models.Model):
    id = models.IntegerField(primary_key=True)
    version_store_id = models.IntegerField(null=True, blank=True)
    dt_created = models.DateTimeField()
    dt_start = models.DateTimeField(null=True, blank=True)
    dt_finish = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'restore_actions'

class TreeStore(models.Model):
    id = models.IntegerField(primary_key=True)
    fullpath = models.CharField(max_length=12288)
    file_is = models.IntegerField()
    size = models.IntegerField(null=True, blank=True)
    mtime = models.CharField(max_length=90, blank=True)
    dt_created = models.DateTimeField(null=True, blank=True)
    dt_modified = models.DateTimeField(null=True, blank=True)
    dt_deleted = models.DateTimeField(null=True, blank=True)
    checked = models.IntegerField()
    level = models.IntegerField()
    class Meta:
        db_table = u'tree_store'

class VersionStore(models.Model):
    id = models.IntegerField(primary_key=True)
    tree_store_id = models.IntegerField(null=True, blank=True)
    filepath = models.CharField(max_length=3000, blank=True)
    filename = models.CharField(max_length=900, blank=True)
    dt_created = models.DateTimeField()
    class Meta:
        db_table = u'version_store'

