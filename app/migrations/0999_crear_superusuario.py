from django.db import migrations
from django.contrib.auth import get_user_model

def crear_admin_inicial(apps, schema_editor):
    Usuario = get_user_model()
    # Cambia 'admin', 'admin@sanblas.com' y 'TuContraseña123' por lo que tú quieras
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
        # Esto le dice a Django que se ejecute después de tus modelos anteriores
        ('app', '0002_usuario_saldo'),
    ]

    operations = [
        migrations.RunPython(crear_admin_inicial),
    ]