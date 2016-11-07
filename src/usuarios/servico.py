# -*- coding: iso8859-1 -*-


from datetime import datetime


class ErroCredenciaisIvalidas(Exception):
    def __init__(self, *args, **kwargs):
        super(ErroCredenciaisIvalidas, self).__init__(*args, **kwargs)


class ErroEmailRepetido(Exception):
    def __init__(self, *args, **kwargs):
        super(ErroEmailRepetido, self).__init__(*args, **kwargs)


class ServicoUsuario(object):
    def __init__(self, dao_usuario):
        self.__dao_usuario = dao_usuario

    def logar(self, email, senha):
        usuario = self.__dao_usuario.buscar_por_email_senha(email, senha)
        if usuario is None:
            raise ErroCredenciaisIvalidas()
        self.__dao_usuario.atualizar_ultimo_login(usuario.id, datetime.now())
        telefones = self.__dao_usuario.buscar_telefones(usuario.id)
        return usuario, telefones

    def adicionar(self, email, nome, senha, telefones):
        if self.__dao_usuario.email_existe(email):
            raise ErroEmailRepetido()
        usuario = self.__dao_usuario.adicionar_usuario(email, nome, senha)
        entidades_telefone = []
        for telefone in telefones:
            ddd = telefone['ddd']
            numero = telefone['numero']
            t = self.__dao_usuario.adicionar_telefone(usuario.id, ddd, numero)
            entidades_telefone.append(t)
        return usuario, entidades_telefone

    def obter(self, id_usuario):
        return self.__dao_usuario.obter(id_usuario)

    def atualizar_token(self, id_usuario, token):
        self.__dao_usuario.atualizar_token(id_usuario, token)
