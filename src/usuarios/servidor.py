# -*- coding: iso8859-1 -*-
from uuid import uuid4

from datetime import timedelta
from flask import Flask, jsonify, abort, make_response, request
from apresentacao import UsuarioController, ErroDeController
from base import sessao, DaoUsuario
from servico import ServicoUsuario
from flask_jwt import JWT, jwt_required

import ssl

from mensagens import *

app = Flask(__name__)

dao_usuario = DaoUsuario(sessao)

servico_usuario = ServicoUsuario(dao_usuario)

usuario_controller = UsuarioController(servico_usuario)

app.config['SECRET_KEY'] = str(uuid4())
app.config['JWT_AUTH_URL_RULE'] = '/api/usuario/login'
app.config['JWT_AUTH_USERNAME_KEY'] = 'email'
app.config['JWT_AUTH_PASSWORD_KEY'] = 'senha'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(0, 0, 0, 0, 1, 0, 0)


def autenticar(email, senha):
    try:
        usuario, telefones = servico_usuario.logar(email, senha)
    except:
        return None
    return usuario


def identidade(pacote_dados):
    usuario, telefones = servico_usuario.obter(pacote_dados['identity'])
    return usuario

jwt = JWT(app, autenticar, identidade)


@jwt.jwt_error_handler
def erro_autenticacao(e):
    if e.message == 'Invalid Token':
        return jsonify({"mensagem": to_utf8(MSG_401_B)}), 403
    return jsonify({"mensagem": to_utf8(MSG_401_A)}), 401


@jwt.auth_response_handler
def fazer_handler(token, usuario):
    usuario.token = token
    servico_usuario.atualizar_token(usuario.id, token)
    telefones = servico_usuario.buscar_telefones(usuario.id)
    representacao = usuario_controller \
        .nova_representacao_usuario(usuario, telefones)

    def handler():
        return jsonify(representacao), 200
    return handler()


@app.route("/api")
def index():
    return jsonify({"mensagem": "Desafio Python ReST"})


@app.route("/api/usuario", methods=['POST'])
def adicionar_usuario():
    try:
        representacao = usuario_controller.adicionar(request.json)
        return make_response(jsonify(representacao), 201)
    except ErroDeController as e:
        abort(e.codigo, {'mensagem': e.message})


@app.route("/api/usuario/<int:id_usuario>", methods=['GET'])
@jwt_required()
def obter_usuario(id_usuario):
    try:
        representacao = usuario_controller.obter(id_usuario)
        return jsonify(representacao)
    except ErroDeController as e:
        abort(e.codigo, {'mensagem': e.message})


@app.errorhandler(400)
def erro_documento_invalido(erro):
    mensagem = erro.description['mensagem']
    return make_response(jsonify({'mensagem': mensagem}), 400)


@app.errorhandler(401)
def erro_nao_autorizado(erro):
    mensagem = erro.description['mensagem']
    return make_response(jsonify({'mensagem': mensagem}), 401)


@app.errorhandler(404)
def erro_nao_encontrado(erro):
    mensagem = erro.description['mensagem']
    return make_response(jsonify({'mensagem': mensagem}), 404)


@app.errorhandler(405)
def erro_nao_encontrado(erro):
    return make_response(jsonify({'mensagem': to_utf8(MSG_405)}), 404)


@app.errorhandler(409)
def erro_conflito(erro):
    mensagem = erro.description['mensagem']
    return make_response(jsonify({'mensagem': mensagem}), 409)


@app.errorhandler(500)
def erro_interno(erro):
    return make_response(jsonify({'mensagem': to_utf8(MSG_500)}), 500)


if __name__ == "__main__":
    #ssl.SSLContext(ssl._SSLv2_IF_EXISTS)
    app.run(debug=True)
