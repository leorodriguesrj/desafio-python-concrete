# -*- coding: iso8859-1 -*-

from flask import Flask, jsonify, abort, make_response, request
from apresentacao import UsuarioController, ErroDeController
from base import sessao, DaoUsuario
from servico import ServicoUsuario

import ssl

from constantes import to_utf8, MSG_405

app = Flask(__name__)

dao_usuario = DaoUsuario(sessao)

servico_usuario = ServicoUsuario(dao_usuario)

usuario_controller = UsuarioController(servico_usuario)


@app.route("/api")
def index():
    return jsonify({"mensagem": "Desafio Python ReST"})


@app.route("/api/usuario/login", methods=['POST'])
def autenticar():
    try:
        representacao = usuario_controller.login(request.json)
        return jsonify(representacao)
    except ErroDeController as e:
        abort(e.codigo, {'mensagem': e.message})


@app.route("/api/usuario", methods=['POST'])
def adicionar_usuario():
    try:
        representacao = usuario_controller.adicionar(request.json)
        return jsonify(representacao)
    except ErroDeController as e:
        abort(e.codigo, {'mensagem': e.message})


@app.route("/api/usuario/<int:id_usuario>", methods=['GET'])
def atualizar_usuario(id_usuario):
    try:
        representacao = usuario_controller.obter(id_usuario)
        return jsonify(representacao)
    except ErroDeController as e:
        abort(e.codigo, {'mensagem': e.message})


@app.route("/api/usuario/<int:id_usuario>", methods=['DELETE'])
def remover_usuario(id_usuario):
    try:
        representacao = usuario_controller.remover(id_usuario)
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
    return make_response(jsonify({'mensagem': "Erro interno do servidor"}), 500)


if __name__ == "__main__":
    #ssl.SSLContext(ssl._SSLv2_IF_EXISTS)
    app.run(debug=True)
