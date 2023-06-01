# Generated by Django 4.2 on 2023-05-30 08:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Hr', '0001_initial'),
        ('Finance', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CashTransfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Amount', models.BigIntegerField(blank=True, null=True)),
                ('transferType', models.CharField(max_length=100)),
                ('receipttype', models.CharField(max_length=100)),
                ('nonEmployeename', models.CharField(blank=True, max_length=500, null=True)),
                ('phone_number', models.PositiveBigIntegerField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('incomeSources', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='Finance.incomesource')),
                ('mainAcc', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='Finance.mainaccount')),
                ('reciept', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='Hr.employee')),
            ],
        ),
    ]