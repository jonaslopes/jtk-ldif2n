#!/usr/bin/python
# -*- coding: UTF-8 -*-

# ################################################################################################################################################# #
# 		JTK                   																			     										#
#		LDIF2N FORMATS                   																			     							#
#		Programa de extração de dados LDIF para N formatos 															     							#
#		Versão: 1.0                      																			     							#
#		Autor: Jonas Lopes																							     							#
#																													     							#
#		Pré-requisitos: Python 2.7.2																				     							#
#																													     							#
#						É necessário ter a Lib Python-LDAP instalada:												     							#
# 						http://python-ldap.sourceforge.net																 							#
#																				 									     							#
#		Entrada obrigatórias:	-s	 		- Arquivo fonte LDIF.														 							#
#								-g		 	- Termo que determinará o grupo de									 		 							#
# 											  separação dos dados.														 							#
#																																					#
# 																														 							#
#		Opções de entrada:	-i			- Exibe mensagens de status de execuação do script							     							#
#							--help		- Exibe as informações de uso												     							#
# 							-o			- Tipo de arquivo de saída [CSV | HTML | XML | SCREEN]							 							#
#																				    									 							#
#		Ex: python jtk-ldif2n.py [-g <grupo> -k <chave_grupo> -f <campo1,campo2...> | -q | --help | -o <CSV | HTML | XML | JSON | prompt>] 			#
# ################################################################################################################################################# #

import sys
import os
import logging
import datetime
import json
import csv


# FUNCOES
def infoId():
	print("JTK")
	print("LDIF2N FORMATS")
	print("Programa de extração de dados LDIF para Ns formatos".decode('utf8'))
	print("Versão: 1.0".decode('utf8'))
	print("Autor: Jonas Lopes".decode('utf8'))
	print("Data: 2011-07-23".decode('utf8'))

def infoPrereq():
	print("Pré-requisitos:".decode('utf8'))
	print("		- Python 2.7.x".decode('utf8'))
	print("		- É necessário ter a Lib Python-LDAP instalada (http://python-ldap.sourceforge.net)".decode('utf8'))

def infoOptions():
	print("Entrada obrigatórias:".decode('utf8'))
	print("		-s 		- Arquivo fonte LDIF.".decode("utf8"))
	print("		-g 		- Termo que determinará o grupo de separação dos dados.".decode('utf8'))
	print("		-k		- Chave que determina a informação que agrupará os registros.".decode('utf8'))
	print("		-d		- Campos dos registros que serão separados.".decode('utf8'))
	print
	print("Opções de entrada:".decode('utf8'))
	print("		-i			- Exibe mensagens de status de execuação do script".decode('utf8'))
	print("		--help		- Exibe as informações de uso".decode('utf8'))
	print("		-o		- Tipo de arquivo de saída [CSV | HTML | XML | JSON | SCREEN]".decode('utf8'))
	print
	print("Ex: python jkt-ldif2n.py [-g <grupo> -k <chave_grupo> -f <campo1,campo2...> | -q | --help | -o <csv | html | xml | screen>]".decode('utf8'))
	print("    python jkt-ldif2n.py -g uid -k <chave_grupo> -f <campo1,campo2...> | -q | --help | -o <csv | html | xml | screen>]".decode('utf8'))

"""
def infoVersion():
	printf("RNP - Integração Intranet e Protheus - rnp-intengracao-intranet-protheus 1.1-RELEASE " + format_usa.format(Calendar.getInstance().getTime()) + " " + PATH_APPLICATION);
"""

def info():
	print("-- LDIF2N HELP --")
	print
	infoId()
	print
	infoPrereq()
	print
	infoOptions()

APPLICATION_PATH = os.path.dirname(os.path.realpath(__file__))
log_folder = APPLICATION_PATH+"/log"

date_log = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
date_ansi = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
date_human = datetime.datetime.now().strftime("%d/-%m/%Y %H:%M:%S")

tipos = ['csv','html','screen']
output = "csv"
interactive = any(n == '-i' for n in sys.argv)
text = ""



# LOGGER
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
Logger = logging.getLogger()
Logger.setLevel(logging.INFO)
fileHandler = logging.FileHandler(log_folder+'/jtk-ldif2n_'+date_log+'.log')
fileHandler.setFormatter(logFormatter)
Logger.addHandler(fileHandler)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
Logger.addHandler(consoleHandler)

print
Logger.info("JTK")
Logger.info("LDIF2N FORMATS")
Logger.info("Programa de extração de dados LDIF para Ns formatos")
Logger.info("Versão: 1.0")
Logger.info("Autor: Jonas Lopes")
Logger.info("Data: 2011-07-24")

