# Generated by Django 2.2.6 on 2019-11-09 16:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_emi'),
    ]

    operations = [
        migrations.RenameField(
            model_name='loanmaster',
            old_name='cust',
            new_name='app_id',
        ),
    ]