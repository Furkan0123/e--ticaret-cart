# Generated by Django 4.2.14 on 2024-07-22 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('small_price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('large_price', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('image', models.ImageField(upload_to='menu_items/')),
                ('is_hot', models.BooleanField(default=True)),
            ],
        ),
    ]
