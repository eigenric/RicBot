from math_eval import evaluate, ExpressionException
from sys import exit

def main():

	while True:
		try:
			resultado = evaluate(raw_input("Introduzca una expresion: "))
		except ExpressionException, e:
			print("Operacion incorrecta")
			print(e)
		except KeyboardInterrupt:
			print("\nSaliendo...")
			exit(0)
		else:
			print(resultado)

if __name__ == '__main__':
	main()