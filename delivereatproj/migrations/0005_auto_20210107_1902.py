# Generated by Django 3.1.4 on 2021-01-07 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivereatproj', '0004_auto_20210107_1036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
