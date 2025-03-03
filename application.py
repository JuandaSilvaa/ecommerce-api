# Importação
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy # uma classe
from flask_cors import CORS
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flasgger import Swagger

# Instância 
application = Flask(__name__)
application.config['SECRET_KEY'] = "minha_chave_123"
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db' # banco SQLite 

login_manager = LoginManager()
db = SQLAlchemy(application)
login_manager.init_app(application)
# login_manager.login_view = 'login'
CORS(application)

# Configuração do Swagger
template = {
    "swagger": "2.0",
    "info": {
        "title": "E-commerce API",
        "description": "API to manage products and carts in e-commerce.",
        "version": "1.0.0",
        "contact": {
            "name": "Juan da Silva",
            "url": "https://www.linkedin.com/in/juan-da-silva-almeida-62aa491b5"
        }
    },
    "host": "localhost:5000",
    "schemes": ["http"],
    "securityDefinitions": {
        "ApiKeyAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization"
        }
    }
}

Swagger(application, template=template)

#Modelagem
# User (id, username, password)
class User(db.Model, UserMixin): #UserMixin e uma herança então estou herdando dele 
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), nullable=False, unique=True)
  password = db.Column(db.String(80), nullable=False)
  cart = db.relationship('CartItem', backref='user', lazy=True) 
  """lazy='True' ele so vai acessar as informações do carrinho 
  quando eu tentar acessar o cart não sempre isso para performace
  """
  
#Produto (id, name, price, description)
class Product(db.Model): # Classe produto
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(120), nullable=False)
  price = db.Column(db.Float, nullable=False) 
  description = db.Column(db.Text, nullable=True)

# cart
class CartItem(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

# Autenticação
@login_manager.user_loader # isso existe para ver qual usuario esta acessando a rota altenticada
def load_user(user_id):
  return User.query.get(int(user_id))

# Rotas/endpoint
@application.route('/')
def initial():
  """
  Check if the API is running
  ---
  responses:
    200:
      description: API is working correctly
  """
  return 'API up'

#Rota de login
@application.route('/login', methods=["POST"])
def login():
  """
  User login
  ---
  tags:
    - Authentication
  parameters:
    - name: body
      in: body
      required: true
      schema:
        type: object
        required:
          - username
          - password
        properties:
          username:
            type: string
            description: User's unique username
          password:
            type: string
            format: password
            description: User's password
  responses:
    200:
      description: User logged in successfully
      schema:
        type: object
        properties:
          message:
            type: string
            example: "Logged in successfully"
    401:
      description: Unauthorized. Invalid credentials
      schema:
        type: object
        properties:
          message:
            type: string
            example: "Unauthorized. Invalid credentials"
  """
  data = request.json
  user = User.query.filter_by(username=data.get("username")).first()

  if user and data.get("password") == user.password: # verifica a senha
      login_user(user) # authentica o user
      return jsonify({"message": "Logged in successfully"})
  return jsonify({"message": "Unauthorized. Invalid credentials"}), 401

#Rota de logout
@application.route('/logout', methods=["POST"])
@login_required
def logout():
  """
  User logout
  ---
  tags:
    - Authentication
  security:
    - ApiKeyAuth: []
  responses:
    200:
      description: User logged out successfully
      schema:
        type: object
        properties:
          message:
            type: string
            example: "Logout successfully"
    401:
      description: Unauthorized. No active session
      schema:
        type: object
        properties:
          message:
            type: string
            example: "Unauthorized. No active session"
  """
  logout_user()
  return jsonify({"message": "Logout successfully"})

# Rota para adicionar usuario
@application.route('/api/user/add', methods=["POST"])
def add_user():
  """
  Add a new user
  ---
  tags:
    - Users
  parameters:
    - name: body
      in: body
      required: true
      schema:
        type: object
        required:
          - username
          - password
        properties:
          username:
            type: string
            description: The username for the new user
          password:
            type: string
            description: The password for the new user
  responses:
    200:
      description: User added successfully
      schema:
        type: object
        properties:
          message:
            type: string
            example: "User added successfully"
    400:
      description: Invalid user data
      schema:
        type: object
        properties:
          message:
            type: string
            example: "Invalid user data"
  """  
  data = request.json
  if 'username' in data and 'password' in data :
    user = User(username=data["username"], password=data["password"]) 
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User added successfully"})
  return jsonify({"message": "Invalid user data"}), 400

# Rota deletar usuario
@application.route('/api/user/delete/<int:user_id>', methods=["DELETE"])
@login_required 
def delete_user(user_id):
  """
  Delete a user by ID
  ---
  tags:
    - Users
  parameters:
    - name: user_id
      in: path
      required: true
      type: integer
      description: The ID of the user to be deleted
  responses:
    200:
      description: User deleted successfully
      schema:
        type: object
        properties:
          message:
            type: string
            example: "User deleted successfully"
    404:
      description: User not found
      schema:
        type: object
        properties:
          message:
            type: string
            example: "User not found"
    401:
      description: Unauthorized. User must be logged in
      schema:
        type: object
        properties:
          message:
            type: string
            example: "Unauthorized. User must be logged in"
  security:
    - ApiKeyAuth: []
  """
  user = User.query.get(user_id)
  if user and current_user.id == user_id :
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"})
  return jsonify({"message": "User not found"}), 404


# Rota de atualizar usuarios
@application.route('/api/user/update/<int:user_id>', methods=["PUT"])
@login_required 
def update_user(user_id):
  """
  Update user information
  ---
  tags:
    - Users
  parameters:
    - name: user_id
      in: path
      required: true
      type: integer
      description: The ID of the user to be updated
    - name: body
      in: body
      required: true
      schema:
        type: object
        properties:
          username:
            type: string
            description: New username
          password:
            type: string
            description: New password
  responses:
    200:
      description: User updated successfully
      schema:
        type: object
        properties:
          message:
            type: string
            example: "User updated successfully"
    404:
      description: User not found
      schema:
        type: object
        properties:
          message:
            type: string
            example: "User not found"
    403:
      description: Insufficient permission
      schema:
        type: object
        properties:
          message:
            type: string
            example: "Insufficient permission"
  security:
    - ApiKeyAuth: []
  """
  user = User.query.get(user_id)
  if not user: 
    return jsonify({"message": "User not found"}), 404
  
  if user and current_user.id == user_id :
    data = request.json
    if 'username' in data:
      user.username = data['username']
    if 'password' in data:
      user.password = data['password']
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})
  return jsonify({"message": "insufficient permission"}), 403
  

