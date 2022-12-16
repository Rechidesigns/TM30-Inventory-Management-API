# Generated by Django 4.1.1 on 2022-12-16 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retailapp', '0008_alter_cart_cart_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='cart_product',
        ),
        migrations.AddField(
            model_name='cart',
            name='cart_product',
            field=models.ManyToManyField(to='retailapp.product'),
        ),
    ]