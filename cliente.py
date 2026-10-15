import requests

URL_BASE = "http://localhost:5000"

def menu():
    while True:
        print("\n--- SISTEMA DE GESTIÓN DE TAREAS ---")
        print("1. Registrar usuario")
        print("2. Iniciar sesión y ver tareas")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            usuario = input("Nuevo usuario: ")
            password = input("Contraseña: ")
            # Enviar petición POST a /registro
            r = requests.post(f"{URL_BASE}/registro", json={"usuario": usuario, "contraseña": password})
            print("Servidor:", r.json())

        elif opcion == '2':
            usuario = input("Usuario: ")
            password = input("Contraseña: ")
            # Enviar petición POST a /login
            r = requests.post(f"{URL_BASE}/login", json={"usuario": usuario, "contraseña": password})
            
            if r.status_code == 200:
                print("Servidor:", r.json().get("mensaje"))
                # Si el login es correcto, consultamos GET /tareas
                r_tareas = requests.get(f"{URL_BASE}/tareas")
                print("\n--- Respuesta de GET /tareas (HTML) ---")
                print(r_tareas.text.strip())
            else:
                print("Error:", r.json().get("error"))

        elif opcion == '3':
            print("Saliendo...")
            break
        else:
            print("Opción no válida.")

if __name__ == '__main__':
    try:
        menu()
    except requests.exceptions.ConnectionError:
        print("Error: No se pudo conectar con la API. Asegurate de que servidor.py esté ejecutándose.")