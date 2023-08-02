import unittest
from calculadora import *

class TestCalculadora(unittest.TestCase):

    def test_suma(self):
        '''Función de prueba para la suma'''
        self.assertEqual(suma(2, 3), 5)
        self.assertEqual(suma(0, 0), 0)
        self.assertEqual(suma(-2, 2), 0)

    def test_resta(self):
        '''Función de prueba para la resta'''
        self.assertEqual(resta(5, 3), 2)
        self.assertEqual(resta(0, 0), 0)
        self.assertEqual(resta(2, 5), -3)

    def test_multiplicacion(self):
        '''Función de prueba para la multiplicación'''
        self.assertEqual(multiplicacion(2, 3), 6)
        self.assertEqual(multiplicacion(0, 5), 0)
        self.assertEqual(multiplicacion(-2, -3), 6)

    def test_division(self):
        '''Función de prueba para la división'''
        self.assertEqual(division(6, 3), 2)
        self.assertEqual(division(0, 5), 0)
        with self.assertRaises(ZeroDivisionError):
            division(10, 0)

    def test_calcular(self):
        '''Función de prueba para calcular'''
        self.assertEqual(calcular(1, 2, 3), 5)
        self.assertEqual(calcular(2, 5, 3), 2)
        self.assertEqual(calcular(3, 2, 3), 6)
        self.assertEqual(calcular(4, 6, 3), 2)
        with self.assertRaises(ValueError):
            calcular(6, 1, 1)

    def test_validar_numero(self):
        '''Función de prueba para la validación de numero'''
        self.assertEqual(validar_numero("5"), 5)
        self.assertEqual(validar_numero("2.5"), 2.5)
        with self.assertRaises(ValueError) as ve:
            validar_numero("texto")
        self.assertEqual(str(ve.exception), "Ingrese un número válido.")

    def test_validar_opcion(self):
        '''Función de prueba para la validación de opciones'''
        self.assertEqual(validar_opcion(1), 1)
        self.assertEqual(validar_opcion(4), 4)
        with self.assertRaises(ValueError) as ve:
            validar_opcion(6)
        self.assertEqual(str(ve.exception), "Opción inválida. Intente nuevamente.")

if __name__ == '__main__':
    unittest.main()