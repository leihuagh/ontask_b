# Generated by Django 2.1.1 on 2018-09-25 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0023_auto_20180722_1013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='column',
            name='data_type',
            field=models.CharField(choices=[('string', 'string'), ('integer', 'integer'), ('double', 'double'), ('boolean', 'boolean'), ('datetime', 'datetime')], max_length=512, verbose_name='type of data to store in the column'),
        ),
    ]
