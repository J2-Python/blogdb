# blogdrf

Proyecto base de Django REST Framework para un blog sencillo con fines educativos.

## Estructura

- Proyecto Django: `blogdj/`
- Aplicación principal: `blogdj/applications/blog/`
- Comandos Django: ejecutar desde `blogdj/`

## Comandos básicos

Desde `blogdj/`:

```bash
python manage.py runserver
python manage.py check
python manage.py migrate
python manage.py test --settings=blogdj.settings.test
```

## Seed de datos de prueba

El proyecto incluye un endpoint para borrar y recrear datos de ejemplo del blog.

- Endpoint: `POST /api/seed/basic`
- Uso principal: resetear el contenido y volver a generar datos de prueba
- Cantidad por defecto: `20` posts
- Protección: solo funciona cuando `DEBUG=True`

### Qué crea

El seed elimina los datos actuales del blog y vuelve a crear:

- categorías
- palabras clave
- autores
- blogs
- suscripciones de ejemplo

### Request

Si no envías cuerpo, crea `20` registros de blog:

```bash
curl -X POST http://127.0.0.1:8000/api/seed/basic
```

También puedes indicar una cantidad personalizada con `count`:

```bash
curl -X POST http://127.0.0.1:8000/api/seed/basic \
  -H "Content-Type: application/json" \
  -d '{"count": 12}'
```

### Response esperada

```json
{
  "message": "Datos de prueba recreados correctamente.",
  "created": {
    "categories": 4,
    "keywords": 8,
    "authors": 5,
    "blogs": 20,
    "suscriptions": 20
  }
}
```

## Notas

- `manage.py` usa por defecto `blogdj.settings.local`
- `blogdj/secrets.json` debe existir para comandos locales
- Los tests usan `blogdj.settings.test` con SQLite
