import flet as ft
import requests # <--- El cartero que habla con tu Backend

def main(page: ft.Page):
    # Configuración de la ventana
    page.title = "Therians App"
    page.bgcolor = "#111111" # Fondo oscuro
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # 1. Creamos los campos de texto (Inputs)
    nombre = ft.TextField(label="Nombre", bgcolor="#222222", color="white", border_color="#ff5fa2")
    email = ft.TextField(label="Email", bgcolor="#222222", color="white", border_color="#ff5fa2")
    password = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, bgcolor="#222222", color="white", border_color="#ff5fa2")
    theriotype = ft.TextField(label="Especie / Theriotype", bgcolor="#222222", color="white", border_color="#ff5fa2")
    
    mensaje_pantalla = ft.Text(value="", color="red") # Para mostrar errores o éxitos

    # 2. La función que se ejecuta al apretar el botón
    def registrar_usuario(e):
        # Desactivamos el botón mientras carga
        boton_registro.disabled = True
        mensaje_pantalla.value = "Conectando con el servidor..."
        mensaje_pantalla.color = "white"
        page.update()

        try:
            # Armamos el "paquete" de datos igual que en Thunder Client
            datos = {
                "nombre": nombre.value,
                "email": email.value,
                "password": password.value,
                "theriotype": theriotype.value
            }
            
            # Se lo mandamos a TU servidor Node.js
            url = "http://localhost:5000/api/user"
            respuesta = requests.post(url, json=datos)
            
            # Verificamos qué respondió el servidor
            if respuesta.status_code == 200:
                # ¡Éxito! En vez de mostrar texto verde, saltamos a la otra pantalla
                mostrar_pantalla_cards()
            else:
                mensaje_pantalla.color = "red"
                try:
                    # Intenta leerlo como JSON
                    error_del_server = respuesta.json().get("msg", "Error al registrar")
                except:
                    # Si el servidor mandó HTML o texto raro, mostramos un pedacito para saber qué es
                    error_del_server = f"Error {respuesta.status_code}: {respuesta.text[:60]}"
                
                mensaje_pantalla.value = error_del_server

        except requests.exceptions.ConnectionError:
            mensaje_pantalla.color = "red"
            mensaje_pantalla.value = "Error: ¿El servidor Node.js está encendido? 🔌"
        except Exception as ex:
            mensaje_pantalla.color = "red"
            mensaje_pantalla.value = f"Error inesperado: {ex}"
        
        # Volvemos a activar el botón
        boton_registro.disabled = False
        page.update()
    
    # --- NUEVA FUNCIÓN: PANTALLA DE CARDS ---
    def mostrar_pantalla_cards():
        page.clean() # Borramos el formulario
        
        titulo = ft.Text("Descubrir Manada 🐾", size=30, color="white", weight=ft.FontWeight.BOLD)
        
        # Este contenedor es la "caja" donde vamos a ir poniendo y sacando las tarjetas
        caja_tarjetas = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        page.add(
            ft.Column([titulo, caja_tarjetas], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
        page.update()

        # 1. Función que le PIDE los usuarios a Node.js
        def cargar_usuarios():
            try:
                # OJO: Verificá si tu ruta GET en el backend es /api/user o /api/users
                url = "http://localhost:5000/api/user" 
                respuesta = requests.get(url)
                
                if respuesta.status_code == 200:
                    lista_usuarios = respuesta.json() 
                    mostrar_tarjeta(lista_usuarios, 0) 
                else:
                    # NUEVO: Le pedimos a Python que nos muestre el error exacto del servidor
                    error_real = respuesta.text[:100] # Leemos los primeros 100 caracteres del error
                    caja_tarjetas.controls.append(ft.Text(f"Error {respuesta.status_code}: {error_real}", color="red"))
                    page.update()
            except Exception as e:
                caja_tarjetas.controls.append(ft.Text(f"Error de conexión: {e}", color="red"))
                page.update()

        # 2. Función que DIBUJA la tarjeta de un usuario específico
        def mostrar_tarjeta(lista, indice):
            caja_tarjetas.controls.clear() # Limpiamos la tarjeta anterior
            
            # Si ya pasamos por todos los usuarios...
            if indice >= len(lista):
                caja_tarjetas.controls.append(ft.Text("No hay más perfiles por ahora 🏜️", color="gray"))
                page.update()
                return

            usuario_actual = lista[indice]
            
            # Diseñamos la Tarjeta (Card)
            tarjeta = ft.Container(
                content=ft.Column([
                    ft.Text(usuario_actual.get("nombre", "Sin nombre"), size=26, weight=ft.FontWeight.BOLD, color="white"),
                    ft.Text(f"Especie: {usuario_actual.get('theriotype', 'Desconocido')}", color="#ff5fa2", size=18),
                    
                    # Botones de Acción (Rechazar / Aceptar)
                    ft.Row([
                        # Botón X (Rojo) -> Pasa al siguiente índice
                        ft.IconButton(icon=ft.icons.CLOSE, icon_color="red", icon_size=40, 
                                      on_click=lambda e: mostrar_tarjeta(lista, indice + 1)),
                        # Botón Corazón (Verde) -> Pasa al siguiente índice
                        ft.IconButton(icon=ft.icons.FAVORITE, icon_color="green", icon_size=40, 
                                      on_click=lambda e: mostrar_tarjeta(lista, indice + 1))
                    ], alignment=ft.MainAxisAlignment.CENTER)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor="#1e1e1e",
                padding=30,
                border_radius=15,
                width=300
            )
            
            caja_tarjetas.controls.append(tarjeta)
            page.update()

        # Arrancamos el proceso llamando a la primera función
        cargar_usuarios()
    # ----------------------------------------

    # 3. El botón de registro
    boton_registro = ft.Button(
        content=ft.Text("Registrarse", color="white", weight=ft.FontWeight.BOLD), 
        bgcolor="#ff5fa2",
        on_click=registrar_usuario,
        width=300
    )

    # 4. Agrupamos todo en una "Tarjeta" central (como el CSS de tu compañera)
    tarjeta = ft.Container(
        content=ft.Column([
            ft.Text("AXIS", size=28, weight=ft.FontWeight.BOLD, color="white"),
            nombre,
            email,
            password,
            theriotype,
            boton_registro,
            mensaje_pantalla
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor="#1e1e1e",
        padding=30,
        border_radius=10,
        width=350
    )

    page.add(tarjeta)

ft.run(main)