from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Get database credentials from environment variables
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_NAME = os.environ.get('DB_NAME')
DB_HOST = os.environ.get('DB_HOST', 'recipes-db.czqakocysnbb.us-east-1.rds.amazonaws.com')
DB_PORT = os.environ.get('DB_PORT', '5432')

# Construct database URI using environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
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