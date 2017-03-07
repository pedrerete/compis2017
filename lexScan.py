# coding=utf-8
#------------------------------
# scanner.py
#------------------------------
import ply.lex as lex

#lista de palabras reservadas
reserved = {
	'funcion' : 'FUNCION',
	'principal' : 'PRINCIPAL',
	'regresa' : 'REGRESA',
	'si' : 'SI',
	'sino' : 'SINO',
	'mientras' : 'MIENTRAS',
	'escribir' : 'ESCRIBIR',
	'crearArco' : 'CREARARCO',
	'crearCuadro' : 'CREARCUADRO',
	'crearTriangulo' : 'CREARTRIANGULO',
	'crearLinea' : 'CREARLINEA',
	'moverFigura': 'MOVERFIGURA',
	'rotarFigura' : 'ROTARFIGURA',
	'colorLinea' : 'COLORLINEA',
	'colorFondo' : 'COLORFONDO',
	'escalarFigura' : 'ESCALARFIGURA',
	'borrarFigura' : 'BORRARFIGURA',
	'borrar' : 'BORRAR',
	'agregarEn' : 'AGREGAREN',
	'rojo' : 'ROJO',
	'verde' : 'VERDE',
	'azul' : 'AZUL',
	'morado' : 'MORADO',
	'naranja' : 'NARANJA',
	'negro' : 'NEGRO',
	'amarillo' : 'AMARILLO',
	'entero' : 'ENTERO_RW',
	'doble' : 'DOBLE_RW',
	'listaEntero' : 'LISTAENTERO_RW',
	'listaDoble' : 'LISTADOBLE_RW',
	'boleano' : 'BOLEANO_RW',
	'void' : 'VOID_RW'
}

# Lista de tokens
tokens = [
	'PARENTESIS_IZQ',
	'PARENTESIS_DER',
	'CORCHETE_IZQ',
	'CORCHETE_DER',
	'LLAVE_IZQ',
	'LLAVE_DER',
	'COMA',
	'PUNTO_COMA',
	'AND',
	'OR',
	'MENOS',
	'MAS',
	'ENTRE',
	'POR',
	'MOD',
	'IGUAL',
	'MENOR_QUE',
	'MAYOR_QUE',
	'IGUAL_IGUAL',
	'MENOR_IGUAL',
	'MAYOR_IGUAL',
	'DIFERENTE_DE',
	'DOBLE',
	'ENTERO',	
	'ID',
	'STRING'] + list(reserved.values())

# Expresiones regulares simples
t_PARENTESIS_IZQ = r'\('
t_PARENTESIS_DER = r'\)'
t_CORCHETE_IZQ	= r'\['
t_CORCHETE_DER	= r'\]'
t_LLAVE_IZQ	= r'{'
t_LLAVE_DER	= r'}'
t_COMA 		= r','
t_PUNTO_COMA	= r';'
t_AND		= r'&&'
t_OR		= r'\|\|'
t_MENOS		= r'-'
t_MAS		= r'\+'
t_ENTRE		= r'/'
t_POR		= r'\*'
t_MOD		= r'%'
t_IGUAL 	= r'='
t_MENOR_QUE	= r'<'
t_MAYOR_QUE 	= r'>'
t_IGUAL_IGUAL	= r'=='
t_MENOR_IGUAL	= r'<='
t_MAYOR_IGUAL	= r'>='
t_DIFERENTE_DE 	= r'!='

def t_DOBLE(t):
	r'\d+\.\d+'
	t.value = float(t.value)
	return t

def t_ENTERO(t):
	r'\d+'
	t.value = int(t.value)
	return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    #Revisar palabras reservadas
    return t

def t_STRING(t):
	r'".*"'
	t.value = str(t.value)
	return t

# Numeros de linea
def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

#Ignorar todo lo demás
t_ignore  = ' \t'

#Manejar errores
def t_error(t):
    print('''Caracter no valido '%s''' % t.value[0])
    t.lexer.skip(1)

# Construir lexer
lexer = lex.lex()

