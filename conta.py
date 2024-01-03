# conta.py
class Conta:
    def __init__(self, user_id, email, senha, observacao=None):
        self.user_id = user_id
        self.email = email
        self.senha = senha
        self.observacao = observacao
