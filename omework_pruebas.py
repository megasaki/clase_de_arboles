
from collections import deque
from typing import Optional, List, Any

class NodoArbol:
    def __init__(self, valor: Any):
        self.valor = valor
        self.izquierdo: Optional['NodoArbol'] = None
        self.derecho: Optional['NodoArbol'] = None

class ArbolBinarioBusqueda:
    def __init__(self):
        self.raiz: Optional[NodoArbol] = None

    def insertar(self, valor: Any) -> None:
        if self.raiz is None:
            self.raiz = NodoArbol(valor)
        else:
            self._insertar_recursivo(self.raiz, valor)

    def _insertar_recursivo(self, nodo_actual: NodoArbol, valor: Any) -> None:
        if valor < nodo_actual.valor:
            if nodo_actual.izquierdo is None:
                nodo_actual.izquierdo = NodoArbol(valor)
            else:
                self._insertar_recursivo(nodo_actual.izquierdo, valor)
        elif valor > nodo_actual.valor:
            if nodo_actual.derecho is None:
                nodo_actual.derecho = NodoArbol(valor)
            else:
                self._insertar_recursivo(nodo_actual.derecho, valor)

    def inorden(self) -> List[Any]:
        resultado: List[Any] = []
        self._inorden_rec(self.raiz, resultado)
        return resultado

    def _inorden_rec(self, nodo: Optional[NodoArbol], resultado: List[Any]) -> None:
        if nodo is not None:
            self._inorden_rec(nodo.izquierdo, resultado)
            resultado.append(nodo.valor)
            self._inorden_rec(nodo.derecho, resultado)

    def mostrar_arbol(self) -> None:
        self._imprimir_nodo(self.raiz, "", True)

    def _imprimir_nodo(self, nodo: Optional[NodoArbol], prefijo: str, es_izquierdo: bool) -> None:
        if nodo is not None:
            self._imprimir_nodo(nodo.derecho, prefijo + ("|   " if es_izquierdo else "    "), False)
            print(prefijo + ("\\-- " if es_izquierdo else "/-- ") + str(nodo.valor))
            self._imprimir_nodo(nodo.izquierdo, prefijo + ("    " if es_izquierdo else "|   "), True)

    # --- TAREA 1: ELIMINAR NODO ---
    def eliminar(self, valor: Any) -> None:
        self.raiz = self._eliminar_rec(self.raiz, valor)

    def _eliminar_rec(self, nodo: Optional[NodoArbol], valor: Any) -> Optional[NodoArbol]:
        if nodo is None:
            return None
            
        if valor < nodo.valor:
            nodo.izquierdo = self._eliminar_rec(nodo.izquierdo, valor)
        elif valor > nodo.valor:
            nodo.derecho = self._eliminar_rec(nodo.derecho, valor)
        else:
            if nodo.izquierdo is None:
                return nodo.derecho
            if nodo.derecho is None:
                return nodo.izquierdo
                
            sucesor = self._min_nodo(nodo.derecho)
            nodo.valor = sucesor.valor
            nodo.derecho = self._eliminar_rec(nodo.derecho, sucesor.valor)
            
        return nodo

    def _min_nodo(self, nodo: NodoArbol) -> NodoArbol:
        actual = nodo
        while actual.izquierdo is not None:
            actual = actual.izquierdo
        return actual

    # --- TAREA 2: RECORRIDO POR NIVELES (BFS) ---
    def por_niveles(self) -> List[Any]:
        if self.raiz is None:
            return []
            
        resultado = []
        cola = deque([self.raiz])
        
        while cola:
            nodo = cola.popleft()
            resultado.append(nodo.valor)
            
            if nodo.izquierdo is not None:
                cola.append(nodo.izquierdo)
            if nodo.derecho is not None:
                cola.append(nodo.derecho)
                
        return resultado

    # --- TAREA 3: SUMA DE ELEMENTOS ---
    def suma_elementos(self) -> int:
        return self._suma_rec(self.raiz)

    def _suma_rec(self, nodo: Optional[NodoArbol]) -> int:
        if nodo is None:
            return 0
        return nodo.valor + self._suma_rec(nodo.izquierdo) + self._suma_rec(nodo.derecho)

    # --- TAREA 4: ES COMPLETO ---
    def es_completo(self) -> bool:
        return self._es_completo_rec(self.raiz)

    def _es_completo_rec(self, nodo: Optional[NodoArbol]) -> bool:
        if nodo is None:
            return True
        if nodo.izquierdo is None and nodo.derecho is None:
            return True
            
        if nodo.izquierdo is not None and nodo.derecho is not None:
            return self._es_completo_rec(nodo.izquierdo) and self._es_completo_rec(nodo.derecho)
            
        return False

# --- TAREA 5: BALANCEAR UN ÁRBOL DEGENERADO ---
def construir_arbol_balanceado(valores: List[Any]) -> Optional[NodoArbol]:
    if not valores:
        return None
        
    medio = len(valores) // 2
    nodo = NodoArbol(valores[medio])
    nodo.izquierdo = construir_arbol_balanceado(valores[:medio])
    nodo.derecho = construir_arbol_balanceado(valores[medio + 1:])
    return nodo

def balancear_arbol(bst_original: ArbolBinarioBusqueda) -> ArbolBinarioBusqueda:
    valores_ordenados = bst_original.inorden() 
    
    nuevo_bst = ArbolBinarioBusqueda()
    nuevo_bst.raiz = construir_arbol_balanceado(valores_ordenados)
    return nuevo_bst

# ==========================================
# BLOQUE DE PRUEBAS
# ==========================================
if __name__ == "__main__":
    print("--- INICIANDO PRUEBAS DEL BST ---")
    
    arbol = ArbolBinarioBusqueda()
    for val in [10, 20, 30, 40, 50, 60, 70]:
        arbol.insertar(val)
        
    print("\n1. Árbol Degenerado Original:")
    arbol.mostrar_arbol()
    
    print("\n2. Balanceando el árbol (Tarea 5):")
    arbol_balanceado = balancear_arbol(arbol)
    arbol_balanceado.mostrar_arbol()
    
    print(f"\n3. Recorrido por niveles / BFS (Tarea 2): {arbol_balanceado.por_niveles()}")
    print(f"4. Suma de elementos (Tarea 3): {arbol_balanceado.suma_elementos()}")
    print(f"5. ¿Es completo? (Tarea 4): {arbol_balanceado.es_completo()}")
    
    print("\n6. Eliminando la raíz (40) (Tarea 1):")
    arbol_balanceado.eliminar(40)
    arbol_balanceado.mostrar_arbol()