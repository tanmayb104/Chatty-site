# Generated by Django 3.1 on 2021-07-13 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0002_auto_20210628_0042'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-timestamp']},
        ),
        migrations.AlterField(
            model_name='room',
            name='code',
            field=models.CharField(default='b55988', max_length=6, primary_key=True, serialize=False),
        ),
    ]