# 📘 Instalación · marco.mcp

## Requisitos
- Node.js `>=20`
- npm `>=10`
- Acceso al árbol `ARKHÉ-ZERO/` (para leer `AI-MANIFEST.json`, `MEMORY.md`)

## Instalación estándar

```bash
cd ARKHE-ZERO/marco.mcp
npm install
cp .env.example .env
# editar .env con tus valores reales
npm run build
npm test