from django.db import migrations
from django.contrib.auth import get_user_model

def crear_admin_inicial(apps, schema_editor):
    Usuario = get_user_model()
    if not Usuario.objects.filter(username='admin').exists():
        Usuario.objects.create_superuser(
            username='admin',
            email='admin@sanblas.com',
            password='admin12081208',
            nombre='admin',
            apellidos='Admin'
        )

class Migration(migrations.Migration):
    dependencies = [
        ('app', '0003_alter_producto_imagenproducto_and_more'), # Su hermana anterior
    ]
    operations = [
        migrations.RunPython(crear_admin_inicial),
    ]