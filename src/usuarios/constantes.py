# -*- coding: iso8859-1 -*-


MSG_400 = 'Formato de requisi��o inv�lida.'
MSG_401 = 'Credenciais inv�lidas.'
MSG_404 = 'Recurso n�o encontrado.'
MSG_405 = "O m�todo n�o � permitido"
MSG_409 = 'A requisi��o viola uma regra de neg�cio.'

MSG_USUARIO_NAO_ENCONTRADO="O usu�rio n�o foi encontrado na base"


def to_utf8(mensagem):
    return mensagem.decode("iso8859-1").encode("utf-8")