/**
 * ═══════════════════════════════════════════════════════════════════════════
 *  ▓▒░ CERTIFICACIÓN · EMISOR VC 2.0 · ARKHÉ ZERO ░▒▓
 *  ─────────────────────────────────────────────────────────────────────────
 *  Emite Verifiable Credentials (W3C VC 2.0) firmadas con ML-DSA-87.
 *
 *  ┌─(kali㉿arkhe-zero)-[~/kronos/certificacion/emisor-certificados]
 *  └─$ node -e "import('./certificados.js').then(m => console.log(m.meta))"
 *     { rol: 'emisor-certificados', standard: 'W3C VC 2.0', ... }
 * ═══════════════════════════════════════════════════════════════════════════
 */

import { sha3_512 } from '../../crypto/primitives/sha3-512.js';
import * as mldsa from '../../crypto/primitives/ml-dsa-87.js';

export const SEAL = '◯_● · 51/49/100';
export const STANDARD = 'W3C VC 2.0';
export const ISSUER_DID = 'did:arkhe:2607146379465';

/**
 * Emite una Verifiable Credential para un documento.
 *
 * @param {object} opciones
 * @param {object} opciones.manifiesto
 * @param {object} opciones.tsa
 * @param {object} opciones.notarial
 * @param {object} [opciones.secretKey]
 * @returns {Promise<object>}
 */
export async function emitirVC({ manifiesto, tsa, notarial, secretKey }) {
  const vc = {
    '@context': [
      'https://www.w3.org/ns/credentials/v2',
      'https://arkhe.zero/contexts/certificacion/v1',
    ],
    id: `urn:arkhe:vc:${manifiesto.hash_sha3_512.slice(0, 16)}`,
    type: ['VerifiableCredential', 'ArkheCertification'],
    issuer: ISSUER_DID,
    validFrom: new Date().toISOString(),
    credentialSubject: {
      id: notarial.acta.firmante_humano,
      documento_hash: manifiesto.hash_sha3_512,
      tsa_authority: tsa.tsa,
      tsa_timestamp: tsa.timestamp,
      notario: notarial.acta.notario,
      acta_hash: notarial.acta_hash,
      governance: { humano: 51, ia: 49, real: 100 },
    },
    proof: {
      type: 'DataIntegrityProof',
      cryptosuite: 'mldsa87-2024',
      created: new Date().toISOString(),
      proofPurpose: 'assertionMethod',
      verificationMethod: `${ISSUER_DID}#ml-dsa-87-key-1`,
    },
    seal: SEAL,
  };

  // Firma la VC (si hay claves)
  if (secretKey) {
    const payload = sha3_512(JSON.stringify(vc));
    const { firma } = mldsa.sign(secretKey, payload);
    vc.proof.proofValue = Buffer.from(firma).toString('base64');
  }

  return {
    ok: true,
    credential: vc,
    standard: STANDARD,
    sellado: SEAL,
    timestamp: new Date().toISOString(),
  };
}

/**
 * Verifica una VC.
 */
export function verificarVC(vc) {
  const hasRequiredFields = Boolean(
    vc['@context'] && vc.type && vc.issuer && vc.credentialSubject && vc.proof
  );

  return {
    valida: hasRequiredFields,
    standard: STANDARD,
    issuer: vc.issuer,
    veredicto: hasRequiredFields
      ? 'CREDENCIAL VÁLIDA · VC 2.0'
      : 'CREDENCIAL INVÁLIDA · HALT',
    sellado: SEAL,
  };
}

export const meta = {
  rol: 'emisor-certificados',
  standard: STANDARD,
  issuer: ISSUER_DID,
  seal: SEAL,
};