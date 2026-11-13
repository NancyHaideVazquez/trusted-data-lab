# Evidencia de pruebas de seguridad

## 1. Objetivo

Verificar que las dependencias del proyecto no presenten vulnerabilidades conocidas y que los archivos examinados del repositorio no contengan credenciales o secretos expuestos.

Las comprobaciones se realizaron mediante `pip-audit` y Gitleaks.

## 2. Auditoría de dependencias

**Herramienta:** pip-audit 2.10.1

**Comando ejecutado:**

`python -m pip_audit -r requirements.txt`

**Resultado:**

`No known vulnerabilities found`

La auditoría no identificó vulnerabilidades conocidas en las dependencias resueltas desde el archivo `requirements.txt` durante esta ejecución.

Este resultado corresponde al momento de la revisión y no garantiza que las dependencias estén libres de vulnerabilidades futuras.

## 3. Escaneo de secretos en el historial de Git

**Herramienta:** Gitleaks 8.30.1

**Comando ejecutado:**

`gitleaks git --redact -v .`

**Resultado:**

- Commits examinados: 47.
- Hallazgos: 0.
- Estado: sin secretos detectados.

## 4. Escaneo de archivos del proyecto

Se realizó inicialmente un escaneo completo del directorio de trabajo.

**Resultado inicial:**

- Datos examinados: aproximadamente 641.97 MB.
- Hallazgos potenciales: 257.

La mayoría de los hallazgos procedían de archivos de bibliotecas instaladas dentro de `.venv/`.

También se detectaron dos posibles secretos en el archivo local `.env`.

Se verificó que `.env` está excluido mediante `.gitignore`, no está versionado en Git y no aparece como cambio pendiente.

Posteriormente se realizó un nuevo escaneo excluyendo únicamente `.venv/` y `.env`, mediante una configuración temporal de Gitleaks.

**Resultado del escaneo con exclusiones:**

- Datos examinados: aproximadamente 5.93 MB.
- Hallazgos: 0.
- Estado: sin secretos detectados en los archivos incluidos.

La exclusión de `.env` no significa que sus valores sean falsos positivos. El archivo debe permanecer privado y no publicarse.

## 5. Conclusión

Las comprobaciones realizadas no identificaron vulnerabilidades conocidas en las dependencias auditadas ni secretos en los 47 commits examinados por Gitleaks.

El escaneo de archivos del proyecto, con exclusión del entorno virtual y las credenciales locales, tampoco encontró secretos.

La auditoría de seguridad deberá repetirse después de actualizar dependencias, incorporar nuevas credenciales o modificar componentes relevantes del proyecto.