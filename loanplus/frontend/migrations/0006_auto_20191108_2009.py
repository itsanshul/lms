# Generated by Django 2.2.6 on 2019-11-08 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0005_auto_20191106_2334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loanapplication',
            name='status',
            field=models.CharField(max_length=10),
        ),
    ]
