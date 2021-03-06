# Generated by Django 3.1 on 2020-08-12 04:14

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=150, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_username', message='Username must be alphanumeric or contain numbers and lowercaps', regex='^[a-za-z0-9]+$')])),
                ('email', models.EmailField(blank=True, max_length=255, null=True, unique=True)),
                ('first_name', models.CharField(max_length=255, null=True, validators=[django.core.validators.RegexValidator(code='invalid_first_name', message='First name must be letters only', regex='^[a-zA-Z ]+$')])),
                ('last_name', models.CharField(max_length=255, null=True, validators=[django.core.validators.RegexValidator(code='invalid_last_name', message='Last name must be letters only', regex='^[a-zA-Z ]+$')])),
                ('active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, null=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=100)),
                ('birthday', models.DateField(blank=True, max_length=10, null=True)),
                ('mobile_number', models.CharField(blank=True, max_length=13, validators=[django.core.validators.RegexValidator(code='invalid_cp_number', message='Please enter a valid cellphone number.', regex='^(09|\\+639)\\d{9}$')])),
                ('image', models.ImageField(blank=True, default='default.jpg', null=True, upload_to='profile_pics')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
