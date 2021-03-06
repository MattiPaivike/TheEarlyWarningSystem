# Generated by Django 2.2.13 on 2020-11-30 23:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Software',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=50)),
                ('dllink', models.CharField(blank=True, max_length=300)),
                ('dllink_x86', models.CharField(blank=True, max_length=300)),
                ('dllink_x64', models.CharField(blank=True, max_length=300)),
                ('checksum', models.CharField(blank=True, max_length=300)),
                ('checksum_x86', models.CharField(blank=True, max_length=300)),
                ('checksum_x64', models.CharField(blank=True, max_length=300)),
                ('checksum_type', models.CharField(blank=True, max_length=50)),
                ('lastupdated', models.CharField(blank=True, max_length=50)),
                ('software', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.Software')),
            ],
            options={
                'ordering': ('software',),
                'get_latest_by': 'order_date',
            },
        ),
    ]
