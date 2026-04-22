### Inbstalar entorno virtual
```
python -m venv tutorial-env
```

### Crear proyectos de DJANGO
```
django-admin startproject biblioteca
```

### Ejecutar proyecto
```
python3 manage.py runserver
```

### Crear Aplicaciones
```
mkdir applications
cd applications
django-admin startapp libro
```

### short cuts
```
fk: llaves foraneas
mc: char field
md: date field
mimg: image field
```

### migraciones
```
python3 manage.py makemigrations (inicial para modelos de django)
python3 manage.py makemigrations tu_app (para migraciones en una app especifica)
python3 manage.py migrate
```

### crear usuarios
```
python3 manage.py createsuperuser
python3 manage.py changepassword "blogdbadmin"
user blogdbadmin
password admin123456
```

### Actualizar version de DJANGO a la 5.2.12 compatible con la version de python 3.14.2
```
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install --upgrade "Django>=5.2.8,<5.3"
python -m django --version
python manage.py check
python manage.py runserver
```

### Instalar DRF
```
pip install djangorestframework
```

### instalar los paquetes del proyecto
```
pip install -r requirements.txt
```

### ejecutar django con un arcchivo settings personalizado
python3 manage.py runserver --settings=bibliotecapro.settings.local

### configuracion db
```
psql -U postgres
postgres=# CREATE DATABASE blogdb;
postgres=# CREATE USER blogdbadmin;
postgres=# \c blogdb;
You are now connected to database "blogdb" as user "jota".
bibliodb=# ALTER USER blogdbadmin WITH password 'blogdbadmin123';
bibliodb=# \c postgres
You are now connected to database "postgres" as user "jota".
postgres=# ALTER DATABASE blogdb OWNER TO blogdbadmin;
```

### Configuracion path de postgres
```
echo 'export PATH="/Library/PostgreSQL/17/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
psql --version
pg_isready
```

### para borrar el cache de python
```
git rm -r --cached .
git add .
git commit -m "Ignorar archivos compilados de Python y __pycache__"
```

### restaurar la migracion inicial
```
mkdir -p tu_app/migrations
touch tu_app/migrations/__init__.py
python manage.py makemigrations tu_app
python manage.py migrate --fake-initial
```
### eliminar una rama e incluir una nueva
```
git remote -v
git remote remove origin
git remote add origin https://github.com/J2-Python/blogdb.git
```

### JSON para Creacion de Blog via metodo POST
```
{
    "author": 2,
    "kwords": [2,3],
    "categorys": [2,3,4],
    "title": "Primer Blog Via Ap",
    "resume": "Resumen del blog",
    "content": "Contenido completo del blog",
    "date": "2026-04-22T18:30:00Z"
}
```