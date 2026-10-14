
"""
Mini-Proyecto: Diccionario Inteligente con BST
Implementación de un sistema de autocompletado y diccionario utilizando 
un Árbol Binario de Búsqueda para almacenar objetos Palabra.
"""

import unicodedata
from typing import Optional, List

def normalizar(texto: str) -> str:
    """
    Convierte el texto a minúsculas y elimina tildes/diacríticos.
    Garantiza que el BST se ordene correctamente sin importar los acentos.
    """
    texto = texto.lower().strip()
    return ''.join(c for c in unicodedata.normalize('NFD', texto) 
                if unicodedata.category(c) != 'Mn') # CORREGIDO: Indentación alineada con la línea superior

class Palabra:
    """Representa una palabra y su definición en el diccionario."""
    def __init__(self, texto: str, definicion: str):
        self.texto_original = texto.strip()
        # texto_busqueda se usa exclusivamente para las comparaciones del árbol
        self.texto_busqueda = normalizar(texto)
        self.definicion = definicion.strip()
        
    def __lt__(self, otra: 'Palabra') -> bool:
        return self.texto_busqueda < otra.texto_busqueda

    def __gt__(self, otra: 'Palabra') -> bool:
        return self.texto_busqueda > otra.texto_busqueda
        
    def __eq__(self, otra: object) -> bool:
        if not isinstance(otra, Palabra):
            return NotImplemented
        return self.texto_busqueda == otra.texto_busqueda
        
    def empieza_con(self, prefijo: str) -> bool:
        """Verifica si la palabra comienza con el prefijo dado de forma normalizada."""
        prefijo_norm = normalizar(prefijo)
        return self.texto_busqueda.startswith(prefijo_norm)

    def __str__(self) -> str:
        return f"{self.texto_original}: {self.definicion}"


class NodoDiccionario:
    """Nodo del árbol que contiene un objeto Palabra."""
    def __init__(self, palabra: Palabra):
        self.palabra = palabra
        self.izquierdo: Optional['NodoDiccionario'] = None
        self.derecho: Optional['NodoDiccionario'] = None


class ArbolDiccionario:
    """Árbol Binario de Búsqueda adaptado para almacenar y buscar Palabras."""
    def __init__(self):
        self.raiz: Optional[NodoDiccionario] = None

    def insertar(self, texto: str, definicion: str) -> None:
        """Inserta una nueva palabra en el diccionario."""
        nueva_palabra = Palabra(texto, definicion)
        if self.raiz is None:
            self.raiz = NodoDiccionario(nueva_palabra)
        else:
            self._insertar_recursivo(self.raiz, nueva_palabra)

    def _insertar_recursivo(self, nodo_actual: NodoDiccionario, nueva_palabra: Palabra) -> None:
        if nueva_palabra < nodo_actual.palabra:
            if nodo_actual.izquierdo is None:
                nodo_actual.izquierdo = NodoDiccionario(nueva_palabra)
            else:
                self._insertar_recursivo(nodo_actual.izquierdo, nueva_palabra)
        elif nueva_palabra > nodo_actual.palabra:
            if nodo_actual.derecho is None:
                nodo_actual.derecho = NodoDiccionario(nueva_palabra)
            else:
                self._insertar_recursivo(nodo_actual.derecho, nueva_palabra)
        else:
            # Si la palabra ya existe, actualiza la definición
            nodo_actual.palabra.definicion = nueva_palabra.definicion

    def buscar_exacta(self, texto: str) -> Optional[str]:
        """Busca una palabra exacta y retorna su definición, o None si no existe."""
        texto_buscado = normalizar(texto)
        nodo = self._buscar_recursivo(self.raiz, texto_buscado)
        return nodo.palabra.definicion if nodo else None

    def _buscar_recursivo(self, nodo_actual: Optional[NodoDiccionario], texto: str) -> Optional[NodoDiccionario]:
        if nodo_actual is None:
            return None
            
        if texto == nodo_actual.palabra.texto_busqueda:
            return nodo_actual
        elif texto < nodo_actual.palabra.texto_busqueda:
            return self._buscar_recursivo(nodo_actual.izquierdo, texto)
        else:
            return self._buscar_recursivo(nodo_actual.derecho, texto)

    def buscar_por_prefijo(self, prefijo: str) -> List[Palabra]:
        """Retorna una lista de todas las palabras que comienzan con el prefijo dado."""
        resultados: List[Palabra] = []
        if not prefijo.strip():
            return resultados
            
        self._buscar_prefijo_recursivo(self.raiz, normalizar(prefijo), resultados)
        return resultados

    def _buscar_prefijo_recursivo(self, nodo_actual: Optional[NodoDiccionario], prefijo: str, resultados: List[Palabra]) -> None:
        if nodo_actual is None:
            return

        texto_nodo = nodo_actual.palabra.texto_busqueda

        # Si hay coincidencia, exploramos en In-Orden para mantener el orden alfabético estricto
        if nodo_actual.palabra.empieza_con(prefijo):
            self._buscar_prefijo_recursivo(nodo_actual.izquierdo, prefijo, resultados)
            resultados.append(nodo_actual.palabra)
            self._buscar_prefijo_recursivo(nodo_actual.derecho, prefijo, resultados)
        
        # Si el nodo es lexicográficamente menor que el prefijo, las coincidencias están a la derecha
        elif texto_nodo < prefijo:
            self._buscar_prefijo_recursivo(nodo_actual.derecho, prefijo, resultados)
            
        # Si el nodo es mayor, las coincidencias están a la izquierda
        else:
            self._buscar_prefijo_recursivo(nodo_actual.izquierdo, prefijo, resultados)

    def inorden(self) -> List[Palabra]:
        """Retorna todas las palabras del diccionario ordenadas alfabéticamente."""
        resultado: List[Palabra] = []
        self._inorden_rec(self.raiz, resultado)
        return resultado

    def _inorden_rec(self, nodo: Optional[NodoDiccionario], resultado: List[Palabra]) -> None:
        if nodo is not None:
            self._inorden_rec(nodo.izquierdo, resultado)
            resultado.append(nodo.palabra)
            self._inorden_rec(nodo.derecho, resultado)

