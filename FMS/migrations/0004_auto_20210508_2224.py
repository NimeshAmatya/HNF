# Generated by Django 3.1.6 on 2021-05-08 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FMS', '0003_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(default='Forms/Nform.png', upload_to='Forms'),
        ),
    ]
