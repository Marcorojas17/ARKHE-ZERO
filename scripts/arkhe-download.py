#!/usr/bin/env python3
import urllib.request
from bs4 import BeautifulSoup
import hashlib
import json
import os
from datetime import datetime

def sellar_archivos_vault():
    print('[ARKHE-ZERO] Iniciando descarga y sellado de la FBI Vault...')
    url = 'https://vault.fbi.gov'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Connection': 'keep-alive'
    }
    
    # Crear carpeta para los archivos
    os.makedirs('vault_downloads', exist_ok=True)
    registro = []
    
    try:
        req = urllib.request.Request(url, headers=headers)
        html = urllib.request.urlopen(req).read()
        soup = BeautifulSoup(html, 'html.parser')
        
        # Buscamos los enlaces de los documentos recientes
        for link in soup.find_all('a', href=True):
            texto = link.get_text(strip=True)
            
            # Filtramos para agarrar solo los documentos recientes
            if texto and ('Part' in texto or 'Final' in texto):
                doc_url = url + link['href']
                print(f'[+] Analizando: {texto}')
                
                try:
                    # Entramos a la página del documento para buscar el PDF
                    req_doc = urllib.request.Request(doc_url, headers=headers)
                    html_doc = urllib.request.urlopen(req_doc).read()
                    soup_doc = BeautifulSoup(html_doc, 'html.parser')
                    
                    # Buscamos el enlace directo al PDF
                    pdf_link = None
                    for a in soup_doc.find_all('a', href=True):
                        if a['href'].lower().endswith('.pdf'):
                            pdf_link = a['href']
                            break
                    
                    if pdf_link:
                        pdf_url = url + pdf_link if not pdf_link.startswith('http') else pdf_link
                        nombre_archivo = f"vault_downloads/{texto.replace(' ', '_').replace('/', '')[:30]}.pdf"
                        
                        print(f'    -> Descargando PDF...')
                        req_pdf = urllib.request.Request(pdf_url, headers=headers)
                        pdf_data = urllib.request.urlopen(req_pdf).read()
                        
                        # Guardar archivo
                        with open(nombre_archivo, 'wb') as f:
                            f.write(pdf_data)
                            
                        # Calcular hash SHA-256 del archivo real
                        hash_obj = hashlib.sha256(pdf_data).hexdigest()
                        
                        registro.append({
                            'titulo': texto,
                            'archivo': nombre_archivo,
                            'sha256': hash_obj,
                            'bytes': len(pdf_data)
                        })
                        print(f'    -> ✅ Sellado: {hash_obj[:16]}...')
                        
                except Exception as e:
                    print(f'    -> ❌ Error en este documento: {e}')
        
        # Guardar el registro maestro
        resultado = {
            'timestamp': datetime.now().isoformat(),
            'total_descargados': len(registro),
            'documentos': registro
        }
        
        with open('arkhe_vault_pdfs.json', 'w') as f:
            json.dump(resultado, f, indent=2)
            
        print(f'[OK] Proceso terminado. {len(registro)} archivos guardados y sellados.')
        
    except Exception as e:
        print(f'[ERROR GLOBAL] {e}')

if __name__ == '__main__':
    sellar_archivos_vault()