# ==========================================
# DATOS INICIALES Y CARGA
# ==========================================
def cargar_diccionario() -> ArbolDiccionario:
    diccionario = ArbolDiccionario()
    
    # Palabras iniciales desordenadas para evitar un árbol degenerado
    palabras_iniciales = [
        ("Nodo", "Elemento básico que forma parte de una estructura de datos jerárquica."),
        ("Algoritmo", "Conjunto ordenado de operaciones sistemáticas."),
        ("Polimorfismo", "Capacidad de un método u objeto de tener diferentes formas."),
        ("Bucle", "Secuencia que se repite un número de veces o hasta que se cumpla una condición."),
        ("Matriz", "Arreglo bidimensional de números u otros elementos matemáticos."),
        ("Clase", "Plantilla para la creación de objetos de datos según un modelo predefinido."),
        ("Web", "Sistema de distribución de documentos interconectados a través de Internet."),
        ("Depuración", "Proceso de identificar y corregir errores de programación."),
        ("XML", "Lenguaje de marcado extensible utilizado para almacenar y transportar datos."),
        ("Encapsulamiento", "Ocultamiento del estado de un objeto, protegiendo su integridad."),
        ("YAML", "Formato de serialización de datos legible por humanos."),
        ("Función", "Bloque de código reutilizable que realiza una tarea específica."),
        ("ZIP", "Formato de compresión de archivos sin pérdida de datos."),
        ("Grafos", "Estructura de datos no lineal que consiste en nodos (vértices) y aristas."),
        ("Array", "Estructura de datos que almacena una colección de elementos del mismo tipo."),
        ("Herencia", "Mecanismo por el cual una clase deriva de otra."),
        ("Backend", "Parte del desarrollo web encargada de la lógica de servidor."),
        ("Iteración", "Cada una de las repeticiones de un proceso."),
        ("Commit", "Acción de confirmar y guardar cambios en un control de versiones."),
        ("JSON", "Formato de texto ligero para el intercambio de datos."),
        ("Docker", "Plataforma que permite crear, probar e implementar aplicaciones."),
        ("Kernel", "Núcleo o parte central de un sistema operativo."),
        ("Entorno", "Conjunto de variables en las que se ejecuta un programa."),
        ("Lista", "Estructura de datos lineal que almacena una colección de elementos."),
        ("Framework", "Estructura conceptual de soporte para el desarrollo de software."),
        ("Objeto", "Instancia de una clase en programación orientada a objetos."),
        ("Git", "Sistema de control de versiones distribuido."),
        ("Query", "Consulta o petición de información a una base de datos."),
        ("HTML", "Lenguaje de marcado utilizado para la creación de páginas web."),
        ("Recursividad", "Propiedad de una función de llamarse a sí misma."),
        ("IDE", "Entorno de desarrollo integrado para programadores."),
        ("String", "Secuencia de caracteres utilizada para representar texto."),
        ("JavaScript", "Lenguaje de programación interpretado, utilizado en la web."),
        ("Tupla", "Estructura de datos inmutable similar a una lista."),
        ("Kotlin", "Lenguaje de programación estático que corre sobre la JVM."),
        ("UML", "Lenguaje Unificado de Modelado para especificar sistemas."),
        ("Linux", "Núcleo de sistema operativo libre y de código abierto."),
        ("Variable", "Espacio en memoria reservado para almacenar un valor."),
        ("Método", "Subrutina asociada exclusivamente a una clase o a un objeto."),
        ("Nube", "Término utilizado para describir una red mundial de servidores."),
        ("ORM", "Técnica para convertir datos utilizando bases relacionales."),
        ("Python", "Lenguaje de programación interpretado, de alto nivel."),
        ("Queue", "Cola, estructura de datos lineal que sigue el principio FIFO."),
        ("API", "Interfaz de programación de aplicaciones."),
        ("Servidor", "Programa que provee servicios a otros programas."),
        ("Token", "Cadena de caracteres con un significado de seguridad."),
        ("UI", "Interfaz de usuario, medio de interacción con un sistema."),
        ("Vista", "Representación visual en la arquitectura MVC."),
        ("WiFi", "Tecnología de comunicación inalámbrica."),
        ("Frontend", "Parte del desarrollo web que interactúa con los usuarios.")
    ]
    
    for p, d in palabras_iniciales:
        diccionario.insertar(p, d)

    return diccionario

