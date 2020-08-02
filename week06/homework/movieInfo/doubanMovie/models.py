# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class TFilmReview(models.Model):
    comment = models.CharField(max_length=2000, blank=True, null=True)
    star = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_film_review'


class TMovieInfo(models.Model):
    movie_title = models.CharField(max_length=64, blank=True, null=True)
    movie_datetime = models.CharField(max_length=32, blank=True, null=True)
    movie_type_name = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_movie_info'


class TPositionInfo(models.Model):
    pos_name = models.CharField(max_length=32, blank=True, null=True)
    area = models.CharField(max_length=32, blank=True, null=True)
    salary = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_position_info'
