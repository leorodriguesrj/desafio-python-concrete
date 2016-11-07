# -*- coding: iso8859-1 -*-


MSG_400 = 'Formato de requisição inválida.'
MSG_401_A = 'Usuário e/ou senha inválidos.'
MSG_401_B = 'Não autorizado.'
MSG_404 = 'Recurso não encontrado.'
MSG_405 = "O método não é permitido"
MSG_409 = 'Email já existe.'
MSG_500 = "Erro interno do servidor"

MSG_USUARIO_NAO_ENCONTRADO="O usuário não foi encontrado na base"


def to_utf8(mensagem):
    return mensagem.decode("iso8859-1").encode("utf-8")