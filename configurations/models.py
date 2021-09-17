"""
ConfigurationMasterModels
"""
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.

from helper.models import CreateUpdateByAbstractModel, DateAbstractModel, StatusAbstractModel


class CurrencyMaster(DateAbstractModel,
                     CreateUpdateByAbstractModel,
                     StatusAbstractModel):
    """
    CurrencyMaster MODEL table
    """
    currency = models.CharField(max_length=30, unique=True)
    symbol = models.CharField(max_length=30)
    code_iso = models.CharField(
        max_length=30,
        verbose_name='Code ISO',
        null=True, blank=True)
    hex_symbol = models.CharField(max_length=30,
                                  verbose_name='Hex Symbol',
                                  null=True,
                                  blank=True)

    class Meta:
        verbose_name = "Currency Master"
        verbose_name_plural = "Currency Master"
        db_table = 'currency_master'

    def __str__(self):
        return self.currency


class CountryMaster(DateAbstractModel,
                    CreateUpdateByAbstractModel,
                    StatusAbstractModel):
    """
    country master table
    """
    country = models.CharField(max_length=50, unique=True, db_index=True)
    isd = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(99999),
            MinValueValidator(1)
        ],
        verbose_name='ISD/Country Code',
        null=True, blank=True)
    mobile_no_digits = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(15),
            MinValueValidator(5)
        ],
        verbose_name='Countries Mobile Number digit')
    currency = models.ForeignKey(CurrencyMaster,
                                 on_delete=models.CASCADE,
                                 related_name='country_master_currency',
                                 verbose_name='Currency',
                                 limit_choices_to={'is_active': '1'},
                                 null=True, blank=True)
    code = models.CharField(
        max_length=10,
        null=True, blank=True,
        verbose_name='ISO Code')
    timezone = models.CharField(
        max_length=100,
        help_text='Please add correct country timezone.')

    class Meta:
        verbose_name = "  Country Master"
        verbose_name_plural = "  Country Master"
        db_table = "country_master"

    def __str__(self):
        return self.country


class StateMaster(DateAbstractModel,
                  CreateUpdateByAbstractModel,
                  StatusAbstractModel):
    """
    all states master table
    """
    state = models.CharField(max_length=50, db_index=True)
    country = models.ForeignKey(CountryMaster,
                                on_delete=models.CASCADE,
                                db_column='country',
                                limit_choices_to={'is_active': '1'})

    class Meta:
        verbose_name = " State Master"
        verbose_name_plural = " State Master"
        unique_together = ('country', 'state')
        db_table = "state_master"

    def __str__(self):
        return self.state


class CityMaster(DateAbstractModel,
                 CreateUpdateByAbstractModel,
                 StatusAbstractModel):
    """
    All city master tables
    """
    city = models.CharField(max_length=50, db_index=True)
    state = models.ForeignKey(StateMaster,
                              on_delete=models.CASCADE,
                              db_column='state',
                              limit_choices_to={'is_active': '1'})

    class Meta:
        verbose_name = "City Master"
        verbose_name_plural = "City Master"
        unique_together = ('state', 'city')
        db_table = "city_master"

    def __str__(self):
        return self.city


class PaymentCommissionRule(DateAbstractModel,
                            CreateUpdateByAbstractModel,
                            StatusAbstractModel):
    """
    All CommissionConfiguration
    """
    is_country_applicable = models.BooleanField(default=False)
    country = models.ForeignKey(CountryMaster,
                                on_delete=models.CASCADE,
                                db_column='country',
                                limit_choices_to={'is_active': '1'},
                                null=True, blank=True)
    commission_value = models.FloatField()

    class Meta:
        verbose_name = "Payment Commission Rule"
        verbose_name_plural = "Payment Commission Rule"
        db_table = "payment_commission_rule"

    def __str__(self):
        return self.commission_value
