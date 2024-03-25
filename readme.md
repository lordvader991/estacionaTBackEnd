# Documentacion de API EstacionaT
### Ruta principal
* https://estacionatbackend.onrender.com/api/v2/

## user/
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