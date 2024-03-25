# Documentacion de API EstacionaT
### Ruta principal
* https://estacionatbackend.onrender.com/api/v2/

# user/
### **Ruta: /login/**
Método: POST
* Descripción: Iniciar sesión de usuario.
* Datos requeridos en formato JSON:
```json
{
  "username": "nombre_de_usuario",
  "password": "contraseña"
}
``` 

 * Respuesta exitosa (HTTP 200 OK):

```json
{
  "token": "token_de_autenticación",
  "user": {
    "id": "ID_del_usuario",
    "username": "nombre_de_usuario",
    "last_name": "apellido",
    "email": "correo_electronico",
    "phone": "número_de_teléfono"
  }
}
 ```

* Respuesta de error (HTTP 404 Not Found):
```json 
{
  "error": "El nombre de usuario o la contraseña son inválidos"
}
```
### **Ruta: /signup/**
Método: POST
* Descripción: Registrar un nuevo usuario.
* Datos requeridos en formato JSON:
```json 
{
  "username": "nombre_de_usuario",
  "last_name": "apellido",
  "email": "correo_electronico",
  "password": "contraseña",
  "phone": "número_de_teléfono"
}
```

* Respuesta exitosa (HTTP 201 Created):
```json 
{
  "token": "token_de_autenticación",
  "user": {
    "id": "ID_del_usuario",
    "username": "nombre_de_usuario",
    "last_name": "apellido",
    "email": "correo_electronico",
    "phone": "número_de_teléfono"
  }
}
```

* Respuesta de error (HTTP 400 Bad Request):
```json
{
  "error": "Error en la validación de datos. Asegúrate de enviar todos los campos requeridos."
}
```
### **Ruta: /users/{id}/**
Método: GET
* Descripción: Obtener los detalles de un usuario específico.
* Respuesta exitosa (HTTP 200 OK):

```json
{
  "id": "ID_del_usuario",
  "username": "nombre_de_usuario",
  "last_name": "apellido",
  "email": "correo_electronico",
  "phone": "número_de_teléfono"
}
```

* Respuesta de error (HTTP 404 Not Found):
```json
{
  "error": "El usuario no existe."
}
```

Método: PUT
* Descripción: Actualizar los detalles de un usuario existente.
* Datos requeridos en formato JSON:
```json
{
  "username": "nuevo_nombre_de_usuario",
  "last_name": "nuevo_apellido",
  "email": "nuevo_correo_electronico",
  "phone": "nuevo_número_de_teléfono"
}
```

* Respuesta exitosa (HTTP 200 OK):
```json
{
  "id": "ID_del_usuario",
  "username": "nuevo_nombre_de_usuario",
  "last_name": "nuevo_apellido",
  "email": "nuevo_correo_electronico",
  "phone": "nuevo_número_de_teléfono"
}
```

* Respuesta de error (HTTP 404 Not Found o HTTP 400 Bad Request):
* Si el usuario no existe:
```json
Copy code
{
  "error": "El usuario no existe."
}
```
* Si hay errores en la validación de datos:
```json
{
  "error": "Error en la validación de datos. Asegúrate de enviar todos los campos requeridos."
}
```

Método: DELETE
* Descripción: Eliminar un usuario existente.
* Respuesta exitosa (HTTP 200 OK):
```json
{
  "deleted": true
}
```
Respuesta de error (HTTP 404 Not Found):
```json
{
  "error": "El usuario no existe."
}
```


# **parking/**
### **Ruta: parking/**
Método: GET
* Descripción: Obtener la lista de todos los parqueos.
* Respuesta exitosa (HTTP 200 OK):
```json
[
  {
    "id": "ID_del_parqueo",
    "name": "nombre_del_parqueo",
    "capacity": "capacidad_total_de_vehículos",
    "phone": "número_de_teléfono",
    "email": "correo_electrónico",
    "user": "ID_del_usuario",
    "spaces_available": "espacios_disponibles",
    "url_image": "URL_de_la_imagen",
    "description": "descripción_del_parqueo"
  },
  ...
]
```
* Respuesta de error (HTTP 404 Not Found):
```json
[]
```
Método: POST
* Descripción: Crear un nuevo parqueo.
* Datos requeridos en formato JSON:
```json
{
  "name": "nombre_del_parqueo",
  "capacity": "capacidad_total_de_vehículos",
  "phone": "número_de_teléfono",
  "email": "correo_electrónico",
  "user": "ID_del_usuario",
  "spaces_available": "espacios_disponibles",
  "url_image": "URL_de_la_imagen",
  "description": "descripción_del_parqueo"
}
```
* Respuesta exitosa (HTTP 201 Created):
```json
{
  "id": "ID_del_parqueo",
  "name": "nombre_del_parqueo",
  "capacity": "capacidad_total_de_vehículos",
  "phone": "número_de_teléfono",
  "email": "correo_electrónico",
  "user": "ID_del_usuario",
  "spaces_available": "espacios_disponibles",
  "url_image": "URL_de_la_imagen",
  "description": "descripción_del_parqueo"
}
```

* Respuesta de error (HTTP 400 Bad Request):
```json
{
  "error": "Error en la validación de datos. Asegúrate de enviar todos los campos requeridos."
}
```
### **Ruta: parking/{id}/**
Método: GET
* Descripción: Obtener los detalles de un parqueo específico.
* Respuesta exitosa (HTTP 200 OK):
```json
{
  "id": "ID_del_parqueo",
  "name": "nombre_del_parqueo",
  "capacity": "capacidad_total_de_vehículos",
  "phone": "número_de_teléfono",
  "email": "correo_electrónico",
  "user": "ID_del_usuario",
  "spaces_available": "espacios_disponibles",
  "url_image": "URL_de_la_imagen",
  "description": "descripción_del_parqueo"
}
```
* Respuesta de error (HTTP 404 Not Found):
```json
{
  "error": "El parqueo no existe."
}
```
Método: PUT
* Descripción: Actualizar los detalles de un parqueo existente.
* Datos requeridos en formato JSON:
```json
{
  "name": "nuevo_nombre_del_parqueo",
  "capacity": "nueva_capacidad_total_de_vehículos",
  "phone": "nuevo_número_de_teléfono",
  "email": "nuevo_correo_electrónico",
  "spaces_available": "nuevos_espacios_disponibles",
  "url_image": "nueva_URL_de_la_imagen",
  "description": "nueva_descripción_del_parqueo"
}
```
 * Respuesta exitosa (HTTP 200 OK):
```json

{
  "id": "ID_del_parqueo",
  "name": "nuevo_nombre_del_parqueo",
  "capacity": "nueva_capacidad_total_de_vehículos",
  "phone": "nuevo_número_de_teléfono",
  "email": "nuevo_correo_electrónico",
  "user": "ID_del_usuario",
  "spaces_available": "nuevos_espacios_disponibles",
  "url_image": "nueva_URL_de_la_imagen",
  "description": "nueva_descripción_del_parqueo"
}
```
* Respuesta de error (HTTP 404 Not Found o HTTP 400 Bad Request):
* Si el parqueo no existe:
```json
{
  "error": "El parqueo no existe."
}
```
* Si hay errores en la validación de datos:
```json
{
  "error": "Error en la validación de datos. Asegúrate de enviar todos los campos requeridos."
}
```
Método: DELETE
* Descripción: Eliminar un parqueo existente.
* Respuesta exitosa (HTTP 200 OK):
``` json
{
  "deleted": true
}
```
* Respuesta de error (HTTP 404 Not Found):
```json
{
  "error": "El parqueo no existe."
}
```