# ==========================================
# INTERFAZ DE CONSOLA
# ==========================================
def mostrar_menu():
    print("\n" + "="*40)
    print("      DICCIONARIO INTELIGENTE (BST)     ")
    print("="*40)
    print("1. Buscar palabra exacta")
    print("2. Autocompletar (buscar por prefijo)")
    print("3. Ver diccionario completo (A-Z)")
    print("4. Agregar nueva palabra")
    print("5. Salir")
    print("="*40)

def main():
    diccionario = cargar_diccionario()
    print("Diccionario cargado con éxito. Palabras iniciales: 50")
    
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-5): ").strip()
        
        if opcion == "1":
            texto = input("\nIngrese la palabra a buscar: ").strip()
            if not texto:
                print("\n[Error] No ha ingresado ninguna palabra.")
                continue
                
            definicion = diccionario.buscar_exacta(texto)
            if definicion:
                print(f"\n[Resultado] {texto.upper()}: {definicion}")
            else:
                print(f"\n[Aviso] La palabra '{texto}' no se encuentra en el diccionario.")
                
        elif opcion == "2":
            prefijo = input("\nIngrese las primeras letras (prefijo): ").strip()
            if not prefijo:
                print("\n[Error] El prefijo no puede estar vacío.")
                continue
                
            resultados = diccionario.buscar_por_prefijo(prefijo)
            if resultados:
                print(f"\nSe encontraron {len(resultados)} palabras que comienzan con '{prefijo}':")
                for p in resultados:
                    print(f" - {p}")
            else:
                print(f"\n[Aviso] No se encontraron palabras que comiencen con '{prefijo}'.")
                
        elif opcion == "3":
            print("\nDiccionario Completo (Orden Alfabético):")
            palabras = diccionario.inorden()
            for i, p in enumerate(palabras, 1):
                print(f"{i:02d}. {p}")
                
        elif opcion == "4":
            texto = input("\nIngrese la nueva palabra: ").strip()
            if not texto:
                print("\n[Error] La palabra no puede estar vacía.")
                continue
                
            if diccionario.buscar_exacta(texto):
                print(f"\n[Aviso] La palabra '{texto}' ya existe. Su definición será actualizada.") # CORREGIDO: Indentación a 4 espacios
                
            definicion = input("Ingrese la definición: ").strip()
            if not definicion:
                print("\n[Error] La definición no puede estar vacía.")
                continue
                
            diccionario.insertar(texto, definicion)
            print("\n[Éxito] Palabra guardada correctamente.")
            
        elif opcion == "5":
            print("\nSaliendo del diccionario. Hasta luego.")
            break
            
        else:
            print("\n[Error] Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()