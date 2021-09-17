"""CoreLevelExtract table
"""

# auth user model tables
from django.contrib.auth.models import User

from django.db import models

# Create your models here.

from smart_selects.db_fields import ChainedForeignKey


class CreateUpdateByAbstractModel(models.Model):
    """
    creation updation by abstract model
    """
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='created_%(class)ss',
        verbose_name='Created By',
        limit_choices_to=~models.Q(is_staff=0, is_superuser=0),
        db_column='created_by')
    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='updated_%(class)ss',
        verbose_name='Updated By',
        limit_choices_to=~models.Q(is_staff=0, is_superuser=0),
        db_column='updated_by',
        null=True)

    class Meta:
        """
        class container with some options attached to the model
        """
        abstract = True


class LocationMaster(models.Model):
    """
    location master abstract model
    """
    country = models.ForeignKey(
        'configurations.CountryMaster',
        related_name='country_%(class)ss',
        on_delete=models.CASCADE, limit_choices_to={'is_active': '1'},
        db_column='country', null=True, blank=True)
    state = ChainedForeignKey(
        'configurations.StateMaster', chained_field="country",
        chained_model_field="country", limit_choices_to={'is_active': '1'},
        related_name='state_%(class)ss', on_delete=models.CASCADE,
        show_all=True, auto_choose=True, sort=True,
        db_column='state', null=True, blank=True)
    city = ChainedForeignKey(
        'configurations.CityMaster', chained_field='state',
        chained_model_field='state', limit_choices_to={'is_active': '1'},
        related_name='city_%(class)ss', on_delete=models.CASCADE,
        show_all=True, auto_choose=True, sort=True,
        db_column='city', null=True, blank=True)

    class Meta:
        abstract = True


class DateAbstractModel(models.Model):
    """
    DateAbstractModel
    date model
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        class container with some options attached to the model
        """
        abstract = True


class StatusAbstractModel(models.Model):
    """
    status abstract model
    """
    is_active = models.BooleanField(default=True)

    class Meta:
        """
        class container with some options attached to the model
        """
        abstract = True
