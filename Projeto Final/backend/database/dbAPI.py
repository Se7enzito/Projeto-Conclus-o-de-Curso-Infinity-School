import sqlite3 as sql
import os

class GerenciamentoUsers():
    def __init__(self) -> None:
        self.database = "backend/database/database.db"
        self.connection = None
        self.cursor = None

    def conectar(self) -> None:
        self.connection = sql.connect(self.database)
        self.cursor = self.connection.cursor()

    def desconectar(self) -> None:
        self.connection.close()

    def tabelaExiste(self, nome_tabela: str) -> bool:
        self.conectar()
        consulta = self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{nome_tabela}'").fetchone()
        self.desconectar()
        
        return consulta is not None
    
    def criarTabela(self) -> None:
        if self.tabelaExiste('users'):
            return
        
        self.conectar()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user TEXT NOT NULL UNIQUE,
                                senha TEXT NOT NULL,
                                perm INTEGER NOT NULL
                            )''')
        self.cursor.execute('''INSERT INTO users (user, senha, perm) VALUES ('admin', 'admin', 3)''')
        self.connection.commit()
        self.desconectar()    
    
    def criarUser(self, user: str, senha: str, perm: int) -> list:
        if (user == "" or senha == "" or perm == None):
            return []
        
        self.conectar()
        self.cursor.execute("INSERT INTO users (user, senha, perm) VALUES (?,?,?)", (user, senha, perm))
        self.connection.commit()
        self.desconectar()
        
        return [user, senha, perm]
    
    def atualizarUser(self, user: str, senha: str, perm: int) -> list:
        if (user == ""):
            return []
        
        if (senha == ""):
            senha = self.getSenha(user)
        
        if (perm == 0 or perm == "" or perm is None):
            perm = self.getPerm(user)

        self.conectar()
        self.cursor.execute("UPDATE users SET senha =?, perm =? WHERE user =?", (senha, perm, user))
        self.connection.commit()
        self.desconectar()
        
        return [user, senha, perm]
    
    def deletarUser(self, user: str) -> bool:
        self.conectar()
        self.cursor.execute("DELETE FROM users WHERE user =?", (user,))
        self.connection.commit()
        self.desconectar()
        
        return True
    
    def getAllUsers(self) -> list:
        self.conectar()
        consulta = self.cursor.execute("SELECT * FROM users").fetchall()
        self.desconectar()
        
        return consulta
    
    def getSenha(self, user: str) -> str:
        self.conectar()
        consulta = self.cursor.execute("SELECT senha FROM users WHERE user =?", (user,)).fetchone()
        self.desconectar()
        
        if consulta:
            return consulta[0]
        else:
            return None
        
    def getPerm(self, user: str) -> int:
        self.conectar()
        consulta = self.cursor.execute("SELECT perm FROM users WHERE user =?", (user,)).fetchone()
        self.desconectar()
        
        if consulta:
            return consulta[0]
        else:
            return None 
    
    def containsUser(self, user: str) -> bool:
        self.conectar()
        consulta = self.cursor.execute("SELECT user FROM users").fetchall()
        self.desconectar()
        
        for row in consulta:
            if row[0] == user:
                return True
        
        return False

    def senhaCorreta(self, user: str, senha: str) -> bool:
        self.conectar()
        consulta = self.cursor.execute("SELECT senha FROM users WHERE user = ?", (user,)).fetchall()
        self.desconectar()
        
        if consulta and consulta[0][0] == senha:
            return True
        else:
            return False
        
class GerenciamentoObjetos():
    def __init__(self) -> None:
        self.database = "backend/database/database.db"
        self.connection = None
        self.cursor = None
        
    def conectar(self) -> None:
        self.connection = sql.connect(self.database)
        self.cursor = self.connection.cursor()

    def desconectar(self) -> None:
        self.connection.close()

    def tabelaExiste(self, nome_tabela: str) -> bool:
        self.conectar()
        consulta = self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{nome_tabela}'").fetchone()
        self.desconectar()
        
        return consulta is not None
    
    def criarTabela(self) -> None:
        if self.tabelaExiste('objeto'):
            return
        
        self.conectar()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS objeto (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                nome TEXT NOT NULL UNIQUE,
                                quantidade INTEGER NOT NULL,
                                tipo TEXT NOT NULL
                            )''')
        self.connection.commit()
        self.desconectar()    
        
    def adicionarItem(self, nome: str, quantidade: int, tipo: str) -> list:
        if (nome == "" or quantidade == 0 or tipo == ""):
            return []
        
        self.conectar()
        self.cursor.execute("INSERT INTO objeto (nome, quantidade, tipo) VALUES (?,?,?)", (nome, quantidade, tipo))
        self.connection.commit()
        self.desconectar()
        
        return [nome, quantidade, tipo]
    
    def removerItem(self, nome: str) -> bool:
        self.conectar()
        self.cursor.execute("DELETE FROM objeto WHERE nome =?", (nome,))
        self.connection.commit()
        self.desconectar()
        
        return True
    
    def getQuantidade(self, nome: str) -> int:
        self.conectar()
        consulta = self.cursor.execute("SELECT quantidade FROM objeto WHERE nome =?", (nome,)).fetchone()
        self.desconectar()
        
        if consulta:
            return consulta[0]
        else:
            return 0
        
    def getTipo(self, nome: str) -> str:
        self.conectar()
        consulta = self.cursor.execute("SELECT tipo FROM objeto WHERE nome =?", (nome,)).fetchone()
        self.desconectar()
        
        if consulta:
            return consulta[0]
        else:
            return ""
    
    def alterarItem(self, nome: str, quantidade: int, tipo: str) -> bool:
        if (nome == ""):
            return False
        
        if (quantidade == None or quantidade == ""):
            quantidade = self.getQuantidade(nome)
            
        if (tipo == ""):
            tipo = self.getTipo(nome)
        
        self.conectar()
        self.cursor.execute("UPDATE objeto SET quantidade =?, tipo =? WHERE nome =?", (quantidade, tipo, nome))
        self.connection.commit()
        self.desconectar()
        
        return True
    
    def getAllItens(self) -> list:
        self.conectar()
        consulta = self.cursor.execute("SELECT * FROM objeto").fetchall()
        self.desconectar()
        
        return consulta
    
    def removerItem(self, nome: str):
        self.conectar()
        self.cursor.execute("DELETE FROM objeto WHERE nome =?", (nome,))
        self.connection.commit()
        self.desconectar()
        
        return True

if __name__ == "__main__":
    pass