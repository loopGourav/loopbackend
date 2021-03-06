# Generated by Django 3.2.6 on 2021-08-21 06:41

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CountryMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('is_active', models.BooleanField(default=True)),
                ('country', models.CharField(db_index=True, max_length=50, unique=True)),
                ('isd', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(99999), django.core.validators.MinValueValidator(1)], verbose_name='ISD/Country Code')),
                ('mobile_no_digits', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(15), django.core.validators.MinValueValidator(5)], verbose_name='Countries Mobile Number digit')),
                ('code', models.CharField(blank=True, max_length=10, null=True, verbose_name='ISO Code')),
                ('timezone', models.CharField(help_text='Please add correct country timezone.', max_length=100)),
                ('created_by', models.ForeignKey(db_column='created_by', limit_choices_to=models.Q(('is_staff', 0), ('is_superuser', 0), _negated=True), on_delete=django.db.models.deletion.CASCADE, related_name='created_countrymasters', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
            ],
            options={
                'verbose_name': '  Country Master',
                'verbose_name_plural': '  Country Master',
                'db_table': 'country_master',
            },
        ),
        migrations.CreateModel(
            name='StateMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('is_active', models.BooleanField(default=True)),
                ('state', models.CharField(db_index=True, max_length=50)),
                ('country', models.ForeignKey(db_column='country', limit_choices_to={'is_active': '1'}, on_delete=django.db.models.deletion.CASCADE, to='configurations.countrymaster')),
                ('created_by', models.ForeignKey(db_column='created_by', limit_choices_to=models.Q(('is_staff', 0), ('is_superuser', 0), _negated=True), on_delete=django.db.models.deletion.CASCADE, related_name='created_statemasters', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('updated_by', models.ForeignKey(db_column='updated_by', limit_choices_to=models.Q(('is_staff', 0), ('is_superuser', 0), _negated=True), null=True, on_delete=django.db.models.deletion.CASCADE, related_name='updated_statemasters', to=settings.AUTH_USER_MODEL, verbose_name='Updated By')),
            ],
            options={
                'verbose_name': ' State Master',
                'verbose_name_plural': ' State Master',
                'db_table': 'state_master',
                'unique_together': {('country', 'state')},
            },
        ),
        migrations.CreateModel(
            name='PaymentCommissionRule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('is_active', models.BooleanField(default=True)),
                ('is_country_applicable', models.BooleanField(default=False)),
                ('commission_value', models.FloatField()),
                ('country', models.ForeignKey(blank=True, db_column='country', limit_choices_to={'is_active': '1'}, null=True, on_delete=django.db.models.deletion.CASCADE, to='configurations.countrymaster')),
                ('created_by', models.ForeignKey(db_column='created_by', limit_choices_to=models.Q(('is_staff', 0), ('is_superuser', 0), _negated=True), on_delete=django.db.models.deletion.CASCADE, related_name='created_paymentcommissionrules', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('updated_by', models.ForeignKey(db_column='updated_by', limit_choices_to=models.Q(('is_staff', 0), ('is_superuser', 0), _negated=True), null=True, on_delete=django.db.models.deletion.CASCADE, related_name='updated_paymentcommissionrules', to=settings.AUTH_USER_MODEL, verbose_name='Updated By')),
            ],
            options={
                'verbose_name': 'Payment Commission Rule',
                'verbose_name_plural': 'Payment Commission Rule',
                'db_table': 'payment_commission_rule',
            },
        ),
        migrations.CreateModel(
            name='CurrencyMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('is_active', models.BooleanField(default=True)),
                ('currency', models.CharField(max_length=30, unique=True)),
                ('symbol', models.CharField(max_length=30)),
                ('code_iso', models.CharField(blank=True, max_length=30, null=True, verbose_name='Code ISO')),
                ('hex_symbol', models.CharField(blank=True, max_length=30, null=True, verbose_name='Hex Symbol')),
                ('created_by', models.ForeignKey(db_column='created_by', limit_choices_to=models.Q(('is_staff', 0), ('is_superuser', 0), _negated=True), on_delete=django.db.models.deletion.CASCADE, related_name='created_currencymasters', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('updated_by', models.ForeignKey(db_column='updated_by', limit_choices_to=models.Q(('is_staff', 0), ('is_superuser', 0), _negated=True), null=True, on_delete=django.db.models.deletion.CASCADE, related_name='updated_currencymasters', to=settings.AUTH_USER_MODEL, verbose_name='Updated By')),
            ],
            options={
                'verbose_name': 'Currency Master',
                'verbose_name_plural': 'Currency Master',
                'db_table': 'currency_master',
            },
        ),
        migrations.AddField(
            model_name='countrymaster',
            name='currency',
            field=models.ForeignKey(blank=True, limit_choices_to={'is_active': '1'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='country_master_currency', to='configurations.currencymaster', verbose_name='Currency'),
        ),
        migrations.AddField(
            model_name='countrymaster',
            name='updated_by',
            field=models.ForeignKey(db_column='updated_by', limit_choices_to=models.Q(('is_staff', 0), ('is_superuser', 0), _negated=True), null=True, on_delete=django.db.models.deletion.CASCADE, related_name='updated_countrymasters', to=settings.AUTH_USER_MODEL, verbose_name='Updated By'),
        ),
        migrations.CreateModel(
            name='CityMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('is_active', models.BooleanField(default=True)),
                ('city', models.CharField(db_index=True, max_length=50)),
                ('created_by', models.ForeignKey(db_column='created_by', limit_choices_to=models.Q(('is_staff', 0), ('is_superuser', 0), _negated=True), on_delete=django.db.models.deletion.CASCADE, related_name='created_citymasters', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('state', models.ForeignKey(db_column='state', limit_choices_to={'is_active': '1'}, on_delete=django.db.models.deletion.CASCADE, to='configurations.statemaster')),
                ('updated_by', models.ForeignKey(db_column='updated_by', limit_choices_to=models.Q(('is_staff', 0), ('is_superuser', 0), _negated=True), null=True, on_delete=django.db.models.deletion.CASCADE, related_name='updated_citymasters', to=settings.AUTH_USER_MODEL, verbose_name='Updated By')),
            ],
            options={
                'verbose_name': 'City Master',
                'verbose_name_plural': 'City Master',
                'db_table': 'city_master',
                'unique_together': {('state', 'city')},
            },
        ),
    ]
