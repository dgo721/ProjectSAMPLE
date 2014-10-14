#Cubo semantico, estructura de llave y lista
#Llave corresponde a par de operadores (Ej. 00 - entero, entero; 12 - flotante, boleano)
#Lista corresponde a un valor entre 0 y 1 (operacion permitida / no permitida)
#Orden de operandos: 
#            0   1   2   3   4   5   6   7   8   9  10  11
#            +   -   *   /   <   >  <=  >=  ==  <> and  or
cubo = {00:[ 0,  0,  0,  0,  2,  2,  2,  2,  2,  2, -1, -1], #Entero-Entero
		01:[ 1,  1,  1,  1,  2,  2,  2,  2,  2,  2, -1, -1], #Entero-Flotante
		02:[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], #Entero-Boleano
		10:[ 1,  1,  1,  1,  2,  2,  2,  2,  2,  2, -1, -1], #Flotante-Entero
		11:[ 1,  1,  1,  1,  2,  2,  2,  2,  2,  2, -1, -1], #Flotante-Entero
		12:[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], #Flotante-Entero
		20:[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], #Boleano-Entero
		21:[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], #Boleano-Flotante
	    22:[-1, -1, -1, -1, -1, -1, -1, -1,  2,  2,  2,  2]} #Boleano-Boleano

#Recibe los dos tipos de operando a comparar con el operador recibido.
def semant_oper(operando1, operando2, oper):
	if (operando1==0 and operando2==0):
		llave = 00
	elif (operando1==0 and operando2==1):
		llave = 01
	elif (operando1==0 and operando2==2):
		llave = 02
	elif (operando1==1 and operando2==0):
		llave = 10
	elif (operando1==1 and operando2==1):
		llave = 11
	elif (operando1==1 and operando2==2):
		llave = 12
	elif (operando1==2 and operando2==0):
		llave = 20
	elif (operando1==2 and operando2==1):
		llave = 21
	elif (operando1==2 and operando2==2):
		llave = 22

	return cubo[llave][oper]

#print "Operacion encontrada", semant_oper(0,0,4) #Flotante, Flotante, AND
