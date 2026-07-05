# Firmas de correo — Alfondo

Generador de firmas HTML para el equipo de [alfondo.cl](https://alfondo.cl). Diseño moderno compatible con **Gmail / Google Workspace**: tablas + CSS inline, logo oficial, fotos del equipo y preview web.

---

## Inicio rápido

```bash
cd signature
python3 server.py
```

Abre **http://localhost:8765/index.html**

El servidor de desarrollo:
- Sirve los archivos estáticos sin caché
- Regenera firmas automáticamente al editar `team.json` o `generate.py`
- Actualiza el preview en el navegador en ~1s

### Solo generar (sin servidor)

```bash
python3 generate.py
```

---

## Estructura del proyecto

```
signature/
├── team.json          # Fuente de verdad — datos de cada persona
├── generate.py        # Plantilla HTML + generación de archivos
├── server.py          # Servidor de desarrollo con live reload
├── index.html         # Portal del equipo (preview + código HTML)
├── netlify.toml       # Config para deploy estático en Netlify
├── team/              # Fragmentos HTML por persona (generados)
│   └── {slug}.html
└── view/              # Páginas completas para copiar en Gmail (generados)
    └── {slug}.html
```

| Archivo | Editar manualmente | Descripción |
|---------|-------------------|-------------|
| `team.json` | ✅ Sí | Datos del equipo |
| `generate.py` | ✅ Sí | Diseño/plantilla de la firma |
| `index.html` | ✅ Sí | UI del portal |
| `team/*.html` | ❌ No | Generados — se sobrescriben |
| `view/*.html` | ❌ No | Generados — se sobrescriben |
| `server.py` | Solo dev | No desplegar en producción |

---

## Datos del equipo (`team.json`)

Cada entrada tiene esta forma:

```json
{
  "slug": "heber-arratia",
  "nombre": "Heber Arratia",
  "cargo": "Socio Fundador | CTO",
  "titulo": "Ingeniero de software",
  "email": "heber.arratia@alfondo.cl",
  "linkedin": "https://www.linkedin.com/in/heberarratia",
  "foto": "https://alfondo.cl/team/heber3.png"
}
```

| Campo | Requerido | Notas |
|-------|-----------|-------|
| `slug` | Sí | Identificador único, kebab-case. Define nombres de archivo. |
| `nombre` | Sí | Nombre completo visible en la firma |
| `cargo` | Sí | Cargo principal |
| `titulo` | No | Grado/título. Si es `null`, no se muestra |
| `email` | Sí | Solo informativo en el portal (no va en la firma) |
| `linkedin` | No | Si existe, muestra badge `in` junto a alfondo.cl |
| `foto` | No | URL pública. Si es `null`, usa placeholder ui-avatars.com |

**Fotos oficiales** están en `https://alfondo.cl/team/` (extraídas de [alfondo.cl/team](https://alfondo.cl/team)).

Tras editar `team.json`:
- Con `server.py` corriendo → regeneración automática
- Sin servidor → `python3 generate.py`

---

## Cómo usa el equipo sus firmas

1. Entrar al portal (`index.html` desplegado o localhost)
2. Buscar su nombre
3. **Opción A (Gmail):** clic en **Abrir firma** → `Cmd+A` → `Cmd+C` → pegar en Gmail → Configuración → Firma
4. **Opción B:** copiar el código HTML del cuadro de texto (respaldo / admin)

> Gmail necesita contenido **renderizado** (Opción A). Pegar código HTML crudo en el editor visual de Gmail no funciona.

---

## Despliegue para el equipo

**No enviar solo `index.html`** — depende de `team.json`, `team/` y `view/` vía fetch.

### Opción recomendada: subdominio alfondo.cl

Subir como sitio estático en `firmas.alfondo.cl` o `alfondo.cl/firmas`:

```
index.html
team/*.html
view/*.html
```

No incluir en producción: `server.py`, `generate.py`, `team.json` (opcional — contiene emails).

### Netlify

```bash
python3 generate.py
# Arrastrar carpeta a netlify.com/drop
# o conectar repo — netlify.toml ya incluido
```

---

## Diseño de la firma

La plantilla vive en `generate.py` → función `build_signature()`.

### Restricciones técnicas (email HTML)

- **Tablas** para layout (`<table>`, no flexbox/grid)
- **CSS inline** en cada elemento (Gmail ignora `<style>` externo)
- **Sin SVG** — no renderiza bien en clientes de correo
- **Imágenes por URL pública** — no rutas locales ni base64
- Fuentes: system stack (`-apple-system`, `Helvetica Neue`, `Arial`)
- Logo: `https://alfondo.cl/logo-negro-sinfondo.png`

### Paleta de marca

| Uso | Color |
|-----|-------|
| Texto principal | `#1A1F2E` |
| Texto secundario | `#888888` |
| Acento terracota | `#D4837A` |
| Barra vertical | `#D4837A` |
| Links alfondo.cl | `#D4837A` |

### Layout

```
[Foto circular 72px]  |  Nombre (bold 17px)
                      |  Cargo · Título
                      |  alfondo.cl · [in]
                      |  [logo alfondo]
```

---

## Guía para agentes IA

### Contexto del proyecto

Proyecto interno de **alfondo.cl** — consultora que ayuda a crear, escalar y financiar proyectos (postulación a fondos CORFO/SERCOTEC, innovación, software). **No es asesoría patrimonial.**

### Flujo de cambios

```
team.json  ──→  generate.py  ──→  team/{slug}.html
                              ──→  view/{slug}.html
                              ──→  index.html (carga vía fetch)
```

### Tareas comunes

| Tarea | Acción |
|-------|--------|
| Agregar persona | Nueva entrada en `team.json` → `python3 generate.py` |
| Cambiar cargo/título | Editar `team.json` |
| Cambiar diseño global | Editar `build_signature()` en `generate.py` |
| Agregar LinkedIn | Campo `linkedin` en `team.json` |
| Cambiar foto | Campo `foto` con URL pública |
| Sincronizar con web | Datos en [alfondo.cl/team](https://alfondo.cl/team) |

### Reglas al modificar

1. **Nunca editar `team/*.html` ni `view/*.html` directamente** — se regeneran
2. **`slug` debe ser único** y coincidir con el patrón `nombre-apellido`
3. **Mantener compatibilidad email** al cambiar CSS (inline, tablas, sin SVG)
4. **`index.html` usa fetch** — requiere servidor HTTP, no funciona con `file://`
5. **`server.py` es solo desarrollo** — producción es estático
6. Tras cambios en `generate.py` o `team.json`, correr `generate.py` si no hay servidor activo

### Archivos legacy (ignorar o eliminar)

- `signature.html` — firma de ejemplo inicial
- `preview.html` — preview antiguo de una sola firma

### Comandos de referencia

```bash
# Desarrollo con live reload
python3 server.py

# Generar firmas una vez
python3 generate.py

# Verificar servidor
curl http://localhost:8765/__dev/version
```

### Dependencias

Solo **Python 3** estándar. Sin pip, sin node.
