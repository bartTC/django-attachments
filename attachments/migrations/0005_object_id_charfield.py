from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attachments', '0004_db_index'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='object_id',
            field=models.CharField(db_index=True, max_length=64),
        ),
    ]
