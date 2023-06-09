# Generated by Django 4.1 on 2023-04-26 12:33

import app_shop.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', app_shop.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Catalog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default=0, verbose_name='цена на товар')),
                ('discount', models.IntegerField(default=0, verbose_name='скидка на товар')),
                ('count', models.IntegerField(verbose_name='кол-во товара')),
                ('limited_edition', models.BooleanField(default=False, verbose_name='ограниченный тираж')),
                ('purchases_number', models.PositiveIntegerField(default=0, verbose_name='кол-во покупок')),
            ],
            options={
                'verbose_name': 'каталог',
                'verbose_name_plural': 'каталоги',
                'db_table': 'catalog',
            },
        ),
        migrations.CreateModel(
            name='CatalogImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='files/', verbose_name='изображение')),
            ],
            options={
                'verbose_name': 'изображение',
                'verbose_name_plural': 'изображения',
                'db_table': 'images',
            },
        ),
        migrations.CreateModel(
            name='DynamicSiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='title')),
                ('meta_content', models.CharField(default='page_content', max_length=256, verbose_name='meta_content')),
                ('cache_timeout', models.IntegerField(default=300, verbose_name='cache timeout')),
                ('logo', models.ImageField(null=True, upload_to='site_images/', verbose_name='изображения сайта')),
                ('express_delivery_cost', models.IntegerField(default=500, verbose_name='стоимость экспресс доставки')),
                ('delivery_cost', models.IntegerField(default=200, verbose_name='стоимость доставки')),
                ('order_cost', models.IntegerField(default=2000, verbose_name='стоимость заказа')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Good',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='название товара')),
                ('description', models.TextField(verbose_name='описание товара')),
                ('purchases_number', models.IntegerField(verbose_name='кол-во покупок')),
                ('release_year', models.IntegerField(default=2010, verbose_name='год выпуска')),
            ],
            options={
                'verbose_name': 'товар',
                'verbose_name_plural': 'товары',
                'db_table': 'good',
            },
        ),
        migrations.CreateModel(
            name='GoodCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=30, unique=True, verbose_name='категории товара')),
                ('active_goods', models.BooleanField(verbose_name='активные товары')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
                'db_table': 'good_category',
            },
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=50, verbose_name='название магазина')),
                ('description', models.TextField(verbose_name='описание магазина')),
            ],
            options={
                'verbose_name': 'магазин',
                'verbose_name_plural': 'магазины',
                'db_table': 'shops',
            },
        ),
        migrations.CreateModel(
            name='Specification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='название характеристики')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specification', to='app_shop.goodcategory', verbose_name='категория')),
            ],
            options={
                'verbose_name': 'характеристика',
                'verbose_name_plural': 'характеристики',
                'db_table': 'specifications',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30, verbose_name='имя')),
                ('last_name', models.CharField(max_length=30, verbose_name='фамилия')),
                ('middle_name', models.CharField(max_length=30, null=True, verbose_name='отчество')),
                ('balance', models.FloatField(default=0, verbose_name='баланс')),
                ('tel', models.CharField(max_length=10, verbose_name='телефон')),
                ('avatar', models.ImageField(upload_to='files/', verbose_name='аватар пользователя')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'профиль пользователя',
                'verbose_name_plural': 'профили пользователей',
                'db_table': 'user_profile',
            },
        ),
        migrations.CreateModel(
            name='SpecificationValues',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=20, verbose_name='значение характеристики')),
                ('specification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specification_value', to='app_shop.specification', verbose_name='характеристика')),
            ],
            options={
                'verbose_name': 'значение характеристики',
                'verbose_name_plural': 'значения характеристик',
                'db_table': 'specification_values',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='дата')),
                ('review', models.TextField(verbose_name='отзыв')),
                ('catalog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='app_shop.catalog', verbose_name='каталог')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_shop.userprofile', verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'комментарий',
                'verbose_name_plural': 'комментарии',
                'db_table': 'reviews',
            },
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=20, verbose_name='производитель')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='manufacturer', to='app_shop.goodcategory', verbose_name='категория')),
            ],
            options={
                'verbose_name': 'производитель',
                'verbose_name_plural': 'производители',
                'db_table': 'manufacturer',
            },
        ),
        migrations.AddIndex(
            model_name='goodcategory',
            index=models.Index(fields=['name'], name='good_catego_name_78a25c_idx'),
        ),
        migrations.AddField(
            model_name='good',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='good', to='app_shop.goodcategory', verbose_name='категория товара'),
        ),
        migrations.AddField(
            model_name='good',
            name='manufacturer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_shop.manufacturer'),
        ),
        migrations.AddField(
            model_name='good',
            name='specifications',
            field=models.ManyToManyField(to='app_shop.specificationvalues'),
        ),
        migrations.AddField(
            model_name='catalogimages',
            name='catalog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='app_shop.catalog', verbose_name='каталог'),
        ),
        migrations.AddField(
            model_name='catalog',
            name='good',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='catalog', to='app_shop.good', verbose_name='товар'),
        ),
        migrations.AddField(
            model_name='catalog',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_shop.shop', verbose_name='магазин'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
        migrations.AddIndex(
            model_name='good',
            index=models.Index(fields=['category'], name='good_categor_71654e_idx'),
        ),
        migrations.AlterOrderWithRespectTo(
            name='catalog',
            order_with_respect_to='good',
        ),
        migrations.AddIndex(
            model_name='catalog',
            index=models.Index(fields=['good'], name='catalog_good_id_cd12df_idx'),
        ),
    ]
