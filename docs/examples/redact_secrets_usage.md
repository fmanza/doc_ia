# Ejemplo: Redactar Credenciales de un Documento Convertido

## 1. Contexto del Ejemplo

Un diseño técnico de integraciones, convertido a Markdown con `convert_to_md.py`, trae en una URL
de ejemplo el `client_secret` de OAuth en claro. Ese texto se va a copiar a `_fuentes/` y a
versionar en el destino. El ejemplo muestra cómo `redact_secrets` encuentra el valor, lo sustituye
por `<REDACTADO>` en el sitio y deja intactos la descripción de un parámetro de contraseña y el
marcador `xxxxxx`.

## 2. Implementación de Referencia

```python
--8<-- "examples/redact_secrets_usage.py"
```

## 3. Explicación del Código

- El `sys.path.insert` apunta a `scripts/` porque doc_ia no es un paquete instalable; el script se
  importa por ruta, igual que en los demás ejemplos.
- `find_secrets` devuelve solo `(línea, regla)`: nunca el valor. La fila `| p2 | -- | Password de
  la llamada |` no se detecta porque no hay valor tras la palabra clave, y `**Contraseña:** xxxxxx`
  es un marcador.
- `redact_tree` recorre los `.md` de la carpeta, sustituye solo el valor y conserva la clave
  (`client_secret=<REDACTADO>`): el documento sigue diciendo que había un secreto y dónde.
- Una segunda pasada no encuentra nada: la herramienta es idempotente.

## 4. Ejecución y Pruebas

```bash
python docs/examples/redact_secrets_usage.py
# Antes: [(8, 'client_secret')]
# Redactado: Diseno_Integraciones.md:8 · client_secret
# Después: []
# **Ej.** https://idp.example/v1/token?grant_type=authorization_code&client_secret=<REDACTADO>
```

Desde la CLI, en la Fase 0c (antes de copiar a `_fuentes/`) y en el CIERRE (comprobación):

```bash
python <doc_ia>/scripts/redact_secrets.py _staging/diseno_integraciones/md
# [redact] _staging\diseno_integraciones\md\Diseno_Integraciones.md:8 · client_secret
# [redact] 1 valor(es) redactado(s).          (exit 1)

python <doc_ia>/scripts/redact_secrets.py _fuentes --check
# [redact] 0 valor(es) pendiente(s) de redactar.   (exit 0)
```

## 5. Referencias Relacionadas

- Documentación funcional: [Redacción de Credenciales](../functional/redact_secrets.md)
- Referencia técnica: [redact_secrets](../api/redact_secrets.md)
- Ejemplos relacionados: [Adquirir Orígenes Documentales](snapshot_sources_usage.md) · [Convertir documentos a Markdown](convert_to_md_usage.md)
