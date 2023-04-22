# Generated by Django 4.1 on 2023-03-20 07:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_shop', '0006_dynamicsitesettings_delivery_cost_and_more'),
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='goods',
        ),
        migrations.CreateModel(
            name='OrdersToGoods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(verbose_name='кол-во товара')),
                ('good', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='good_to_order', to='app_shop.catalog')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_to_good', to='payment.order')),
            ],
        ),
    ]
