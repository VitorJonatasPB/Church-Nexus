import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secretaria', '0004_alter_membro_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='congregacao',
            name='data_cadastro',
            field=models.DateField(auto_now_add=True, db_index=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='membro',
            name='data_cadastro',
            field=models.DateField(auto_now_add=True, db_index=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