# Prueba
#prueba = 'funcion principal regresa si sino mientras escribir crearArco crearCuadro crearTriangulo crearLinea moverFigura rotarFigura colorLinea colorFondo escalarFigura borrarFigura borrar agregarEn rojo verde azul morado naranja negro amarillo ( ) [ ] { } , ; && || - + / * % = < > == <= >= != 3.4 3 algo "ee"'

# Pasar la prueba
#lexer.input(prueba)

# Tokenizar
#while True:
#    tok = lexer.token()
#    if not tok: 
#        break      # No more input
#    print(tok)

import ply.yacc as yacc
import sys

# Gramatica
def p_programa(p):
	'programa : vars funciones principal'
	p[0] = 'PROGRAM COMPILED'

def p_vars(p):
	'''vars : tipo ID s1 s2 PUNTO_COMA vars
		| '''

def p_s1(p):
	'''s1 : CORCHETE_IZQ ENTERO CORCHETE_DER 
	      | '''

def p_s2(p):
	'''s2 : COMA ID s1 s2
	      | '''

def p_funciones(p):
	'''funciones : FUNCION tipoFun ID PARENTESIS_IZQ parametros PARENTESIS_DER bloqueFun funciones
		     | '''

def p_tipo(p):
	''' tipo : DOBLE_RW
		 | ENTERO_RW
		 | BOLEANO_RW
		 | LISTAENTERO_RW
		 | LISTADOBLE_RW'''

def p_tipoFun(p):
	'''tipoFun : DOBLE_RW
		   | ENTERO_RW
		   | BOLEANO_RW
		   | VOID_RW''' 

def p_principal(p):
	'principal : PRINCIPAL bloqueP'

def p_parametros(p):
	'''parametros : tipo ID s20 s3
			| '''

def p_s3(p):
	'''s3 : COMA tipo ID s1 s3
	      | '''

def p_bloqueP(p):
	'bloqueP : LLAVE_IZQ cuerpoP LLAVE_DER'

def p_bloqueFun(p):
	'bloqueFun : LLAVE_IZQ cuerpoFun LLAVE_DER'

def p_cuerpoFun(p):
	'cuerpoFun : vars estatuto s5'

def p_s5(p):
	'''s5 : REGRESA exp PUNTO_COMA
	      | '''

def p_cuerpoP(p):
	'cuerpoP : vars estatuto REGRESA exp PUNTO_COMA'

def p_bloque(p):
	'bloque : LLAVE_IZQ cuerpo LLAVE_DER'

def p_cuerpo(p):
	'''cuerpo : estatuto
		  | '''

def p_estatuto(p):
	'''estatuto : asignacion estatuto
		    | condicion estatuto
		    | ciclo estatuto
		    | escribir estatuto
		    | llamarVoid estatuto
		    | predefinido estatuto
		    | '''

def p_asignacion(p):
	'asignacion : ID s20 IGUAL expresion PUNTO_COMA'

def p_condicion(p):
	'condicion : SI PARENTESIS_IZQ expresion PARENTESIS_DER bloque s6'

def p_s6(p):
	'''s6 : SINO bloque
	    | '''

def p_ciclo(p):
	'ciclo : MIENTRAS PARENTESIS_IZQ expresion PARENTESIS_DER bloque'

def p_escribir(p):
	'escribir : ESCRIBIR PARENTESIS_IZQ s7 s8 PARENTESIS_DER PUNTO_COMA'

def p_s7(p):
	'''s7 : STRING
	      | exp'''

def p_s8(p):
	'''s8 : MAS s7 s8
	      | '''

def p_llamarFuncion(p):
	'llamarFuncion : ID PARENTESIS_IZQ args PARENTESIS_DER'

def p_llamarVoid(p):
	'llamarVoid : ID PARENTESIS_IZQ args PARENTESIS_DER'

def p_args(p):
	'''args : exp s9
		| '''

def p_s9(p):
	'''s9 : COMA args
	      | '''

def p_predefinido(p):
	'''predefinido : crearArco
			| crearCuadro
			| crearLinea
			| crearTriangulo
			| moverFigura
			| rotarFigura
			| colorLinea
			| colorFondo
			| escalarFigura
			| borrarFigura
			| agregarEn
			| borrar'''

