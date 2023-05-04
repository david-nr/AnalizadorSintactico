import ast
import tokenize
import io

def obtener_nombre_token(token):
    # Devuelve el nombre del token correspondiente al token pasado como argumento
    return tokenize.tok_name[token.type]
def obtener_mensaje_error_sintactico(error, codigo_fuente):
    # Obtener el token en el que ocurre el error
    tokens = list(tokenize.tokenize(io.BytesIO(codigo_fuente.encode('utf-8')).readline))
    indice_token_error = next(i for i, t in enumerate(tokens) if t.start[0] == error.lineno and t.start[1] <= error.offset < t.end[1])
    token_error = tokens[indice_token_error-1]

    # Buscar en los tokens cercanos para determinar qué se esperaba
    mensaje = ""
    if token_error.string == 'if':
        mensaje += ("Se esperaba una condición después del 'if'")
    elif token_error.string == ':':
        mensaje += ("Se esperaba un bloque de código después de ':'")
    elif token_error.string == ';':
        mensaje += ("Se encontró un ';' y se esperaba un salto de línea")
    elif token_error.string == ',':
        mensaje += ("Se esperaba otro argumento después de ','")
    else:
        mensaje += (f"Se encontró '{token_error.string}' y se esperaba algo diferente")
    print(mensaje)
    return mensaje


def analizador_sintactico(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        codigo_fuente = archivo.read()
        
    try:
        ast.parse(codigo_fuente)
        print("El archivo no tiene errores de sintaxis.")
    except SyntaxError as e:
        mensaje = (f"Error sintáctico en la línea {e.lineno}, columna {e.offset}: {e.text.strip()} error: {e.msg}")
        
        if("indentation level" in str(e)):
            mensaje += (" Error de identacion")
        
            
        elif(("(" in str(e.text.strip()))):
            if(")" not in str(e.text.strip())):
                mensaje += (" Falta cerrarlo con un ')'")
        
        elif((")" in str(e.text.strip()))):
            if("(" not in str(e.text.strip())):
                mensaje += (" Falta cerrarlo con un '('")
        
        elif(("[" in str(e.text.strip()))):
            if("]" not in str(e.text.strip())):
                mensaje += (" Falta cerrarlo con un ']'")
        
        elif(("]" in str(e.text.strip()))):
            if("[" not in str(e.text.strip())):
                mensaje += (" Falta cerrarlo con un '['")
        elif(("{" in str(e.text.strip()))):
            if("}" not in str(e.text.strip())):
                mensaje += (" Falta cerrarlo con un '}'")
        elif(("}" in str(e.text.strip()))):
            if("{" not in str(e.text.strip())):
                mensaje += (" Falta cerrarlo con un '{' en la linea correspondiente")
        
            
        else:
            mensaje += obtener_mensaje_error_sintactico(e, codigo_fuente)
        print(mensaje)
        return mensaje     

nombre_archivo = ("Archivo2.py")
analizador_sintactico(nombre_archivo)
