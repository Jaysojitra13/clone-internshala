# Generated by Django 2.0.1 on 2018-03-05 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intern', '0003_auto_20180305_0854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='academicdetails',
            name='marksheet_10',
            field=models.FileField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='academicdetails',
            name='marksheet_12',
            field=models.FileField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='academicdetails',
            name='marksheet_clg',
            field=models.FileField(upload_to=''),
        ),
    ]