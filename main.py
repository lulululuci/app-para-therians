import flet as ft
import requests

def main(page: ft.Page):
    # Configuración base de la App
    page.title = "Therians App"
    page.bgcolor = "#111111"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    URL_BASE = "http://localhost:5000/api/user" 

    # ---------------------------------------------------------
    # 5. PANTALLA PRINCIPAL
    # ---------------------------------------------------------
    def mostrar_principal():
        page.clean() 
        page.navigation_bar = None 
        
        # --- 1. DATOS FALSOS ---
        usuarios_descubrir = [
            {"nombre": "Shadow", "especie": "Lobo Negro", "vibras": "Bosque Nocturno"},
            {"nombre": "Aurora", "especie": "Leopardo de las Nieves", "vibras": "Montañas Frías"},
            {"nombre": "Garra", "especie": "Zorro Rojo", "vibras": "Matorrales y praderas"}
        ]
        
        estado = {"indice": 0}

        # --- 2. DISEÑO DEL "AVISTAMIENTO" ---
        zona_avistamiento = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)

        def actualizar_tarjeta():
            zona_avistamiento.controls.clear()
            
            if estado["indice"] >= len(usuarios_descubrir):
                zona_avistamiento.controls.append(
                    ft.Column([
                        ft.Icon(ft.Icons.NIGHTLIGHT_ROUND, size=80, color="gray"),
                        ft.Text("El bosque está en silencio...", size=20, color="gray", weight=ft.FontWeight.BOLD),
                        ft.Text("Vuelve más tarde para buscar rastros.", color="gray")
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                )
            else:
                usuario = usuarios_descubrir[estado["indice"]]
                
                tarjeta_mistica = ft.Container(
                    content=ft.Column([
                        ft.Text("✨ Rastro detectado ✨", color="#ff5fa2", weight=ft.FontWeight.BOLD),
                        ft.CircleAvatar(radius=50, content=ft.Icon(ft.Icons.PETS, size=40, color="#1e1e1e"), bgcolor="#ff5fa2"),
                        ft.Text(usuario["nombre"], size=30, color="white", weight=ft.FontWeight.BOLD),
                        ft.Text(f"Especie: {usuario['especie']}", size=18, color="white"),
                        ft.Text(f"Hábitat: {usuario['vibras']}", size=14, color="gray"),
                        ft.Container(height=20),
                        
                        # BOTONES PERSONALIZADOS (Alineación perfecta)
                        ft.Row([
                            # Botón: Dejar pasar
                            ft.Container(
                                content=ft.Row([ft.Icon(ft.Icons.ECO, color="gray", size=18), ft.Text("Dejar pasar", color="gray", size=14)], alignment=ft.MainAxisAlignment.CENTER),
                                bgcolor="#222222",
                                padding=12, # Un poco menos de padding para que respiren
                                border_radius=30,
                                on_click=siguiente_perfil,
                                ink=True,
                                expand=True # <--- LA MAGIA: Se ajusta al tamaño perfecto
                            ),
                            # Botón: Acercarse
                            ft.Container(
                                content=ft.Row([ft.Icon(ft.Icons.FAVORITE, color="white", size=18), ft.Text("Acercarse", color="white", size=14)], alignment=ft.MainAxisAlignment.CENTER),
                                bgcolor="#ff5fa2",
                                padding=12,
                                border_radius=30,
                                on_click=siguiente_perfil,
                                ink=True,
                                expand=True # <--- LA MAGIA: Se ajusta al tamaño perfecto
                            )
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=15)
                        
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    width=320,
                    padding=30,
                    bgcolor="#1a1a24", 
                    border_radius=20,
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=20, color="#4cff5fa2")
                )
                zona_avistamiento.controls.append(tarjeta_mistica)
            
            page.update()

        def siguiente_perfil(e):
            estado["indice"] += 1
            actualizar_tarjeta()

        actualizar_tarjeta()

        # --- 3. LAS VISTAS ---
        vista_descubrir = ft.Column([
            ft.Text("Territorio 🐾", size=30, color="white", weight=ft.FontWeight.BOLD),
            zona_avistamiento 
        ], visible=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        vista_matches = ft.Column([ft.Text("Tus Manadas 💚", size=30, color="white", weight=ft.FontWeight.BOLD)], visible=False, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        # --- DISEÑO DEL PERFIL (Mockup) ---
        vista_perfil = ft.Column([
            ft.Text("Mi Refugio 🐺", size=30, color="white", weight=ft.FontWeight.BOLD),
            ft.Container(height=20), # Espaciador
            
            # Foto de Perfil
            ft.CircleAvatar(radius=60, bgcolor="#ff5fa2", content=ft.Icon(ft.Icons.PERSON, size=60, color="#1e1e1e")),
            
            # Datos del Usuario (Pronto vendrán de la BD)
            ft.Text("Leonardo (Prueba)", size=26, color="white", weight=ft.FontWeight.BOLD),
            ft.Text("Especie: Lobo Gris", size=18, color="#ff5fa2"),
            ft.Container(height=30), # Espaciador
            
            # Botones de Configuración
            ft.Container(
                content=ft.Row([ft.Icon(ft.Icons.EDIT, color="white"), ft.Text("Editar Perfil", color="white", weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.CENTER),
                bgcolor="#222222", width=250, padding=15, border_radius=10, ink=True
            ),
            ft.Container(
                content=ft.Row([ft.Icon(ft.Icons.LOGOUT, color="white"), ft.Text("Cerrar Sesión", color="white", weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.CENTER),
                bgcolor="#8b0000", width=250, padding=15, border_radius=10, ink=True,
                # on_click=mostrar_eleccion # (Esto lo activaremos luego para volver al inicio)
            )
        ], visible=False, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        contenido = ft.Column([vista_descubrir, vista_matches, vista_perfil], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True)

        # --- 4. LOS BOTONES DEL MENÚ ---
        btn_descubrir = ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.EXPLORE, color="white", size=24), 
                ft.Text("Explorar", color="white", size=12, weight=ft.FontWeight.BOLD)
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
            bgcolor="#ff5fa2", width=100, height=65, border_radius=10, on_click=lambda e: cambiar_pestana(0)
        )
        
        btn_matches = ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.GROUPS, color="white", size=24), 
                ft.Text("Manada", color="white", size=12, weight=ft.FontWeight.BOLD)
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
            bgcolor="#444444", width=100, height=65, border_radius=10, on_click=lambda e: cambiar_pestana(1)
        )
        
        btn_perfil = ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.PERSON_OUTLINE, color="white", size=24), 
                ft.Text("Perfil", color="white", size=12, weight=ft.FontWeight.BOLD)
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
            bgcolor="#444444", width=100, height=65, border_radius=10, on_click=lambda e: cambiar_pestana(2)
        )

        def cambiar_pestana(indice):
            vista_descubrir.visible = False
            vista_matches.visible = False
            vista_perfil.visible = False
            
            if indice == 0: vista_descubrir.visible = True
            elif indice == 1: vista_matches.visible = True
            elif indice == 2: vista_perfil.visible = True
            
            btn_descubrir.bgcolor = "#ff5fa2" if indice == 0 else "#444444"
            btn_matches.bgcolor = "#ff5fa2" if indice == 1 else "#444444"
            btn_perfil.bgcolor = "#ff5fa2" if indice == 2 else "#444444"
            
            page.update()

        barra_inferior = ft.Container(
            bgcolor="#1e1e1e",
            padding=10,
            content=ft.Row([btn_descubrir, btn_matches, btn_perfil], alignment=ft.MainAxisAlignment.CENTER, spacing=15)
        )

        pantalla_completa = ft.Column([contenido, barra_inferior], expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        page.add(pantalla_completa)
        page.update()

    # ---------------------------------------------------------
    # 4. PANTALLA DE INICIO DE SESIÓN
    # ---------------------------------------------------------
    def mostrar_login(e=None):
        page.clean()
        
        email = ft.TextField(label="Email", bgcolor="#222222", color="white", border_color="#ff5fa2")
        password = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, bgcolor="#222222", color="white", border_color="#ff5fa2")
        mensaje = ft.Text(value="", color="red")

        def hacer_login(e):
            mensaje.value = "Conectando..."
            mensaje.color = "white"
            page.update()
            
            try:
                res = requests.post(f"{URL_BASE}/login", json={"email": email.value, "password": password.value})
                if res.status_code == 200:
                    mostrar_principal() 
                else:
                    mensaje.value = "Email o contraseña incorrectos 🚫"
                    mensaje.color = "red"
            except Exception as ex:
                print(f"🔥 ERROR: {ex}")
                page.clean()
                page.add(ft.Text(f"Error crítico: {ex}", color="red"))
            page.update()

        tarjeta = ft.Container(
            content=ft.Column([
                ft.Text("Iniciar Sesión", size=28, weight=ft.FontWeight.BOLD, color="white"),
                email, password,
                ft.Button(content=ft.Text("Ingresar", color="white"), bgcolor="#ff5fa2", on_click=hacer_login, width=300),
                mensaje,
                ft.TextButton("Volver atrás", on_click=mostrar_eleccion)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor="#1e1e1e", padding=30, border_radius=10, width=350
        )
        page.add(tarjeta)
        page.update()

    # ---------------------------------------------------------
    # 3. PANTALLA DE REGISTRO
    # ---------------------------------------------------------
    def mostrar_registro(e=None):
        page.clean()
        
        nombre = ft.TextField(label="Nombre", bgcolor="#222222", color="white", border_color="#ff5fa2")
        email = ft.TextField(label="Email", bgcolor="#222222", color="white", border_color="#ff5fa2")
        password = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, bgcolor="#222222", color="white", border_color="#ff5fa2")
        theriotype = ft.TextField(label="Especie / Theriotype", bgcolor="#222222", color="white", border_color="#ff5fa2")
        mensaje = ft.Text(value="", color="red")

        def hacer_registro(e):
            mensaje.value = "Creando cuenta..."
            mensaje.color = "white"
            page.update()
            
            try:
                datos = {"nombre": nombre.value, "email": email.value, "password": password.value, "theriotype": theriotype.value}
                res = requests.post(URL_BASE, json=datos)
                
                if res.status_code == 200:
                    mostrar_principal() 
                else:
                    mensaje.value = "Error al registrar"
                    mensaje.color = "red"
            except Exception as ex:
                print(f"🔥 ERROR: {ex}")
                page.clean()
                page.add(ft.Text(f"Error crítico: {ex}", color="red"))
            page.update()

        tarjeta = ft.Container(
            content=ft.Column([
                ft.Text("Registrarse", size=28, weight=ft.FontWeight.BOLD, color="white"),
                nombre, email, password, theriotype,
                ft.Button(content=ft.Text("Crear Cuenta", color="white"), bgcolor="#ff5fa2", on_click=hacer_registro, width=300),
                mensaje,
                ft.TextButton("Volver atrás", on_click=mostrar_eleccion)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor="#1e1e1e", padding=30, border_radius=10, width=350
        )
        page.add(tarjeta)
        page.update()

    # ---------------------------------------------------------
    # 2. PANTALLA DE ELECCIÓN
    # ---------------------------------------------------------
    def mostrar_eleccion(e=None):
        page.clean()
        
        logo = ft.Text("🐺", size=80)
        titulo = ft.Text("AXIS App", size=35, color="white", weight=ft.FontWeight.BOLD)
        
        btn_login = ft.Button(content=ft.Text("Iniciar Sesión", color="white"), bgcolor="#444444", width=250, height=50, on_click=mostrar_login)
        btn_registro = ft.Button(content=ft.Text("Crear Cuenta", color="white"), bgcolor="#ff5fa2", width=250, height=50, on_click=mostrar_registro)

        page.add(ft.Column([logo, titulo, ft.Container(height=30), btn_login, btn_registro], horizontal_alignment=ft.CrossAxisAlignment.CENTER))
        page.update()

    # ---------------------------------------------------------
    # 1. PANTALLA DE TÉRMINOS
    # ---------------------------------------------------------
    def mostrar_terminos():
        titulo = ft.Text("Políticas y Condiciones", size=24, color="white", weight=ft.FontWeight.BOLD)
        texto = ft.Text(
            "Bienvenido a AXIS App. Al continuar, aceptas nuestras políticas de privacidad y normas de convivencia de la manada. "
            "Nos comprometemos a mantener este espacio seguro, respetuoso y libre de hate.",
            color="gray", text_align=ft.TextAlign.CENTER
        )
        
        btn_aceptar = ft.Button(content=ft.Text("Acepto y quiero entrar", color="white", weight=ft.FontWeight.BOLD), bgcolor="#ff5fa2", width=300, on_click=mostrar_eleccion)

        tarjeta = ft.Container(
            content=ft.Column([titulo, texto, ft.Container(height=20), btn_aceptar], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor="#1e1e1e", padding=30, border_radius=10, width=350
        )
        page.add(tarjeta)
        page.update()

    mostrar_terminos()

ft.run(main)