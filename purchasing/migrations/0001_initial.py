# Generated by Django 2.2.2 on 2019-06-12 02:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(max_length=64)),
                ('middle_name', models.CharField(blank=True, max_length=64, null=True)),
                ('last_name', models.CharField(max_length=64)),
                ('suffix_name', models.CharField(blank=True, max_length=3, null=True)),
                ('address_1', models.CharField(blank=True, max_length=128, null=True)),
                ('address_2', models.CharField(blank=True, max_length=128, null=True)),
                ('city', models.CharField(blank=True, max_length=128, null=True)),
                ('state', models.CharField(blank=True, max_length=64, null=True)),
                ('postal', models.CharField(blank=True, max_length=16, null=True)),
                ('country', models.CharField(blank=True, max_length=128, null=True)),
                ('access_level', models.IntegerField(choices=[(1, 'Licencee'), (2, 'Purchaser'), (3, 'Administrator')], default=2)),
                ('is_active', models.BooleanField(default=True)),
                ('django_admin', models.BooleanField(default=False)),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='purchasing.Group')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
