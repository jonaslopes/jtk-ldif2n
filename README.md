# jtk-ldif2n
#### LDIF file converter for N formats
#### Versão: 1.0

```
Copyright (c) 2011-2016, JONAS LOPES
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that
the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the
following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```


```
Pré-requisitos: Python 2.7.2

Entrada obrigatórias:
  -s	 		- Arquivo fonte LDIF.
  -g		 	- Termo que determinará o grupo de separação dos dados.

Opções de entrada:
  -f			- Campos dos registros que serão separados. Se não for especificado serão todos separadados
  - i			- Exibe mensagens de status de execuação do script
  --help		- Exibe as informações de uso
  --version   - Exibe a versão do script
  -o			- Tipo de arquivo de saída [CSV | JSON | HTML | SCREEN]

$ Ex: python jkt-ldif2n.py [-g <grupo> | --help | -o <CSV | HTML | XML | JSON | screen>]
```
