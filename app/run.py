from app import app
from database import criar_tabela

if __name__ == '__main__':
    # Cria a tabela no banco de dados ao iniciar a aplicação
    criar_tabela()
    app.run(debug=True)