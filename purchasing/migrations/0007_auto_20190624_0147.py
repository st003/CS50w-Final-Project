# Generated by Django 2.2.2 on 2019-06-24 01:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('purchasing', '0006_license_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='license',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='licenses', to='purchasing.Group'),
        ),
    ]
