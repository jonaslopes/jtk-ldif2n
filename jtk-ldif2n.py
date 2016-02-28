#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Copyright (c) 2011-2016, JONAS LOPES
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that
# the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the
# following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys
import os
import logging
import datetime
import json
import csv

APPLICATION_PATH = os.path.dirname(os.path.realpath(__file__))
log_folder = APPLICATION_PATH+"/log"

date_log = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
date_ansi = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
date_human = datetime.datetime.now().strftime("%d/-%m/%Y %H:%M:%S")

output_type = ['csv','json','screen']
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
if interactive:
	consoleHandler = logging.StreamHandler()
	consoleHandler.setFormatter(logFormatter)
	Logger.addHandler(consoleHandler)

version = "1.0"
python_version = "2.7.x"
author = "Jonas Lopes"
release_date = "2011-07-24"
description = "Programa de extração de dados LDIF para Ns formatos"

infoPrereq = """
	Pré-requisitos:
		- Python %s
		- É necessário ter a Lib Python-LDAP instalada (http://python-ldap.sourceforge.net)""" % python_version

infoRequiredEntry = """
	Entrada obrigatórias:
		-s 		- Arquivo fonte LDIF
		-g 		- Termo que determinará o grupo de separação dos dados
"""

infoEntryNotRequired = """
	Opções de entrada:
		-i		- Exibe mensagens de status de execuação do script
		--help		- Exibe as informações de uso
		--vertsion	- Exibe a versão do script
		-o		- Tipo de arquivo de saída [CSV | JSON | SCREEN]
"""

infoOptions = """
	%s

	%s

	Ex:
		python jkt-ldif2n.py [-g <grupo> | -q | --help | -o <csv | json | screen>]
		python jkt-ldif2n.py -g uid -o json
	""" % (infoRequiredEntry, infoEntryNotRequired)

infoVersion = "JTK - JON TOOLKIT - jtk-ldif2n %s-RELEASE %s %s" % (version, release_date, APPLICATION_PATH)

infoSintaxe = """$ python jkt-ldif2n.py [-g <grupo> | --help | -o <CSV | HTML | XML | JSON | screen>]
"""

infoId = """
	%s
	%s
	Versão: %s
	Autor: %s
	Data da Versão: %s""" % (infoVersion, description, version, author, release_date)


if any(n == '-s' for n in sys.argv) and any(n == '-g' for n in sys.argv):

	Logger.info(infoVersion)
	Logger.info(description)
	Logger.info("Autor: %s" % author)

	Logger.info("Verificando tipo de arquivo de saída que será gerado...")

	if any(n == '-o' for n in sys.argv):
		indiceArgs = sys.argv.index("-o")
		if len(sys.argv) >= indiceArgs+2:
			output = sys.argv[indiceArgs+1]
			if len(output) > 0:
				if output.lower() in output_type:
					output = output.lower()
				else:
					Logger.info('Tipo de arquivo de saída inválido. O formato padrão CSV será utilizado.')
					output = "csv"
			else:
				Logger.info('Nenhum tipo de  arquivo de saída atribuído. O formato padrão CSV será utilizado.')
	else:
		Logger.info('Nenhum tipo de  arquivo de saída especificado. O formato padrão CSV será utilizado.')


	Logger.info('Verificando o arquivo fonte...')
	indiceFile = sys.argv.index("-s")
	if len(sys.argv) >= indiceFile+2:
		file = sys.argv[indiceFile+1]
		if len(file) > 0:
			if os.path.exists(file):
				source = open(file,'r')
				reg = 0

				with open(file, "r") as ins:

					Logger.info("Verificando o delimitador que definirá um grupo de dados que determina um registro...")
					group = ""
					if any(n == '-g' for n in sys.argv):
						indiceGroup = sys.argv.index("-g")
						if len(sys.argv) >= indiceGroup+2:
							group = sys.argv[indiceGroup+1]

						Logger.info("O delimitador será: %s" % group)

						Logger.info("Definindo as colunas de registros...")
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

						Logger.info("Foram encontradas %d colunas" % len(columns))

						Logger.info("Verificando os dados dos registro...")
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


						Logger.info("Foram encontrados %d registros." % len(records))

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

						Logger.info('Arquivo gerado com sucesso!')

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
	print """
	-- LDIF2N HELP --
	%s
	%s
	%s
	""" % (infoId, infoPrereq, infoOptions)

elif any(n == '--version' for n in sys.argv):
	print infoVersion

else:
	print """
	ERRO!!!
	%s

	digite o seguinte comando para ajuda:
			$ python jtk-ldif2n.py --help
	""" % infoRequiredEntry