#if any(n == '-s' for n in sys.argv) and any(n == '-g' for n in sys.argv) and any(n == '-k' for n in sys.argv):
if any(n == '-s' for n in sys.argv):
	if interactive:
		infoId()

	if any(n == '-o' for n in sys.argv):
		indiceArgs = sys.argv.index("-o")
		if len(sys.argv) >= indiceArgs+2:
			output = sys.argv[indiceArgs+1]
			if len(output) > 0:
				if any(n == output.lower() for n in tipos):
					output = output.lower()
	else:
		Logger.info('ATENÇÃO: Tipo de arquivo de saída inválido. O formato padrão CSV será utilizado.')

	indiceFile = sys.argv.index("-s")
	if len(sys.argv) >= indiceFile+2:
		file = sys.argv[indiceFile+1]
		if len(file) > 0:
			if os.path.exists(file):
				source = open(file,'r')

				reg = 0
				#print("REGISTRO "+str(reg))
				with open(file, "r") as ins:

					# DEFINI A LINHA INICIAL QUE DETERMINA UM GRUPO
					# CASO NAO TENHA EH DEFINIDO COMO LINHA EM BRANCO
					group = ""
					if any(n == '-g' for n in sys.argv):
						indiceGroup = sys.argv.index("-g")
						if len(sys.argv) >= indiceGroup+2:
							group = sys.argv[indiceGroup+1]

						# DEFINI AS COLUNAS
						columns = []
						reg = 0
						for line in ins:
							if len(line.strip()) > 0 and group not in line:
								if ':' in line:
									if line[0] != " ":
										line_column = line[:line.index(':')]
										line_value = line[line.index(':')+1:].lstrip()

										if line_column not in columns:
											columns.append(line_column)
							else:
								if len(line.strip()) > 0 and group in line:
									reg += 1
									#print "REGISTRO: ", str(reg)

						ins.seek(0)

						# RECUPERA OS DADOS
						records = {}
						record_line = {}
						record_start = 0
						reg = 0
						mark = 0

						line_value = ""
						line_column = ""
						for line in ins:

							if group in line:
								reg += 1

								if len(record_line) > 0:
									records[reg] = record_line

								record_line = {}
								for c in columns:
									record_line[c] = ""
							else:
								if len(line.strip()) > 0:
										if ':' in line:
											if line[0] != " ":
												line_column = line[:line.index(':')]
												line_value = line[line.index(':')+1:].lstrip()

												#print "record_line['"+line_column+"']: " + record_line[line_column]
												#print "agora deve ser: " + line_value.strip().replace("\n","").replace("\t","")
												record_line[line_column] = line_value.strip().replace("\n","").replace("\t","")

												#print "RESULTADO: " + record_line[line_column]
											else:
												record_line[line_column] = line_value.strip().replace("\n","").replace("\t","")+line.strip().replace("\n","").replace("\t","")
												#print line_value.strip().replace("\n","")+line.strip().replace("\n","")
										else:
											if line[0] == " ":
												record_line[line_column] = line_value.strip().replace("\n","").replace("\t","")+line.strip().replace("\n","").replace("\t","")


						# SAIDA DOS DADOS
						if len(records) > 0:

							filename = 'jtk-ldif2n_output_'+date_log

							if output == 'csv':

								Logger.info('Gerando arquivo no formato ' + output + ' com o nome ' + filename+'.csv')

								with open(filename+'.csv', 'wb') as csvfile:
									spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
									spamwriter.writerow(columns)

									for r in records:
										val = []
										for c in columns:
											val.append(records[r][c])

										spamwriter.writerow(val)

							elif output == 'json':

								Logger.info('Gerando arquivo no formato ' + output + ' com o nome ' + filename+'.json')

								f = open(filename+'.json', 'w')
								for r in records:
									f.write(json.dumps(records[r] , sort_keys=True, indent=4, separators=(',', ': ')) + "\n")
								f.close()

							elif output == 'prompt':
								l = 0
								for r in records:
									l += 1
									print "REGISTRO " + str(l) + "#"
									for rr in records[r]:
										print "    " + rr + ": " + records[r][rr]
									print

							elif output == 'html':
								Logger.info('Gerando arquivo no formato ' + output + ' com o nome ' + filename+'.html')

								f = open(filename+'.html', 'w')

								f.write("<html> \n")
								f.write("<head><style>")
								f.write("table, th, td {border: 1px solid black; border-collapse: collapse;}")
								f.write("th {background-color: #ccc;}")
								f.write("th, td {padding: 5px; text-align: left;}")
								f.write("</style></head>")
								f.write("<body> \n")
								f.write("<h1>JTK - JON TOOLKIT - jtk-ldif2n 1.0-RELEASE</h1> \n")
								f.write("<h3>"+date_human+"</h3> \n")

								f.write("<table><tr> \n")
								for c in columns:
									f.write("<th>"+c+"</th> \n")
								f.write("</tr> \n")

								for r in records:
									f.write("<tr> \n")
									for rr in records[r]:
										f.write("<td>"+records[r][rr]+"</td> \n")
									f.write("</tr> \n")
								f.write("</table></body></html> \n")
								f.close()

						else:
							Logger.info('Nenhum registro recuperado.')

					else:
						print
						print "ERRO: Nome do grupo de separação dos dados inválido.".decode("utf8")
						print
			else:
				print
				print "ERRO: Caminho ou Arquivo inexistente.".decode("utf8")
				print
		else:
			print
			print "ERRO: Nome ou caminho do arquivo inválido.".decode("utf8")
			print

elif any(n == '--help' for n in sys.argv):
	info()

elif any(n == '--version' for n in sys.argv):
	print("JTK - JON TOOLKIT - jtk-ldif2n 1.0-RELEASE " + date_ansi + " " + APPLICATION_PATH)

else:
	print "[ Erro!!! ]"
	print "As seguintes variáveis são obrigatórias:".decode('utf8')
	print "		-s 		- Arquivo fonte LDIF.".decode('utf8')
	print "		-g 		- Termo que determinará o grupo de separação dos dados.".decode('utf8')
	print "		-k		- Chave que determina a informação que agrupará os registros.".decode('utf8')
	print "		-f		- Campos dos registros que serão separados.".decode('utf8')
	print
	print "digite o seguinte comando para ajuda:"
	print "		python jtk-ldif2n.py --help"

