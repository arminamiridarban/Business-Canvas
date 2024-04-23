# Generated by Django 4.2.11 on 2024-03-30 15:41

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
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
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('channels', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerRelationship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relationship', models.CharField(max_length=511)),
                ('description', models.TextField(max_length=1023)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerSegment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_segment', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ValueProposition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=1023)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='value_propositions', to='canvas.project')),
            ],
        ),
        migrations.CreateModel(
            name='RevenueStreams',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('revenue', models.CharField(max_length=1023)),
                ('customer_segment', models.ManyToManyField(related_name='revenue_stream', to='canvas.customersegment')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='revenue_stream', to='canvas.project')),
            ],
        ),
        migrations.CreateModel(
            name='KeyResources',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key_resource', models.CharField(max_length=255)),
                ('description', models.TextField(max_length=1023)),
                ('channel', models.ManyToManyField(related_name='key_resources', to='canvas.channel')),
                ('customer_relationship', models.ManyToManyField(related_name='key_resources', to='canvas.customerrelationship')),
                ('customer_segment', models.ManyToManyField(related_name='key_resources', to='canvas.customersegment')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='key_resources', to='canvas.project')),
                ('value_propositions', models.ManyToManyField(related_name='key_resources', to='canvas.valueproposition')),
            ],
        ),
        migrations.CreateModel(
            name='KeyPartnership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key_partner', models.CharField(max_length=255)),
                ('description', models.TextField(max_length=1023)),
                ('channel', models.ManyToManyField(related_name='key_partner', to='canvas.channel')),
                ('customer_relationship', models.ManyToManyField(related_name='key_partner', to='canvas.customerrelationship')),
                ('customer_segment', models.ManyToManyField(related_name='key_partner', to='canvas.customersegment')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='key_partner', to='canvas.project')),
                ('value_propositions', models.ManyToManyField(related_name='key_partner', to='canvas.valueproposition')),
            ],
        ),
        migrations.CreateModel(
            name='KeyActivities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key_activity', models.CharField(max_length=255)),
                ('description', models.TextField(max_length=1023)),
                ('channel', models.ManyToManyField(related_name='key_activity', to='canvas.channel')),
                ('customer_relationship', models.ManyToManyField(related_name='key_activity', to='canvas.customerrelationship')),
                ('customer_segment', models.ManyToManyField(related_name='key_activity', to='canvas.customersegment')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='key_activity', to='canvas.project')),
                ('value_propositions', models.ManyToManyField(related_name='key_activity', to='canvas.valueproposition')),
            ],
        ),
        migrations.AddField(
            model_name='customersegment',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_segments', to='canvas.project'),
        ),
        migrations.AddField(
            model_name='customersegment',
            name='value_propositions',
            field=models.ManyToManyField(related_name='customer_segments', to='canvas.valueproposition'),
        ),
        migrations.AddField(
            model_name='customerrelationship',
            name='customer_segment',
            field=models.ManyToManyField(related_name='customer_relationship', to='canvas.customersegment'),
        ),
        migrations.AddField(
            model_name='customerrelationship',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_relationship', to='canvas.project'),
        ),
        migrations.AddField(
            model_name='channel',
            name='customer_segments',
            field=models.ManyToManyField(related_name='channel', to='canvas.customersegment'),
        ),
        migrations.AddField(
            model_name='channel',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='channel', to='canvas.project'),
        ),
    ]