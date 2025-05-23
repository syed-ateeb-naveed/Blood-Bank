# Generated by Django 4.2.17 on 2025-05-01 10:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("worker", "0003_alter_status_status"),
        ("patient", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="request",
            name="status",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="request_status",
                to="worker.status",
            ),
        ),
    ]
