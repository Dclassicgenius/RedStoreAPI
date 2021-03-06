# Generated by Django 4.0.6 on 2022-07-14 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_rename_variation_value_variation_color_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='variation',
            old_name='color',
            new_name='variation_value',
        ),
        migrations.RemoveField(
            model_name='variation',
            name='size',
        ),
        migrations.AddField(
            model_name='variation',
            name='variation_category',
            field=models.CharField(choices=[('color', 'color'), ('size', 'size')], default=0, max_length=100),
            preserve_default=False,
        ),
    ]
