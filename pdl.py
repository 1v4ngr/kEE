import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network
import networkx as nx

def construir_dfa_kEE(S,k):
    def getSigma(L):
        """
        Función que obtiene el alfabeto de una lista de cadenas.

        Parámetros:
            lista_cadenas: lista de cadenas.

        Salida:
            alfabeto: conjunto de caracteres que forman el alfabeto de las cadenas.
        """

        alfabeto = set()
        for cadena in L:
            for caracter in cadena:
                alfabeto.add(caracter.lower())

        return alfabeto

    def prefijos(palabra):
        """
        Encuentra todos los prefijos de una palabra.

        Parámetros:
            palabra: Cadena de caracteres.

        Salida:
            Lista de tuplas que contiene los prefijos y el resto de la palabra.
        """
        resultado = []
        prefijo = ""
        for c in palabra:
            resultado.append((prefijo, palabra[len(prefijo):]))
            prefijo += c
        resultado.append((palabra, ""))
        return resultado

    def in_sigmaE(x):
        """
        Comprueba si una cadena x forma parte de Sigma*

        Parámetros:
            x (str): La palabra que se desea comprobar.
            sigma (set): El conjunto de letras con las que se desea comparar.

        Devuelve:
            bool: True si todas las letras de la palabra están en Sigma*, False si no.
        """
        if x == "": return True
        for letra in x:
            if letra not in sigma:
                return False
        return True

    def Ik(S, k):
        resultado = set()
        for w in S:
            # Primera condición (u | uv ∊ S, |u| = k-1, v ∊ Σ(S)*)
            for u,v in prefijos(w):
                if len(u) == k-1 and in_sigmaE(v):
                    resultado.add(u)
            
            # Segunda condición (x ∊ S | |x| < k-1)
            if len(w) < k-1:
                resultado.add(w)
            
        return resultado
    
    def Fk(S, k):
        resultado = set()
        for w in S:
            # Primera condición (v | uv ∊ S, |v| = k-1, v ∊ Σ(S)*)
            for u,v in prefijos(w):
                if len(v) == k-1 and in_sigmaE(v):
                    resultado.add(v)
            
            # Segunda condición (x ∊ S | |x| < k-1)
            if len(w) < k-1:
                resultado.add(w)
            
        return resultado
    
    def Tk(S, k):
        def dividir3(palabra):
            """
            Esta función devuelve una lista con todas las divisiones posibles de una palabra en tres partes, incluyendo el vacío.

            Parámetros:
                palabra: Una palabra.

            Retorno:
                Una lista con todas las divisiones posibles de la palabra.
            """

            divisiones = []
            for i in range(len(palabra) + 1):
                for j in range(i, len(palabra) + 2):
                # Dividir la palabra en tres partes
                    primera_parte = palabra[:i]
                    segunda_parte = palabra[i:j]
                    tercera_parte = palabra[j:]
                    # Agregar la división a la lista
                    divisiones.append((primera_parte, segunda_parte, tercera_parte))

            return divisiones
        resultado = set()
        for x in S:
            for u,v,w in dividir3(x):
                if len(v)==k and in_sigmaE(u) and in_sigmaE(w):
                    resultado.add(v)
        return resultado
                    
    sigma = getSigma(S)
    I, F, T = Ik(S,k), Fk(S,k), Tk(S,k)
    print(sigma,I,F,T)

    # Inicializamos AFD
    Q = set("_")
    delta = set()
    qi = "_"

    print("I:",I)
    for a in I:
        for j in range(0,len(a)):
            print(a[:j+1])
            Q.add(a[:j+1])
            delta.add((a[:j],a[j],a[:j+1]))

    for a in T:
        k = len(a)-1
        Q.add(a[1:k+1])
        delta.add((a[:k],a[k],a[1:k+1]))

    deltaN = set()
    for q1,a,q2 in delta:
        q1n,q2n = q1,q2
        if q1 == "": q1n = "_"
        if q2 == "": q2n = "_"
        deltaN.add((q1n,a,q2n))

    # The final states Qf is set to F
    Qf = F

    # Define the final DFA
    print("Delta",deltaN)
    return sigma, Q, qi, Qf, deltaN

def draw_dfa(Q, qA, FA, delta):
    net = Network(height='500px', width='100%', bgcolor='#FFFFFF', font_color='black')
    
    # Añadir todos los nodos antes de añadir las aristas
    for q in Q:
        if q != qA:
            net.add_node(q, label=q, borderWith=2,borderWidthSelected=4 ,color='red' if q in FA else 'gray')
        else:
            net.add_node(q, label=q, color='orange')
    
    
    # Añadir las aristas y asegurarse de que ambos nodos de origen y destino existan
    for src, symbol, dest in delta:
        if src in Q and dest in Q:  # Comprobar si ambos estados están en el conjunto de nodos
            net.add_edge(src, dest, label=symbol, color='blue', arrows='to')
        else:
            raise ValueError(f"La arista desde {src} hasta {dest} incluye un nodo inexistente.")
    
    # Deshabilitar el zoom en el gráfico
    options = """
    {
      "interaction":{
        "zoomView":false,
        "dragView": false
      }
    }
    """
    net.set_options(options)
    # Generar y mostrar el gráfico del DFA en un archivo HTML
    net.show('dfa.html', notebook=False)


st.write("Iván Gómez Ruiz")
st.title('Generadores de Lenguaje a través de Inferencia Gramatical')

input_usuario = st.text_input(
    "Introduce una lista de cadenas separadas por comas (,): ",
    value='abba, aaabba, bbaaa, bba')

lista_valores = input_usuario.split(',')
k = int(st.number_input("Introduce un valor para k: ",
                        format='%d', min_value = 1, 
                        value = 3))

S = [valor.strip() for valor in lista_valores]

dfa = construir_dfa_kEE(S, k)

sigma, Q, qA, FA, delta = dfa

draw_dfa(Q, qA, FA, delta)
st.write("DFA: ")
st.write(dfa)

# Use Streamlit components to render the HTML file as an iframe
HtmlFile = open('dfa.html', 'r', encoding='utf-8')
source_code = HtmlFile.read() 
components.html(source_code, height=510)

k = 3
resultado = construir_dfa_kEE(S, k)