# Rota para adicionar produto
#description=data.get("description", "") ele adiciona o vazio "" como default, caso não venha nada no get
@application.route('/api/products/add', methods=["POST"])
@login_required # exige senha nessa rota
def add_product():
  """
  Add a new product
  ---
  tags:
    - Products
  security:
    - ApiKeyAuth: []
  parameters:
    - name: body
      in: body
      required: true
      schema:
        type: object
        required:
          - name
          - price
        properties:
          name:
            type: string
            description: Product name
          price:
            type: number
            format: float
            description: Product price
          description:
            type: string
            description: Optional product description
  responses:
    200:
      description: Product added successfully
      schema:
        type: object
        properties:
          message:
            type: string
            example: "Product added successfully"
    400:
      description: Invalid product data
      schema:
        type: object
        properties:
          message:
            type: string
            example: "Invalid product data"
    401:
      description: Unauthorized - Authentication required
      schema:
        type: object
        properties:
          message:
            type: string
            example: "Unauthorized. Please log in."
  """
  data = request.json
  if 'name' in data and 'price' in data :
    product = Product(name=data["name"], price=data["price"], description=data.get("description", "")) 
    db.session.add(product)
    db.session.commit()
    return jsonify({"message": "Product added successfully"})
  return jsonify({"message": "Invalid product data"}), 400


# Rota deletar produto
@application.route('/api/products/delete/<int:product_id>', methods=["DELETE"])
@login_required # exige senha nessa rota
def delete_produto(product_id):
  """
  Delete a product by ID
  ---
  tags:
    - Products
  security:
    - ApiKeyAuth: []
  parameters:
    - name: product_id
      in: path
      required: true
      type: integer
      description: The ID of the product to be deleted
  responses:
    200:
      description: Product deleted successfully
      schema:
        type: object
        properties:
          message:
            type: string
            example: "Product deleted successfully"
    404:
      description: Product not found
      schema:
        type: object
        properties:
          message:
            type: string
            example: "Product not found"
    401:
      description: Unauthorized - Authentication required
      schema:
        type: object
        properties:
          message:
            type: string
            example: "Unauthorized. Please log in."
  """
  # Recuperar o produto da base de dados
  # Verificar se o produto existe
  # Se existe, apagar da base de dados
  # Se não existe, retornar 404 not found
  product = Product.query.get(product_id)
  """f product != None : ou so if product: no python ele ja vai enternter como: 
  existe algum valor valido em product, se sim vamos prosseguir 
  """
  if product:
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully"})
  return jsonify({"message": "Product not found"}), 404