def p_expresion(p):
	'expresion : comparacion s10'

def p_s10(p):
	'''s10 : OR s11
		| AND s11
		| '''

def p_s11(p):
	's11 : expresion'

def p_comparacion(p):
	'comparacion : exp s12'

def p_s12(p):
	'''s12 : operador comparacion
		| '''

def p_exp(p):
	'exp : termino s13'

def p_s13(p):
	'''s13 : MAS s14
		| MENOS s14
		| '''

def p_s14(p):
	's14 : exp'

def p_termino(p):
	'termino : factor s15'

def p_s15(p):
	'''s15 : ENTRE s16
		| POR s16
		| MOD s16
		| '''

def p_s16(p):
	's16 : termino'

def p_factor(p):
	'''factor : llamarFuncion
		  | s17
		  | ENTERO
		  | DOBLE
		  | PARENTESIS_IZQ exp PARENTESIS_DER'''

def p_s17(p):
    's17 : ID s20'

def p_operador(p):
    '''operador : MENOR_QUE
            | MAYOR_QUE
            | IGUAL_IGUAL
            | MENOR_IGUAL
            | MAYOR_IGUAL
            | DIFERENTE_DE'''

def p_crearArco (p):
    'crearArco : CREARARCO baseFigura'

def p_crearCuadro (p):
	'crearCuadro : CREARCUADRO baseFigura'

def p_crearTriangulo (p): 
    'crearTriangulo : CREARTRIANGULO baseFigura'

def p_crearLinea(p):
    'crearLinea : CREARLINEA PARENTESIS_IZQ ID COMA exp COMA exp PARENTESIS_DER PUNTO_COMA'

def p_baseFigura(p):
    'baseFigura : PARENTESIS_IZQ ID COMA exp COMA exp COMA exp COMA exp COMA color PARENTESIS_DER PUNTO_COMA'

def p_moverFigura (p):
    'moverFigura : MOVERFIGURA PARENTESIS_IZQ ID COMA exp COMA exp PARENTESIS_DER PUNTO_COMA'

def p_rotarFigura(p):
    'rotarFigura : ROTARFIGURA PARENTESIS_IZQ baseTransformar PARENTESIS_DER PUNTO_COMA'

def p_colorLinea(p):
    'colorLinea : COLORLINEA baseColor'

def p_colorFondo(p):
    'colorFondo : COLORFONDO baseColor'

def p_baseColor(p):
    'baseColor : PARENTESIS_IZQ ID COMA color PARENTESIS_DER PUNTO_COMA'

def p_escalarFigura(p):
    'escalarFigura : ESCALARFIGURA baseTransformar'

def p_baseTransformar(p):
    'baseTransformar : PARENTESIS_IZQ ID COMA exp PARENTESIS_DER PUNTO_COMA'

def p_borrarFigura(p):
    'borrarFigura : BORRARFIGURA PARENTESIS_IZQ ID PARENTESIS_DER PUNTO_COMA'

def p_borrar(p):
    'borrar : BORRAR baseTransformar'

def p_agregaEn(p): 
    'agregarEn : AGREGAREN PARENTESIS_IZQ ID COMA exp COMA exp PARENTESIS_DER PUNTO_COMA'

def p_color(p):
    '''color : ROJO
        | VERDE
        | AZUL
        | MORADO
        | NARANJA
        | NEGRO
        | AMARILLO'''

def p_s20(p):
	'''s20 : CORCHETE_IZQ exp CORCHETE_DER
		| '''

# Manejar errores
def p_error(p):
	print "Linea {1}: Mala sintaxis en la entrada en '{0}'".format(p.value, lexer.lineno)

# Construir el parser
parser = yacc.yacc()


# Main
if __name__ == '__main__':
  if (len(sys.argv) > 1):
    file = sys.argv[1]
    # Abrir archivo, almacenar informacion y cerrarlo
    try:
      f = open(file,'r')
      data = f.read()
      f.close()
      if (parser.parse(data, tracking=True) == 'PROGRAM COMPILED'): 
	print("Buena sintaxis!")

    except EOFError:
      print(EOFError)
  else:
    print('File missing')
