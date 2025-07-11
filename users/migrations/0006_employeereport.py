# Generated by Django 5.2.3 on 2025-06-21 12:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_customuser_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work_summary', models.TextField()),
                ('highlights', models.TextField()),
                ('judgment_parameters', models.JSONField(default=list)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('manager_feedback', models.TextField(blank=True, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
