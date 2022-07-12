# Generated by Django 4.0.6 on 2022-07-12 08:42

from django.db import migrations
import django.utils.timezone
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_product_image_ppoi_alter_product_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='images',
            field=versatileimagefield.fields.VersatileImageField(blank=True, default=django.utils.timezone.now, upload_to='photos/products', verbose_name='Image'),
            preserve_default=False,
        ),
    ]