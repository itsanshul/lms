# Generated by Django 2.2.6 on 2019-11-05 19:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LoanDetail',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type_of_loan', models.CharField(max_length=50)),
                ('duration', models.CharField(max_length=10)),
                ('rate', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='LoanApplication',
            fields=[
                ('app_id', models.AutoField(primary_key=True, serialize=False)),
                ('loan_amount', models.FloatField()),
                ('cust_name', models.CharField(max_length=50)),
                ('income', models.FloatField()),
                ('age', models.IntegerField()),
                ('address', models.TextField()),
                ('phone', models.IntegerField()),
                ('email', models.EmailField(max_length=70)),
                ('loan_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.LoanDetail')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pan_no', models.CharField(max_length=10)),
                ('phone', models.IntegerField()),
                ('address', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
