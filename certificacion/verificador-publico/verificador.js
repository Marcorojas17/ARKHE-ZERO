/**
 * ═══════════════════════════════════════════════════════════════════════════
 *  ▓▒░ CERTIFICACIÓN · VERIFICADOR PÚBLICO · ARKHÉ ZERO ░▒▓
 *  ─────────────────────────────────────────────────────────────────────────
 *  Cualquiera puede verificar un certificado ARKHÉ sin permiso.
 *  No requiere cuenta. No requiere API key. Solo el hash.
 *
 *  ┌─(kali㉿arkhe-zero)-[~/kronos/certificacion/verificador-publico]
 *  └─$ node verificador.js --hash=f03f7e2d852617309457e0fe207f8f8bd...
 * ═══════════════════════════════════════════════════════════════════════════
 */

import { sha3_512 } from '../../crypto/primitives/sha3-512.js';

export const SEAL = '◯_● · 51/49/100';
export const INDEX_ZERO_SHA256 = 'f03f7e2d852617309457e0fe207f8f8bd2627d0b723de02f3b0ce05767219112';

/**
 * Verifica un hash contra el Índice Cero y devuelve un veredicto público.
 *
 * @param {string} hash
 * @param {string} [contenido] - opcional, para verificar integridad
 * @returns {object}
 */
export function verificar(hash, contenido) {
  const hashOk = /^[0-9a-f]{128}$/i.test(hash);

  let contenidoOk = null;
  if (contenido) {
    contenidoOk = sha3_512(contenido) === hash;
  }

  const esIndiceCero = hash === INDEX_ZERO_SHA256;

  return {
    ok: hashOk && (contenidoOk !== false),
    hash,
    hash_valido: hashOk,
    contenido_ok: contenidoOk,
    es_indice_cero: esIndiceCero,
    veredicto: esIndiceCero
      ? 'ANCLADO AL ÍNDICE CERO · VERIFICADO'
      : hashOk
        ? 'HASH VÁLIDO · SIN ANCLAJE AL ÍNDICE CERO'
        : 'HASH INVÁLIDO · HALT',
    verificable_por: 'CUALQUIERA · SIN PERMISO',
    sellado: SEAL,
  };
}

export const meta = {
  rol: 'verificador-publico',
  access: 'public',
  seal: SEAL,
};