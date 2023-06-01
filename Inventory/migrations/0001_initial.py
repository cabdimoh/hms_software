# Generated by Django 4.2 on 2023-05-27 07:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Hr', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=40)),
                ('quantity', models.PositiveIntegerField()),
                ('lost_and_damaged', models.IntegerField()),
                ('manufacturing', models.CharField(max_length=100)),
                ('supplier_price', models.FloatField()),
            ],
            options={
                'db_table': 'Equipment',
            },
        ),
        migrations.CreateModel(
            name='Equipment_categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=40)),
                ('discription', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'Equipment_categories',
            },
        ),
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Medicine_name', models.CharField(max_length=100)),
                ('box', models.PositiveIntegerField()),
                ('quantity', models.PositiveIntegerField()),
                ('dosage', models.CharField(max_length=100)),
                ('manufacturing', models.CharField(max_length=100)),
                ('supplier_price', models.FloatField()),
                ('status', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'Medicine',
            },
        ),
        migrations.CreateModel(
            name='Medicine_categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medicine_cat_name', models.CharField(max_length=40)),
                ('discription', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'medicine_categories',
            },
        ),
        migrations.CreateModel(
            name='MedicineTransection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Type', models.CharField(max_length=100)),
                ('box', models.PositiveIntegerField()),
                ('qty', models.PositiveIntegerField()),
                ('manufacturing_date', models.DateField()),
                ('BatchNO', models.CharField(max_length=100)),
                ('supplier_price', models.CharField(max_length=100)),
                ('Expire_date', models.DateField()),
                ('date', models.DateField(auto_now_add=True)),
                ('status', models.CharField(max_length=100)),
                ('MedId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Inventory.medicine')),
                ('employe', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Hr.employee')),
            ],
            options={
                'db_table': 'MedicineTransection',
            },
        ),
        migrations.AddField(
            model_name='medicine',
            name='Medicine_categories',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Inventory.medicine_categories'),
        ),
        migrations.CreateModel(
            name='lost_and_dameged_equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lost_and_damaged', models.PositiveIntegerField()),
                ('reason', models.CharField(max_length=100)),
                ('Status', models.CharField(max_length=100)),
                ('Equipment_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Inventory.equipment')),
            ],
            options={
                'db_table': 'lost_and_dameged_equipment',
            },
        ),
        migrations.CreateModel(
            name='EquipmentTransection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Type', models.CharField(max_length=200)),
                ('quantity', models.PositiveIntegerField()),
                ('lost_and_damaged', models.IntegerField()),
                ('manufacturing', models.CharField(max_length=100)),
                ('supplier_price', models.FloatField()),
                ('Transectno', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=100)),
                ('date', models.DateField(auto_now_add=True)),
                ('EqId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Inventory.equipment')),
            ],
            options={
                'db_table': 'EquipmentTransection',
            },
        ),
        migrations.AddField(
            model_name='equipment',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Inventory.equipment_categories'),
        ),
        migrations.AddField(
            model_name='equipment',
            name='employe',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Hr.employee'),
        ),
    ]