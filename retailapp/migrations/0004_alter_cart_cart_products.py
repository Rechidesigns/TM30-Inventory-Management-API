# Generated by Django 4.1.1 on 2022-12-16 09:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('retailapp', '0003_alter_cart_cart_products'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='cart_products',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='retailapp.product'),
        ),
    ]
