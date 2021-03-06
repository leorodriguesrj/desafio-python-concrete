# -*- coding: iso8859-1 -*-

from mensagens import *
from servico import ErroEmailRepetido, ErroCredenciaisIvalidas


class ErroDeController(Exception):
    def __init__(self, codigo, *args, **kwargs):
        super(ErroDeController, self).__init__(*args, **kwargs)
        self.__codigo = codigo

    @property
    def codigo(self):
        return self.__codigo


class UsuarioController(object):
    def __init__(self, servico_usuario):
        self.__servico_usuario = servico_usuario

    def obter(self, id_usuario):
        if id_usuario is None:
            raise ErroDeController(400, to_utf8(MSG_400))
        usuario, telefones = self.__servico_usuario.obter(id_usuario)
        if usuario is None:
            raise ErroDeController(404, to_utf8(MSG_404))
        return self.nova_representacao_usuario(usuario, telefones)

    def adicionar(self, json):
        if self.rejeitar_representacao_usuario(json):
            raise ErroDeController(400, to_utf8(MSG_400))

        email = json.get('email')
        nome = json.get('nome')
        senha = json.get('senha')
        telefones = []
        for telefone in json.get('telefones'):
            telefones.append({
                "numero": telefone.get('numero'), "ddd": telefone.get('ddd')
            })

        try:
            usuario, telefones = self.__servico_usuario.adicionar(
                email, nome, senha, telefones)
            return self.nova_representacao_usuario(usuario, telefones)
        except ErroEmailRepetido:
            raise ErroDeController(409, to_utf8(MSG_409))

    def rejeitar_representacao_login(self, json):
        if not json:
            return True
        if not self.__campos_sao_unicode(json, ['email', 'senha']):
            return True
        return False

    def rejeitar_representacao_usuario(self, json):
        if not json:
            return True
        if not self.__campos_sao_unicode(json, ['nome', 'email', 'senha']):
            return True
        if 'telefones' not in json:
            return True
        telefones = json['telefones']
        if type(telefones) != list or len(telefones) == 0:
            return True
        for telefone in telefones:
            if not self.__campos_sao_unicode(telefone, ['ddd', 'numero']):
                return True
        return False

    @staticmethod
    def nova_representacao_usuario(usuario, telefones):
        representacao = {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "telefones": [
                {"ddd": t.ddd, "numero": t.numero} for t in telefones
            ],
            "criado": usuario.data_criacao,
            "modificado": usuario.data_modificacao
        }
        if usuario.ultimo_login is not None:
            representacao['ultimo_login'] = usuario.ultimo_login
        if usuario.token is not None:
            representacao['token'] = usuario.token
        return representacao

    @staticmethod
    def __campos_sao_unicode(mapa, lisa_campos):
        for campo in lisa_campos:
            if campo not in mapa or type(mapa[campo]) != unicode:
                return False
        return True
