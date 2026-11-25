# Publishing pesping / Publicar pesping

## English

### Validate locally
```powershell
py -m pip install --upgrade build twine pytest
py -m pip install -e .
py -m pytest -q
py -m build
py -m twine check dist/*
```

### Configure PyPI Trusted Publishing
1. Open https://pypi.org/ and sign in. For an unpublished project, configure a **pending trusted publisher** under your PyPI account; otherwise configure the publisher on your PyPI project.
2. Set owner `jpesqueda`, repository `pesping`, workflow filename `publish.yml`, and environment `pypi`.
3. In GitHub repository settings, create environment `pypi` under **Settings → Environments**.
4. Verify GitHub Actions CI passes on `main` before publishing.
5. Create a GitHub release tagged `v1.1.0` to trigger `.github/workflows/publish.yml`.
6. Check the GitHub Actions publishing job and https://pypi.org/project/pesping/. Install with `py -m pip install pesping` after publication.

**Do not** commit PyPI API tokens or passwords. Trusted Publishing uses GitHub OIDC. Make sure the project name is available on PyPI before the first release. Publishing is not triggered by a normal commit.

### Future releases
Increment the version in both `pyproject.toml` and `src/pesping.py`, run tests, push changes, and publish a new GitHub release. PyPI does not permit replacing files for an already published version.

## Español

### Validación local
```powershell
py -m pip install --upgrade build twine pytest
py -m pip install -e .
py -m pytest -q
py -m build
py -m twine check dist/*
```

### Configuración de Trusted Publishing
1. Accede a https://pypi.org/. Si todavía no existe el proyecto, registra un **pending trusted publisher**; si ya existe, configura el publisher desde la administración del proyecto.
2. Usa owner `jpesqueda`, repositorio `pesping`, archivo workflow `publish.yml` y environment `pypi`.
3. En GitHub, crea el environment `pypi` en **Settings → Environments**.
4. Verifica que las pruebas de CI finalicen correctamente en `main`.
5. Crea una release con tag `v1.1.0` para ejecutar `.github/workflows/publish.yml`.
6. Confirma la publicación en Actions y https://pypi.org/project/pesping/. Después podrás instalar con `py -m pip install pesping`.

**Nunca** subas tokens ni contraseñas al repositorio. Trusted Publishing utiliza OIDC de GitHub. Verifica primero que el nombre del paquete esté disponible. Un commit normal no publica en PyPI.

### Próximas versiones
Actualiza la versión tanto en `pyproject.toml` como en `src/pesping.py`, ejecuta pruebas, sube los cambios y crea una release nueva. PyPI no permite reemplazar archivos de una versión publicada.
