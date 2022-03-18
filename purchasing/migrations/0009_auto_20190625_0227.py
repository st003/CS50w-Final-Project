# Generated by Django 2.2.2 on 2019-06-25 02:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('purchasing', '0008_auto_20190624_0234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='license',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='licenses', to=settings.AUTH_USER_MODEL),
        ),
    ]