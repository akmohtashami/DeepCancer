# Generated by Django 2.0.5 on 2018-05-16 14:22

from django.db import migrations, models
import django.db.models.deletion
import engine.models
import enumfields.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ModelRun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='uid')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('input_file', models.FileField(upload_to='', verbose_name='input file')),
                ('task_id', models.CharField(max_length=100, null=True, verbose_name='celery task id')),
                ('status', enumfields.fields.EnumField(default=0, enum=engine.models.ModelRunStatus, max_length=10, verbose_name='status')),
            ],
        ),
        migrations.CreateModel(
            name='ModelRunOutput',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('file', models.FileField(upload_to='', verbose_name='file')),
                ('show_download_link', models.BooleanField(default=True, verbose_name='show download link')),
                ('include_in_results_page', models.BooleanField(default=False, verbose_name='include in results page')),
                ('run', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outputs', to='engine.ModelRun', verbose_name='run')),
            ],
        ),
    ]
