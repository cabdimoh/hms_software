# Generated by Django 4.2 on 2023-05-27 07:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Inventory', '0001_initial'),
        ('LRPD', '0001_initial'),
        ('APEN', '0003_initial'),
        ('Hr', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='radiologyequipmentorder',
            name='Ordered_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='pharmacytransection',
            name='PhMedId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='LRPD.pharmacy_medicine'),
        ),
        migrations.AddField(
            model_name='pharmacytransection',
            name='employe',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Hr.employee'),
        ),
        migrations.AddField(
            model_name='pharmacy_medicine',
            name='Medicine_categories',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Inventory.medicine_categories'),
        ),
        migrations.AddField(
            model_name='pharmacy_medicine',
            name='Medicine_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Inventory.medicine'),
        ),
        migrations.AddField(
            model_name='medicineorderdetails',
            name='Medicine_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Inventory.medicine'),
        ),
        migrations.AddField(
            model_name='medicineorderdetails',
            name='medicineOrderid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LRPD.medicineorder'),
        ),
        migrations.AddField(
            model_name='medicineorder',
            name='Ordered_BY',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='labtestsubgroups',
            name='Group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LRPD.labtestgroups'),
        ),
        migrations.AddField(
            model_name='labtestresult',
            name='Collected_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='collected_by', to='Hr.employee'),
        ),
        migrations.AddField(
            model_name='labtestresult',
            name='Employee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employee', to='Hr.employee'),
        ),
        migrations.AddField(
            model_name='labtestresult',
            name='LabTestOrder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LRPD.labtestorders'),
        ),
        migrations.AddField(
            model_name='labtestorders',
            name='Admission',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='APEN.addmission'),
        ),
        migrations.AddField(
            model_name='labtestorders',
            name='Appointment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='APEN.appointments'),
        ),
        migrations.AddField(
            model_name='labtestorders',
            name='Visit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='APEN.emergencyroomvisit'),
        ),
        migrations.AddField(
            model_name='labtestorderdetails',
            name='LabTestOrder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LRPD.labtestorders'),
        ),
        migrations.AddField(
            model_name='labtestorderdetails',
            name='Test',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='LRPD.labtests'),
        ),
        migrations.AddField(
            model_name='labtest_blood_properties',
            name='Group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LRPD.labtestgroups'),
        ),
        migrations.AddField(
            model_name='labtest_blood_properties',
            name='SubGroup',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='LRPD.labtestsubgroups'),
        ),
        migrations.AddField(
            model_name='labtest_blood_properties',
            name='TestID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LRPD.labtests'),
        ),
        migrations.AddField(
            model_name='labexaminationparameters',
            name='Test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='LRPD.labtests'),
        ),
        migrations.AddField(
            model_name='labequipmentorder',
            name='Item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Inventory.equipment'),
        ),
        migrations.AddField(
            model_name='labequipmentorder',
            name='Ordered_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='lab_examinationparameters_results',
            name='Parameter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='LRPD.labexaminationparameters'),
        ),
        migrations.AddField(
            model_name='lab_examinationparameters_results',
            name='TestID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LRPD.labtests'),
        ),
        migrations.AddField(
            model_name='lab_examinationparameters_results',
            name='labTest_result',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LRPD.labtestresult'),
        ),
        migrations.AddField(
            model_name='lab_blood_results',
            name='TestID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LRPD.labtest_blood_properties'),
        ),
        migrations.AddField(
            model_name='lab_blood_results',
            name='labTest_result',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LRPD.labtestresult'),
        ),
    ]