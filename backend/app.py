from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import boto3
import json
from botocore.exceptions import ClientError

app = Flask(__name__)
CORS(app)

def get_db_credentials():
    secret_name = "postgress-secrets"  # Change if your secret name is different
    region_name = "us-east-1"  # Change to your AWS region

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        print(f"Error retrieving secret: {e}")
        return None  # Handle this properly in your app

    # Parse the secret string into a dictionary
    secret_dict = json.loads(get_secret_value_response['SecretString'])

    # Extract username and password
    db_user = secret_dict["username"]
    db_pass = secret_dict["password"]

    # Define your RDS endpoint (Replace with your actual endpoint)
    db_host = "recipes-db.czqakocysnbb.us-east-1.rds.amazonaws.com"  
    db_name = "recipesDB"

    # Return PostgreSQL connection string
    return f"postgresql://{db_user}:{db_pass}@{db_host}:5432/{db_name}"

app.config['SQLALCHEMY_DATABASE_URI'] = get_db_credentials()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    instructions = db.Column(db.Text, nullable=False)

# Initialize Database
with app.app_context():
    db.create_all()

@app.route('/api/recipes/<int:id>', methods=['GET'])
def get_recipe(id):
    recipe = Recipe.query.get(id)
    if not recipe:
        return jsonify({'error': 'Recipe not found'}), 404
    return jsonify({
        'id': recipe.id,
        'title': recipe.title,
        'category': recipe.category,
        'instructions': recipe.instructions
    })
    

@app.route('/api/recipes/category/<string:category>', methods=['GET'])
def get_recipes_by_category(category):
    recipes = Recipe.query.filter_by(category=category).all()
    recipe_list = [
        {
            'id': recipe.id,
            'title': recipe.title,
            'category': recipe.category,
            'instructions': recipe.instructions
        }
        for recipe in recipes
    ]
    return jsonify(recipe_list)
    

@app.route('/api/recipes', methods=['POST'])
def add_recipe():
    data = request.json
    new_recipe = Recipe(
        title=data.get('title'),
        category=data.get('category'),
        instructions=data.get('instructions')
    )
    db.session.add(new_recipe)
    db.session.commit()
    return jsonify({'message': 'Recipe added successfully'}), 201


@app.route('/api/recipes/<int:id>', methods=['PUT'])
def update_recipe(id):
    recipe = Recipe.query.get(id)
    if not recipe:
        return jsonify({'error': 'Recipe not found'}), 404

    data = request.json
    recipe.title = data.get('title', recipe.title)
    recipe.category = data.get('category', recipe.category)
    recipe.instructions = data.get('instructions', recipe.instructions)

    db.session.commit()
    return jsonify({'message': 'Recipe updated successfully'})



@app.route('/api/recipes/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return jsonify({'error': 'Recipe not found'}), 404

    db.session.delete(recipe)
    db.session.commit()
    return jsonify({'message': 'Recipe deleted successfully'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)