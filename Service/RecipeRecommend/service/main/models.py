# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Food(models.Model):
    data_source = models.CharField(max_length=10, blank=True, null=True)
    id = models.IntegerField(primary_key=True)
    food_name = models.CharField(max_length=1000, blank=True, null=True)
    food_img = models.CharField(max_length=1000, blank=True, null=True)
    recipe_link = models.CharField(max_length=1000, blank=True, null=True)
    serving = models.CharField(max_length=10, blank=True, null=True)
    category_high_level = models.CharField(max_length=20, blank=True, null=True)
    category_mid_level = models.CharField(max_length=20, blank=True, null=True)
    category_low_level = models.CharField(max_length=20, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    views = models.IntegerField(blank=True, null=True)
    likes = models.IntegerField(blank=True, null=True)
    reviews = models.IntegerField(blank=True, null=True)
    comments = models.IntegerField(blank=True, null=True)
    재료1 = models.CharField(max_length=50, blank=True, null=True)
    재료2 = models.CharField(max_length=50, blank=True, null=True)
    재료3 = models.CharField(max_length=50, blank=True, null=True)
    재료4 = models.CharField(max_length=50, blank=True, null=True)
    재료5 = models.CharField(max_length=50, blank=True, null=True)
    재료6 = models.CharField(max_length=50, blank=True, null=True)
    재료7 = models.CharField(max_length=50, blank=True, null=True)
    재료8 = models.CharField(max_length=50, blank=True, null=True)
    재료9 = models.CharField(max_length=50, blank=True, null=True)
    재료10 = models.CharField(max_length=50, blank=True, null=True)
    재료1_정량 = models.CharField(max_length=50, blank=True, null=True)
    재료2_정량 = models.CharField(max_length=50, blank=True, null=True)
    재료3_정량 = models.CharField(max_length=50, blank=True, null=True)
    재료4_정량 = models.CharField(max_length=50, blank=True, null=True)
    재료5_정량 = models.CharField(max_length=50, blank=True, null=True)
    재료6_정량 = models.CharField(max_length=50, blank=True, null=True)
    재료7_정량 = models.CharField(max_length=50, blank=True, null=True)
    재료8_정량 = models.CharField(max_length=50, blank=True, null=True)
    재료9_정량 = models.CharField(max_length=50, blank=True, null=True)
    재료10_정량 = models.CharField(max_length=50, blank=True, null=True)
    rating = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'food'
