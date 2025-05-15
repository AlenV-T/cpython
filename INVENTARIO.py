import csv
import os
import fnmatch

inventario = []

# ------------------ Cargar y Guardar Archivos ------------------

def cargar_inventario():
    if os.path.exists("inventario.txt"):
        with open("inventario.txt", "r", encoding="utf-8") as archivo:
            for linea in archivo:
                nombre, codigo, precio, cantidad, categoria = linea.strip().split("|")
                producto = {
                    "nombre": nombre,
                    "codigo": codigo,
                    "precio": float(precio),
                    "cantidad": int(cantidad),
                    "categoria": categoria
                }
                inventario.append(producto)

def guardar_inventario():
    with open("inventario.txt", "w", encoding="utf-8") as archivo:
        for p in inventario:
            archivo.write(f'{p["nombre"]}|{p["codigo"]}|{p["precio"]}|{p["cantidad"]}|{p["categoria"]}\n')

# ------------------ Funciones Principales ------------------

def agregar_producto():
    print("\n--- Agregar Producto ---")
    nombre = input("Nombre: ")
    codigo = input("Código único: ")
    if any(p["codigo"].lower() == codigo.lower() for p in inventario):
        print("Ya existe un producto con ese código.")
        return
    try:
        precio = float(input("Precio: "))
        cantidad = int(input("Cantidad en stock: "))
    except ValueError:
        print("Precio y cantidad deben ser numéricos.")
        return
    categoria = input("Categoría: ")

    producto = {
        "nombre": nombre,
        "codigo": codigo,
        "precio": precio,
        "cantidad": cantidad,
        "categoria": categoria
    }
    inventario.append(producto)
    print("Producto agregado.")

def buscar_producto():
    print("\n--- Buscar Producto ---")
    print("1. Por nombre (wildcards)")
    print("2. Por código (wildcards)")
    print("3. Por categoría")
    print("4. Por rango de precios")
    opcion = input("Seleccione una opción: ")

    resultados = []
    if opcion == "1":
        patron = input("Nombre (usa * o ? como comodines): ").lower()
        resultados = [p for p in inventario if fnmatch.fnmatch(p["nombre"].lower(), patron)]
    elif opcion == "2":
        patron = input("Código (usa * o ? como comodines): ").lower()
        resultados = [p for p in inventario if fnmatch.fnmatch(p["codigo"].lower(), patron)]
    elif opcion == "3":
        categoria = input("Categoría: ").lower()
        resultados = [p for p in inventario if p["categoria"].lower() == categoria]
    elif opcion == "4":
        try:
            min_precio = float(input("Precio mínimo: "))
            max_precio = float(input("Precio máximo: "))
            resultados = [p for p in inventario if min_precio <= p["precio"] <= max_precio]
        except ValueError:
            print("Entrada no válida.")
            return
    else:
        print("Opción inválida.")
        return

    if resultados:
        print(f"\n{len(resultados)} producto(s) encontrado(s):")
        for idx, p in enumerate(resultados, 1):
            print(f"{idx}. {p}")
    else:
        print("No se encontraron productos.")

def actualizar_producto():
    print("\n--- Actualizar Producto ---")
    codigo = input("Ingrese el código del producto a actualizar: ").strip().lower()
    producto = next((p for p in inventario if p["codigo"].lower() == codigo), None)
    if not producto:
        print("Producto no encontrado.")
        return

    print(f"Producto actual: {producto}")
    campos = ["nombre", "codigo", "precio", "cantidad", "categoria"]
    for campo in campos:
        nuevo_valor = input(f"Nuevo {campo} (dejar en blanco para mantener '{producto[campo]}'): ")
        if nuevo_valor:
            if campo == "precio":
                producto[campo] = float(nuevo_valor)
            elif campo == "cantidad":
                producto[campo] = int(nuevo_valor)
            else:
                producto[campo] = nuevo_valor
    print("Producto actualizado.")

def agregar_stock():
    print("\n--- Agregar Cantidad al Inventario ---")
    codigo = input("Ingrese el código del producto: ").strip().lower()
    producto = next((p for p in inventario if p["codigo"].lower() == codigo), None)

    if not producto:
        print("Producto no encontrado.")
        return

    try:
        cantidad_extra = int(input(f"Cantidad a agregar al producto '{producto['nombre']}': "))
        if cantidad_extra < 0:
            print("No se puede agregar una cantidad negativa.")
            return
    except ValueError:
        print("Debe ingresar un número entero válido.")
        return

    producto["cantidad"] += cantidad_extra
    print(f"Stock actualizado. Nueva cantidad: {producto['cantidad']}")

