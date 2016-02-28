# jtk-ldif2n
LDIF file converter for N formats


JTK - LDIF2N FORMATS
Programa de extração de dados LDIF para N formatos
Versão: 1.0
Autor: Jonas Lopes

Pré-requisitos: Python 2.7.2


Entrada obrigatórias:	-s	 		- Arquivo fonte LDIF.
                        -g		 	- Termo que determinará o grupo de
                                      separação dos dados.


Opções de entrada:	    -f			- Campos dos registros que serão
                                      separados. Se não for especificado serão todos separadados
                        -i			- Exibe mensagens de status de execuação do script
                        --help		- Exibe as informações de uso
                        --version   - Exibe a versão do script
                        -o			- Tipo de arquivo de saída [CSV | JSON | HTML | SCREEN]

Ex: python jkt-ldif2n.py [-g <grupo> -k <chave_grupo> -f <campo1,campo2...> | -q | --help | -o <CSV | HTML | XML | JSON | screen>]
