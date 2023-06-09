# Generated by Django 4.2 on 2023-05-30 13:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Hr', '0001_initial'),
        ('Finance', '0002_cashtransfer'),
    ]

    operations = [
        migrations.AddField(
            model_name='cashtransfer',
            name='usercreated',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='cashtransfer',
            name='incomeSources',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='Finance.incomesource'),
        ),
        migrations.AlterField(
            model_name='cashtransfer',
            name='mainAcc',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='Finance.mainaccount'),
        ),
        migrations.AlterField(
            model_name='cashtransfer',
            name='reciept',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='Hr.employee'),
        ),
    ]
