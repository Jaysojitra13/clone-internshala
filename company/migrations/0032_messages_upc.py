# Generated by Django 2.0.1 on 2018-03-23 08:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0031_auto_20180323_0452'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='upc',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='company.UserPostConnection'),
        ),
    ]