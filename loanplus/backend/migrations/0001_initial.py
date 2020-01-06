# Generated by Django 2.2.6 on 2019-11-08 19:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('frontend', '0006_auto_20191108_2009'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoanMaster',
            fields=[
                ('loan_id', models.AutoField(primary_key=True, serialize=False)),
                ('loan_tenure', models.IntegerField()),
                ('loan_amount', models.FloatField()),
                ('interest_rate', models.FloatField()),
                ('issue_date', models.DateTimeField(auto_now_add=True)),
                ('phone', models.CharField(max_length=10)),
                ('address', models.TextField()),
                ('c_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.LoanApplication')),
                ('loan_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.LoanDetail')),
            ],
        ),
    ]
