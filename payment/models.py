from django.db import models

# auth user model tables
from django.contrib.auth.models import User

from helper.constants import PAYMENT_STATUS

from configurations.models import PaymentCommissionRule

# Create your models here.
from helper.models import DateAbstractModel, StatusAbstractModel
from user_tracker.models import ChatTracking, VideoTracking


class PaymentType(DateAbstractModel, StatusAbstractModel):
    """
    PaymentType
    """
    payment_type = models.CharField(max_length=50)

    class Meta:
        verbose_name = "    Payment Type"
        verbose_name_plural = "    Payment Type"
        db_table = 'payment_type'

    def __str__(self):
        return self.payment_type


class UserPaymentTransaction(models.Model):
    """
    UserPaymentTransaction
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='payment_transaction_user')
    video_call_tracking = models.ForeignKey(
        VideoTracking,
        on_delete=models.CASCADE,
        related_name='payment_transaction_video_track')
    chat_tracking = models.ForeignKey(
        ChatTracking,
        on_delete=models.CASCADE,
        related_name='payment_transaction_chat_track')
    invoice_no = models.CharField(max_length=100)
    payment_datetime = models.DateTimeField(
        auto_now_add=True, verbose_name='Payment Datetime')
    payment_type = models.ForeignKey(PaymentType, verbose_name='Payment Type',
                                     on_delete=models.CASCADE)
    invoice_amount = models.FloatField(verbose_name='Invoice Amount (in $)')
    currency = models.ForeignKey('configurations.CurrencyMaster', on_delete=models.CASCADE,
                                 null=True, blank=True)
    payment_status = models.CharField(max_length=100, choices=PAYMENT_STATUS)
    transaction_id = models.CharField(max_length=255, null=True,
                                      verbose_name='Payment Transaction ID')

    class Meta:
        verbose_name = "User Payment Transaction"
        verbose_name_plural = "User Payment Transaction"
        db_table = 'user_payment_type'

    def __str__(self):
        return self.invoice_no


class PaymentTransactionAfterCommission(models.Model):
    """
    PaymentTransactionAfterCommission
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='commission_payment_transaction_user')
    payment_commission_rule = models.ForeignKey(
        PaymentCommissionRule, on_delete=models.CASCADE,
        related_name='commission_rule_instance')
    payment_datetime = models.DateTimeField(
        auto_now_add=True, verbose_name='Payment Datetime')
    payment_type = models.ForeignKey(PaymentType, verbose_name='Payment Type',
                                     on_delete=models.CASCADE)
    system_amount = models.FloatField(verbose_name='System Amount')
    user_payble_amount = models.FloatField(verbose_name='User Payble Amount')
    system_currency = models.ForeignKey(
        'configurations.CurrencyMaster',
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='system_currency_payment',
        verbose_name='System Currency')
    user_payble_currency = models.ForeignKey(
        'configurations.CurrencyMaster',
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='user_currency_payment',
        verbose_name='User Payble Currency')
    payment_status = models.CharField(max_length=100, choices=PAYMENT_STATUS)
    transaction_id = models.CharField(max_length=255, null=True,
                                      verbose_name='Payment Transaction ID')

    class Meta:
        verbose_name = "User Payment Transaction"
        verbose_name_plural = "User Payment Transaction"
        db_table = 'payment_transaction_after_commission'

    def __str__(self):
        return self.invoice_no
