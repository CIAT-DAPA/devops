def suma(a, b):
    return a + b

def resta(a, b):
    return a - b

def multiplicacion(a, b):
    return a * b

def division(a, b):
    if b == 0:
        raise ZeroDivisionError("No se puede dividir entre cero.")
    return a / b

def calcular(opcion, num1, num2):
    if opcion == 1:
        return suma(num1, num2)
    elif opcion == 2:
        return resta(num1, num2)
    elif opcion == 3:
        return multiplicacion(num1, num2)
    elif opcion == 4:
        return division(num1, num2)
    else:
        raise ValueError("Opción inválida. Intente nuevamente.")
    
def validar_numero(valor):
    try:
        return float(valor)
    except ValueError:
        raise ValueError("Ingrese un número válido.")

def validar_opcion(opcion):
    opciones_validas = [1, 2, 3, 4, 5]
    if opcion not in opciones_validas:
        raise ValueError("Opción inválida. Intente nuevamente.")
    return opcion

def calculadora():
    while True:
        try:
            print("Opciones:")
            print("1. Suma")
            print("2. Resta")
            print("3. Multiplicación")
            print("4. División")
            print("5. Salir")

            opcion = int(input("Elija una opción (1/2/3/4/5): "))
            opcion = validar_opcion(opcion)

            if opcion == 5:
                print("¡Hasta luego!")
                break

            num1 = input("Ingrese el primer número: ")
            num1 = validar_numero(num1)

            num2 = input("Ingrese el segundo número: ")
            num2 = validar_numero(num2)

            resultado = calcular(opcion, num1, num2)
            print("Resultado:", resultado)

        except Exception as ve:
            print("Error:", ve)
            print("Intente nuevamente.")

if __name__ == "__main__":
    calculadora()