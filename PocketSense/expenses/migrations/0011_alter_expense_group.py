# Generated by Django 4.2.17 on 2025-01-09 03:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0010_remove_expense_settlement_settlement_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to='expenses.group'),
        ),
    ]
