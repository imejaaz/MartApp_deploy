# Generated by Django 4.2.6 on 2023-12-19 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_rename_disc_category_desc_rename_disc_discount_desc_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='brand',
            old_name='description',
            new_name='desc',
        ),
        migrations.AddField(
            model_name='brand',
            name='discount',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
