# Ejemplo: Verificar Entorno

## 1. Contexto del Ejemplo

Antes de generar documentación o ejecutar las puertas de calidad conviene confirmar que
el entorno tiene instaladas las cuatro herramientas del tooling (`mkdocs`, `ruff`, `mypy`,
`pytest`). Este ejemplo muestra las dos formas de hacerlo: ejecutar el script CLI tal
cual, o importar `missing_tools` desde código propio (mismo patrón que usan los tests
del proyecto).

## 2. Implementación de Referencia

```python
--8<-- "docs/examples/check_env_usage.py"
```

## 3. Explicación del Código

- El `sys.path.insert` apunta a `scripts/` porque doc_ia no es un paquete instalable:
  los scripts se importan por ruta (mismo patrón que `tests/test_check_env.py`).
- `missing_tools` usa `importlib.util.find_spec`, que detecta importabilidad **sin
  importar** la herramienta: no ejecuta código de terceros ni toca la red.
- El resultado preserva el orden de `REQUIRED_TOOLS`, por lo que el output es determinista.

## 4. Ejecución y Pruebas

```bash
python docs/examples/check_env_usage.py
# Entorno de tooling documental completo.

python scripts/check_env.py && echo OK
# Entorno de tooling documental completo.
# OK

python -m py_compile docs/examples/check_env_usage.py   # validación sintáctica
```

Con una herramienta ausente, el output sería `Faltan herramientas: <lista>` y el script
CLI devolvería código de salida `1`.

## 5. Referencias Relacionadas

- Documentación funcional: [Verificación de Entorno](../functional/check_env.md)
- Referencia técnica: [check_env](../api/check_env.md)
- Ejemplos relacionados: [Generar ZIP Offline](build_docs_zip_offline.md)