# Rota de recuperar detalhes do produto
@application.route('/api/products/<int:product_id>', methods=["GET"])
def get_product_details(product_id):
  """
  Retrieve product details by ID
  ---
  tags:
    - Products
  parameters:
    - name: product_id
      in: path
      required: true
      type: integer
      description: The ID of the product to retrieve
  responses:
    200:
      description: Product details retrieved successfully
      schema:
        type: object
        properties:
          id:
            type: integer
            example: 1
          name:
            type: string
            example: "Smartphone"
          price:
            type: number
            format: float
            example: 499.99
          description:
            type: string
            example: "Latest model with advanced features"
    404:
      description: Product not found
      schema:
        type: object
        properties:
          message:
            type: string
            example: "Product not found"
  """
  product = Product.query.get(product_id)
  if product:
    return jsonify({
      "id": product.id,
      "name": product.name,
      "price": product.price,
      "description": product.description
    })
  return jsonify({"message": "Product not found"}), 404

# Rota de atualizar produtos
@application.route('/api/products/update/<int:product_id>', methods=["PUT"])
@login_required # exige senha nessa rota
def update_product(product_id):
  """
  Update an existing product by ID
  ---
  tags:
    - Products
  parameters:
    - name: product_id
      in: path
      required: true
      type: integer
      description: The ID of the product to update
    - name: body
      in: body
      required: true
      schema:
        type: object
        properties:
          name:
            type: string
            example: "Smartphone Pro"
          price:
            type: number
            format: float
            example: 599.99
          description:
            type: string
            example: "Updated version with better battery life"
  responses:
    200:
      description: Product updated successfully
      schema:
        type: object
        properties:
          message:
            type: string
            example: "Product updated successfully"
    404:
      description: Product not found
      schema:
        type: object
        properties:
          message:
            type: string
            example: "Product not found"
  """
  product = Product.query.get(product_id)
  if not product: # negando se torna verdadeiro
    return jsonify({"message": "Product not found"}), 404
  
  data = request.json
  if 'name' in data:
    product.name = data['name']
  
  if 'price' in data:
    product.price = data['price']

  if 'description' in data:
    product.description = data['description']
  
  db.session.commit()
  return jsonify({'message': 'Product updated successfully'})

# Listar produtos
@application.route('/api/products', methods=["GET"])
def get_products():
  """
  Retrieve all products
  ---
  tags:
    - Products
  responses:
    200:
      description: A list of all available products
      schema:
        type: array
        items:
          type: object
          properties:
            id:
              type: integer
              example: 1
            name:
              type: string
              example: "Wireless Headphones"
            price:
              type: number
              format: float
              example: 149.99
            description:
              type: string
              example: "Noise-canceling wireless headphones with 20 hours of battery life"
  """
  products = Product.query.all() # retorna todos os produtos cadastrados com o .all()
  product_list = []
  for product in products: # for para percorrer os produtos
    product_data = {
      "id": product.id,
      "name": product.name,
      "price": product.price,
      "description": product.description
    }
    product_list.append(product_data)
  return jsonify(product_list)

