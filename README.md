# Configuración del entorno de desarrollo

## 1. Creación del entorno virtual

Para crear un entorno virtual con el nombre `venv`, puedes usar el siguiente comando:

```bash
python3 -m venv venv
```
## 2. activar del entorno virtual

Para activar un entorno virtual con el nombre `venv`, puedes usar el siguiente comando:

### windows
```bash
venv\Scripts\activate
```

### Unix o MacOS
```bash
source venv/bin/activate
```

## 3. Instalar dependencias

Para instalar todas las dependencias de **_requirements.txt_**, usa el siguiente comando:
```bash
pip install -r requirements.txt
```
## 4. Configurar variables de entorno

se debe crear un archivo **_.env_** y poner las siguientes variables:
```bash
MONGODB_URL=
DB_NAME=
```
## 5. Correr script

se deben ejecutar los siguientes comandos para **reestructurar** la BD:
```bash
python  main.py
```