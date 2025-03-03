# E-commerce API - Flask + Swagger

## 📌 Sobre o Projeto

Este projeto teve início no minicurso de Python da Rocketseat. Inicialmente, era uma aplicação mais simples, mas decidi expandi-lo e ele se tornou um projeto mais completo para aprender e praticar Python, Flask e Swagger. Ele consiste em uma API de e-commerce onde é possível gerenciar produtos, carrinho de compras e usuários.

## 🚀 Tecnologias Utilizadas

- **Python** 3.13.2
- **Flask**
- **Flask-SQLAlchemy** (Banco de dados)
- **Flask-Login** (Autenticação de usuários)
- **Flasgger** (Documentação Swagger)

## 📥 Instalação e Configuração

### 🔹 1. Clonar o Repositório

```sh
  git clone https://github.com/JuandaSilvaa/ecommerce-api.git
  cd ecommerce-api
```

### 🔹 2. Instalar Dependências

```sh
  pip install -r requirements.txt
```

### 🔹 3. Criar o Banco de Dados

Para configurar o banco de dados, execute os seguintes comandos:

💡 **Dica**: Se quiser visualizar o banco de dados no VS Code, use a extensão **SQLite Viewer** para facilitar a inspeção das tabelas e dados armazenados.

```sh
  flask shell  # Abre o terminal Flask
  db.create_all()  # Cria as tabelas
```

Caso precise apagar e recriar as tabelas:

```sh
  db.drop_all()  # Apaga todas as tabelas
  db.create_all()  # Cria novamente
```

### 🔹 4. Criar um Usuário direto no Banco de Dados (Opicional)

```sh
  flask shell
  user = User(username="admin", password="123")  # Cria o usuário
  db.session.add(user)  # Adiciona ao banco
  db.session.commit()  # Salva as modificações
  exit()  # Sai do Flask Shell
```

## ▶️ Como Rodar o Projeto no VS Code

Se estiver rodando no **VS Code**, siga estas etapas:

💡 **Recomendado**: Tenha instalada a extensão padrão da Microsoft para **Python** no VS Code para melhor experiência.

### 🔹 1. Abrir o Terminal Integrado do VS Code

- Acesse **Terminal** > **Novo Terminal** ou pressione `Ctrl + Shift + '`.

### 🔹 2. Rodar o Servidor Flask

Para rodar o projeto, use o seguinte comando:

```sh
  python application.py
```

A API estará disponível em: `http://localhost:5000`

## 📖 Documentação Swagger

A documentação da API está disponível via Swagger em:

- **Swagger UI:** [http://localhost:5000/apidocs/](http://localhost:5000/apidocs/)
- **Importação no Swagger Editor:** Você pode importar o arquivo de documentação no site [Swagger Editor](https://editor.swagger.io/)

## 🛠 Endpoints Principais

A API contém endpoints para:

- Gerenciar usuários (criação, login, logout, remoção)
- Gerenciar produtos (adicionar, listar, atualizar, deletar)
- Adicionar e remover itens do carrinho
- Realizar checkout

## 💡 Comentários no Código
O código deste projeto contém diversos comentários explicativos para facilitar o entendimento das funcionalidades e auxiliar nos estudos. Isso torna mais fácil compreender cada parte do código e como a API funciona.

## 📚 Contribuição

Este projeto é apenas para fins de aprendizado. Sinta-se à vontade para sugerir melhorias ou testar novas funcionalidades.

---

📌 **Desenvolvido para estudos de Python, Flask e Swagger!** 🚀