# Checkout / cart
# Rota adicionar item ao carrinho
@application.route('/api/cart/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
  """
  Add a product to the user's cart
  ---
  tags:
    - Cart
  parameters:
    - name: product_id
      in: path
      type: integer
      required: true
      description: The ID of the product to be added to the cart
  responses:
    200:
      description: Item added to the cart successfully
      schema:
        type: object
        properties:
          message:
            type: string
            example: "Item added to the cart successfully"
    400:
      description: Failed to add item to the cart
      schema:
        type: object
        properties:
          message:
            type: string
            example: "Failed to add item to the cart"
  security:
    - ApiKeyAuth: []
  """
  # tenho q ter Usuario e o produto, caso contrario tenho q parar
  # Usuario
  user = User.query.get(int(current_user.id))
  # Produto
  product = Product.query.get(product_id)

  if user and product:
    cart_item = CartItem(user_id=user.id, product_id= product.id)
    db.session.add(cart_item)
    db.session.commit()
    return jsonify({'message': 'Item added to the cart successfully'})
  return jsonify({'message': 'Failed to add item to the cart'}), 400

# Rota para DELETAR item ao carrinho
@application.route('/api/cart/remove/<int:product_id>', methods=['DELETE'])
@login_required
def remove_from_cart(product_id):
  """
  Remove a product from the user's cart
  ---
  tags:
    - Cart
  parameters:
    - name: product_id
      in: path
      type: integer
      required: true
      description: The ID of the product to be removed from the cart
  responses:
    200:
      description: Item removed from the cart successfully
      schema:
        type: object
        properties:
          message:
            type: string
            example: "Item removed from the cart successfully"
    400:
      description: Failed to remove item from the cart
      schema:
        type: object
        properties:
          message:
            type: string
            example: "Failed to remove item from the cart"
  security:
    - ApiKeyAuth: []
  """
  # procurar o item do carrinho com essas duas informações que ja tenho Produto, Usuario = Item carrinho
  cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first() # se não achar ele vai ficar como nulo
  if cart_item:
    db.session.delete(cart_item)
    db.session.commit()
    return jsonify({'message': 'Item removed from the cart successfully'})
  return jsonify({'message': 'Failed to remove item from the cart'}), 400

# Ver todos os itens no carinho 
@application.route('/api/cart', methods=['GET'])
@login_required
def view_cart():
  """
  Retrieve the user's shopping cart
  ---
  tags:
    - Cart
  responses:
    200:
      description: A list of items in the user's cart
      schema:
        type: array
        items:
          type: object
          properties:
            id:
              type: integer
              example: 1
              description: Cart item ID
            user_id:
              type: integer
              example: 2
              description: User ID who owns the cart item
            product_id:
              type: integer
              example: 5
              description: Product ID in the cart
            product_name:
              type: string
              example: "Wireless Headphones"
              description: Name of the product
            product_price:
              type: number
              format: float
              example: 99.99
              description: Price of the product
    401:
      description: Unauthorized. User must be logged in
      schema:
        type: object
        properties:
          message:
            type: string
            example: "Unauthorized. No active session"
  security:
    - ApiKeyAuth: []
  """
  # Usuario
  user = User.query.get(int(current_user.id))
  cart_items = user.cart # gera uma lista
  cart_content = []
  for cart_item in cart_items:
    product = Product.query.get(cart_item.product_id)
    cart_content.append( {
                          "id": cart_item.id,
                          "user_id": cart_item.user_id,
                          "product_id": cart_item.product_id,
                          "product_name": product.name,
                          "product_price": product.price
                        })
  return jsonify(cart_content)

# Rota de checkout
@application.route('/api/cart/checkout', methods=["POST"])
@login_required
def checkout():
  """
  Checkout and clear the user's shopping cart
  ---
  tags:
    - Cart
  responses:
    200:
      description: Checkout completed successfully. Cart has been cleared.
      schema:
        type: object
        properties:
          message:
            type: string
            example: "Checkout successful. Cart has been cleared."
    401:
      description: Unauthorized. User must be logged in.
      schema:
        type: object
        properties:
          message:
            type: string
            example: "Unauthorized. No active session"
  security:
    - ApiKeyAuth: []
  """
  user = User.query.get(int(current_user.id))
  cart_items = user.cart
  for cart_item in cart_items:
    db.session.delete(cart_item)
  db.session.commit()
  return jsonify({'message': 'Checkout successful. Cart has been cleared.'})

if __name__ == "__main__":
  application.run(debug=True)

#db.session.commit()
# session e a conecção com o banco
# commit efetiva as mudanças

"""
flask shell abre o terminal flask
db.create_all() cria as tabelas
db.drop_all() apaga todas as tabelas
user = User(username="admin", password="123") cria o usuario 
db.session.add(user) adiciona ele
db.session.commit() salva as modificações 
exit() sai do flask shell
"""

""" Definir uma rota raiz (página inicial) e a função que será executada ao requisitar
@app.route('/')
def hello_word():
  return 'Hello World'"""

# intalar dependencias pip install -r requirements.py