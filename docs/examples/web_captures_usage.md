# Ejemplo: Publicar Capturas Revisadas del Origen WEB

## 1. Contexto del Ejemplo

Se documenta el manual de funcionamiento de una aplicación desplegada en PRE. El usuario ha
dejado dos capturas en `_staging/kuniv/`, pero una muestra datos reales y no ha pasado la
revisión. El ejemplo muestra cómo `web_captures` publica **solo** la captura revisada, detecta
una cita sin texto alternativo y descubre una imagen copiada a mano a `docs/assets/manual/` sin
pasar por la publicación.

## 2. Implementación de Referencia

```python
--8<-- "examples/web_captures_usage.py"
```

## 3. Explicación del Código

- El `sys.path.insert` apunta a `scripts/` porque doc_ia no es un paquete instalable; el script se
  importa por ruta, igual que en los demás ejemplos.
- `publish` recibe la lista explícita de capturas revisadas: `alta.png` no se publica. Registra en
  `.ai/captures.json` la huella, el entorno (`PRE`), la versión desplegada y el rol, nunca la URL.
- La primera comprobación encuentra `sin_alt`: la página cita la captura sin texto alternativo.
- Tras corregir la cita, `check` no encuentra nada.
- Una imagen copiada a mano a `docs/assets/manual/` aparece como `sin_registrar`: no pasó por la
  revisión.

## 4. Ejecución y Pruebas

```bash
python docs/examples/web_captures_usage.py
# Publicada: docs/assets/manual/kuniv/procesos/listado.png
# Sin texto alternativo: [('sin_alt', 'assets/manual/kuniv/procesos/listado.png')]
# Corregido: []
# Copiada a mano: [('sin_registrar', 'alta.png')]
```

Desde la CLI, en un destino (Fase 0-pre, paso de revisión, y Fase 6 / CIERRE):

```bash
python <doc_ia>/scripts/web_captures.py --root <destino> publish kuniv procesos/listado.png --env PRE --version 1.8.8 --role Coordinador
# [captures] publicada docs/assets/manual/kuniv/procesos/listado.png
# [captures] 1 captura(s) publicada(s) · .ai/captures.json      (exit 0)

python <doc_ia>/scripts/web_captures.py --root <destino> check
# [captures] 0 hallazgo(s).                                      (exit 0)
```

## 5. Referencias Relacionadas

- Documentación funcional: [Capturas del Origen WEB](../functional/web_captures.md)
- Referencia técnica: [web_captures](../api/web_captures.md)
- Ejemplos relacionados: [Adquirir Orígenes Documentales](snapshot_sources_usage.md) · [Redactar Credenciales de un Documento Convertido](redact_secrets_usage.md)
