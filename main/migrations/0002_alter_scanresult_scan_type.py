from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scanresult',
            name='scan_type',
            field=models.CharField(choices=[('url', 'URL / Ссылка'), ('apk', 'APK Файл'), ('qr', 'QR Code')], max_length=10),
        ),
    ]
