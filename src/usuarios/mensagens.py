# -*- coding: iso8859-1 -*-


MSG_400 = 'Formato de requisi��o inv�lida.'
MSG_401_A = 'Usu�rio e/ou senha inv�lidos.'
MSG_401_B = 'N�o autorizado.'
MSG_404 = 'Recurso n�o encontrado.'
MSG_405 = "O m�todo n�o � permitido"
MSG_409 = 'Email j� existe.'
MSG_500 = "Erro interno do servidor"

MSG_USUARIO_NAO_ENCONTRADO="O usu�rio n�o foi encontrado na base"


def to_utf8(mensagem):
    return mensagem.decode("iso8859-1").encode("utf-8")