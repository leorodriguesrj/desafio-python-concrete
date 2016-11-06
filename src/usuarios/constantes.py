# -*- coding: iso8859-1 -*-


MSG_400 = 'Formato de requisição inválida.'
MSG_401 = 'Credenciais inválidas.'
MSG_404 = 'Recurso não encontrado.'
MSG_405 = "O método não é permitido"
MSG_409 = 'A requisição viola uma regra de negócio.'

MSG_USUARIO_NAO_ENCONTRADO="O usuário não foi encontrado na base"


def to_utf8(mensagem):
    return mensagem.decode("iso8859-1").encode("utf-8")