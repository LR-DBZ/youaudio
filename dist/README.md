# YouAudio → MP3 Downloader — Instalación
# by TUP4C

## Linux
1. **Instalar Docker**
   ```sh
   curl -fsSL https://get.docker.com | sh
   sudo usermod -aG docker $USER
   # cerrar sesión y volver a entrar
   docker --version
   ```
2. **Instalar Docker Compose** (plugin incluido con Docker ≥ 23)
   ```sh
   docker compose version
   ```
3. **Desplegar**
   ```sh
   cd dist
   docker compose up --build -d
   ```
4. Abrir `http://localhost:5000`
5. **Si el puerto 5000 está ocupado**, cambiarlo en `docker-compose.yml`:
   ```yaml
   ports:
     - "5001:5000"   # 5001 es el puerto anfitrión, cambia a gusto
   ```
   Luego acceder a `http://localhost:5001`

## youaudio CLI — actualización y mantenimiento

youaudio incluye un comando de terminal para facilitar la instalación,
actualización y mantenimiento del proyecto.

### Instalar el comando

```sh
cd dist
./youaudio install
```

Esto crea un enlace simbólico en `/usr/local/bin/youaudio`.
Ahora puedes ejecutar `youaudio` desde cualquier directorio.

### Actualizar a la última versión

```sh
youaudio update                          # actualizar proyecto actual (raíz)
youaudio update ~/ruta/del/proyecto      # actualizar proyecto específico
```

El comando descarga la última versión desde GitHub, reemplaza los archivos
de `dist/`, preserva la configuración local y las canciones descargadas,
y reinicia el contenedor Docker automáticamente.

**Nota:** ejecutar `youaudio update` apuntando a la raíz del proyecto (donde
está `dist/docker-compose.yml`), no dentro de `dist/` — el script necesita
ver la estructura completa del proyecto para funcionar correctamente.

### Desinstalar el comando

```sh
sudo rm /usr/local/bin/youaudio
```

## Windows
### Opción A: WSL v2 + Docker (recomendado)
1. **WSL v2** — PowerShell como Admin:
   ```powershell
   wsl --install -d Ubuntu
   wsl --set-default-version 2
   ```
2. **Docker dentro de WSL** — seguir pasos de Linux arriba
3. La app corre en `http://localhost:5000` desde WSL

### Opción B: Docker Desktop
1. Descargar e instalar [Docker Desktop](https://www.docker.com/products/docker-desktop/)
2. Usar WSL 2 backend (Settings → Resources → WSL Integration)
3. Abrir terminal (PowerShell o WSL), ir a `dist/` y:
   ```powershell
   docker compose up --build -d
   ```

## Nota configuración de Puertos
- El contenedor expone el puerto **5000** (interno)
- El `docker-compose.yml` mapea `"5000:5000"` (anfitrión:contenedor)
- Si el puerto 5000 del anfitrión ya está ocupado, edita solo el lado izquierdo: `"5001:5000"` y accede a `http://localhost:5001`

## Carpeta Music
- Los audios convertidos quedan en `dist/music/`
- Es un **volumen persistente** — sobrevive a `docker compose down` y `docker compose up`
- Para eliminar los MP3: `sudo rm -rf dist/music/*` (Linux) o vaciar la carpeta manualmente
- Cada archivo es MP3 a 320kbps con metadatos: `<título> - <autor>.mp3`
- El contenedor también usa `dist/download/` como temporal (m4as descargados)
