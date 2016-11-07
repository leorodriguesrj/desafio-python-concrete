# -*- coding: iso8859-1 -*-
from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy import DateTime
from sqlalchemy import exists
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

Entidade = declarative_base()


class Usuario(Entidade):
    __tablename__ = 'Usuario'
    id = Column(Integer, primary_key=True)
    nome = Column(String(80), nullable=False)
    email = Column(String(250), nullable=False)
    senha = Column(String(50), nullable=False)
    data_criacao = Column(DateTime, nullable=False)
    data_modificacao = Column(DateTime, nullable=False)
    ultimo_login = Column(DateTime, nullable=True)
    token = Column(Text, nullable=True)


class Telefone(Entidade):
    __tablename__ = 'Telefone'
    id = Column(Integer, primary_key=True)
    ddd = Column(String(2), nullable=False)
    numero = Column(String(9), nullable=False)
    id_usuario = Column(Integer, ForeignKey('Usuario.id'))
    usuario = relationship(Usuario)


motor = create_engine(
    'sqlite:///',
    encoding='ISO8859-1',
    connect_args={'check_same_thread': False},
    poolclass=StaticPool)

Entidade.metadata.create_all(motor)
Entidade.metadata.bind = motor

DBSession = sessionmaker(bind=motor)
sessao = DBSession()


class DaoUsuario(object):

    def __init__(self, sessao):
        self.__sessao = sessao

    def buscar_por_email_senha(self, email, senha):
        usuario = self.__sessao.query(Usuario).filter(
            Usuario.email == email and Usuario.senha == senha
        ).first()
        return usuario

    def buscar_telefones(self, id_usuario):
        return self.__sessao.query(Telefone) \
            .filter(Telefone.id_usuario == id_usuario).all()

    def email_existe(self, email):
        where = exists().where(Usuario.email == email)
        return self.__sessao.query(where).scalar()

    def atualizar_ultimo_login(self, id_usuario, data_e_hora):
        self.__sessao.query(Usuario) \
            .filter(Usuario.id == id_usuario) \
            .update({Usuario.ultimo_login: data_e_hora})
        self.__sessao.commit()

    def atualizar_token(self, id_usuario, token):
        self.__sessao.query(Usuario) \
            .filter(Usuario.id == id_usuario) \
            .update({Usuario.token: token})
        self.__sessao.commit()

    def adicionar_usuario(self, email, nome, senha):
        agora = datetime.now()
        usuario = Usuario(
            nome=nome,
            email=email,
            senha=senha,
            data_criacao=agora,
            data_modificacao=agora
        )
        self.__sessao.add(usuario)
        self.__sessao.commit()
        return usuario

    def adicionar_telefone(self, id_usuario, ddd, numero):
        telefone = Telefone(id_usuario=id_usuario, ddd=ddd, numero=numero)
        self.__sessao.add(telefone)
        self.__sessao.commit()
        return telefone

    def obter(self, id_usuario):
        usuario = self.__sessao.query(Usuario) \
            .filter(Usuario.id == id_usuario).first()

        if usuario is None:
            return None, None

        telefones = self.__sessao.query(Telefone) \
            .filter(Telefone.id_usuario == id_usuario).all()

        return usuario, telefones
