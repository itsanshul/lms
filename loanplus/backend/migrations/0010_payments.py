# Generated by Django 2.2.6 on 2019-11-27 21:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('backend', '0009_loanmaster_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('payment_no', models.AutoField(primary_key=True, serialize=False)),
                ('no_of_payments', models.IntegerField()),
                ('pay_date', models.DateTimeField(auto_now_add=True)),
                ('emi_amount', models.FloatField()),
                ('c_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