def eliminar_producto():
    print("\n--- Eliminar Producto ---")
    campo = input("Eliminar por (nombre, código o categoría): ").strip().lower()
    valor = input(f"Ingrese el valor de {campo}: ").strip().lower()
    coincidencias = [p for p in inventario if p[campo].lower() == valor]
    if not coincidencias:
        print("No se encontraron productos.")
        return

    print("Productos encontrados:")
    for i, p in enumerate(coincidencias, 1):
        print(f"{i}. {p}")

    confirm = input("¿Eliminar estos productos? (s/n): ")
    if confirm.lower() == "s":
        for p in coincidencias:
            inventario.remove(p)
        print("Producto(s) eliminado(s).")

def analizar_inventario():
    print("\n--- Análisis del Inventario ---")
    total_productos = len(inventario)
    valor_total = sum(p["precio"] * p["cantidad"] for p in inventario)
    categorias = {}
    bajo_stock = []

    umbral = int(input("Definir umbral para bajo stock: "))
    for p in inventario:
        cat = p["categoria"]
        categorias[cat] = categorias.get(cat, 0) + 1
        if p["cantidad"] < umbral:
            bajo_stock.append(p)

    print(f"Total de productos: {total_productos}")
    print(f"Valor total del inventario: ${valor_total:.2f}")
    print("Cantidad por categoría:")
    for cat, cantidad in categorias.items():
        print(f"  {cat}: {cantidad}")
    if bajo_stock:
        print("Productos con bajo stock:")
        for p in bajo_stock:
            print(f"  {p['nombre']} - {p['cantidad']} unidades")

def exportar_csv():
    with open("inventario.csv", "w", newline="", encoding="utf-8") as archivo_csv:
        campos = ["nombre", "codigo", "precio", "cantidad", "categoria"]
        writer = csv.DictWriter(archivo_csv, fieldnames=campos)
        writer.writeheader()
        writer.writerows(inventario)
    print("Exportado a 'inventario.csv'.")

def mostrar_ordenado():
    print("\n--- Mostrar Inventario Ordenado ---")
    print("1. Ordenar por nombre")
    print("2. Ordenar por categoría")
    print("3. Ordenar por precio")
    print("4. Ordenar por cantidad")
    opcion = input("Seleccione una opción de ordenamiento: ")

    clave = ""
    if opcion == "1":
        clave = "nombre"
    elif opcion == "2":
        clave = "categoria"
    elif opcion == "3":
        clave = "precio"
    elif opcion == "4":
        clave = "cantidad"
    else:
        print("Opción inválida.")
        return

    productos_ordenados = sorted(inventario, key=lambda x: x[clave])
    print(f"\nInventario ordenado por {clave}:\n")
    for idx, prod in enumerate(productos_ordenados, start=1):
        print(f"{idx}. {prod['nombre']} | Código: {prod['codigo']} | Precio: ${prod['precio']} | "
              f"Stock: {prod['cantidad']} | Categoría: {prod['categoria']}")

# ------------------ Menú Principal ------------------

def menu():
    cargar_inventario()
    while True:
        print("\n--- Sistema de Gestión de Inventario ---")
        print("1. Agregar producto")
        print("2. Buscar producto")
        print("3. Actualizar producto")
        print("4. Agregar stock por código")
        print("5. Eliminar producto")
        print("6. Análisis del inventario")
        print("7. Exportar a CSV")
        print("8. Mostrar inventario ordenado")
        print("9. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            agregar_producto()
        elif opcion == "2":
            buscar_producto()
        elif opcion == "3":
            actualizar_producto()
        elif opcion == "4":
            agregar_stock()
        elif opcion == "5":
            eliminar_producto()
        elif opcion == "6":
            analizar_inventario()
        elif opcion == "7":
            exportar_csv()
        elif opcion == "8":
            mostrar_ordenado()
        elif opcion == "9":
            guardar_inventario()
            print("Inventario guardado. Saliendo del programa...")
            break
        else:
            print("Opción inválida.")

# ------------------ Ejecutar ------------------

if __name__ == "__main__":
    menu()
