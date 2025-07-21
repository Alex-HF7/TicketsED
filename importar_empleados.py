
import os
import django
import pandas as pd

# Configura el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TicketsED.settings')
django.setup()

from empleado.models import Empleado

# Mapeo de nombres amigables de departamentos a los valores del modelo
depto_map = {
    'Dir. General': 'Dir General',
    'Del. Administrativa': 'Del Administrativa',
    'UCG': 'UCG',
    'Sub. Juridica': 'Sub Jurídica',
    'Sub. Planeación': 'Sub Planeación',
    'Sub. Comercialización': 'Sub Comercialización',
    'Sub. Técnica': 'Sub Técnica'
}

# Cargar datos desde el archivo Excel
df = pd.read_excel('usuarios_empleados3.xlsx')

for _, row in df.iterrows():
    username = str(row['username']).strip()
    if not username:
        continue

    empleado, creado = Empleado.objects.get_or_create(username=username)
    empleado.first_name = row.get('first_name', '').strip()
    empleado.last_name = row.get('last_name', '').strip()
    empleado.email = row.get('email', '').strip()

    depto_raw = row.get('depto', '').strip()
    empleado.depto = depto_map.get(depto_raw, 'Dir General')  # Valor por defecto si no coincide

    rol = row.get('rol', 'empleado').strip()
    empleado.rol = rol if rol in dict(Empleado.ROLES) else 'empleado'

    password = str(row.get('password', '123456')).strip()
    empleado.set_password(password)

    empleado.save()
    print(f"{'✔ Creado' if creado else '✎ Actualizado'}: {empleado.username}")
