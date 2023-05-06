# Generated by Django 2.2.28 on 2023-05-06 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remote_host', models.GenericIPAddressField(db_index=True)),
                ('remote_logname', models.CharField(blank=True, max_length=100, null=True)),
                ('remote_user', models.CharField(blank=True, max_length=100, null=True)),
                ('request_time', models.DateTimeField()),
                ('request_line', models.TextField(blank=True, null=True)),
                ('final_status', models.PositiveIntegerField(blank=True, null=True)),
                ('bytes_sent', models.PositiveIntegerField(blank=True, null=True)),
                ('referer', models.TextField(blank=True, null=True)),
                ('user_agent', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['request_time', 'remote_host'],
            },
        ),
        migrations.CreateModel(
            name='LogFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(auto_now=True)),
                ('file_path', models.TextField()),
                ('last_line', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['date_time'],
            },
        ),
    ]