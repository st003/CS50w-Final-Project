# Generated by Django 2.2.2 on 2019-06-12 03:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('purchasing', '0002_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(1, 'Credit'), (2, 'Invoice')], default=None, null=True)),
                ('status', models.IntegerField(choices=[(0, 'Unpaid'), (1, 'Pending'), (2, 'Paid'), (3, 'Declined')], default=0)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]