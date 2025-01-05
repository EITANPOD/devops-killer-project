const API_URL = 'http://backend:5000/api';

// Load recipes by category
async function loadCategory(category) {
    try {
        const response = await fetch(`${API_URL}/recipes/category/${category}`);
        const recipes = await response.json();
        displayRecipes(recipes, category);
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('app').innerHTML = '<p>Error loading recipes</p>';
    }
}

// Load all recipes
async function loadAllRecipes() {
    try {
        const categories = ['Breakfast', 'Lunch', 'Dinner', 'Dessert'];
        let allRecipes = [];
        
        for (const category of categories) {
            const response = await fetch(`${API_URL}/recipes/category/${category}`);
            const recipes = await response.json();
            allRecipes = [...allRecipes, ...recipes];
        }
        
        displayRecipes(allRecipes, 'All Recipes');
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('app').innerHTML = '<p>Error loading recipes</p>';
    }
}

// Display recipes
function displayRecipes(recipes, category) {
    const app = document.getElementById('app');
    const html = `
        <h1 class="page-title">${category}</h1>
        <div class="recipes-grid">
            ${recipes.map(recipe => `
                <div class="recipe-card">
                    <div class="recipe-content">
                        <h2 class="recipe-title">${recipe.title}</h2>
                        <p class="recipe-category">${recipe.category}</p>
                        <p class="recipe-instructions">${recipe.instructions}</p>
                        <div class="recipe-actions">
                            <button class="btn btn-secondary" onclick="editRecipe(${recipe.id})">Edit</button>
                            <button class="btn btn-danger" onclick="deleteRecipe(${recipe.id})">Delete</button>
                        </div>
                    </div>
                </div>
            `).join('')}
        </div>
    `;
    app.innerHTML = html;
}

// Show add recipe form
function showAddRecipeForm() {
    const app = document.getElementById('app');
    const html = `
        <div class="recipe-form">
            <h2>Add New Recipe</h2>
            <form onsubmit="submitRecipe(event)">
                <div class="form-group">
                    <label for="title">Title</label>
                    <input type="text" id="title" required>
                </div>
                <div class="form-group">
                    <label for="category">Category</label>
                    <select id="category" required>
                        <option value="Breakfast">Breakfast</option>
                        <option value="Lunch">Lunch</option>
                        <option value="Dinner">Dinner</option>
                        <option value="Dessert">Dessert</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="instructions">Instructions</label>
                    <textarea id="instructions" required></textarea>
                </div>
                <div class="form-actions">
                    <button type="submit" class="btn btn-primary">Add Recipe</button>
                    <button type="button" class="btn btn-secondary" onclick="loadAllRecipes()">Cancel</button>
                </div>
            </form>
        </div>
    `;
    app.innerHTML = html;
}

// Submit new recipe
async function submitRecipe(event) {
    event.preventDefault();
    const recipe = {
        title: document.getElementById('title').value,
        category: document.getElementById('category').value,
        instructions: document.getElementById('instructions').value
    };

    try {
        const response = await fetch(`${API_URL}/recipes`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(recipe)
        });

        if (response.ok) {
            loadCategory(recipe.category);
        } else {
            throw new Error('Failed to add recipe');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to add recipe');
    }
}

// Delete recipe
async function deleteRecipe(id) {
    if (confirm('Are you sure you want to delete this recipe?')) {
        try {
            const response = await fetch(`${API_URL}/recipes/${id}`, {
                method: 'DELETE'
            });
            if (response.ok) {
                loadAllRecipes();
            } else {
                throw new Error('Failed to delete recipe');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to delete recipe');
        }
    }
}

// Edit recipe
async function editRecipe(id) {
    try {
        const response = await fetch(`${API_URL}/recipes/${id}`);
        const recipe = await response.json();
        
        const app = document.getElementById('app');
        const html = `
            <div class="recipe-form">
                <h2>Edit Recipe</h2>
                <form onsubmit="updateRecipe(event, ${id})">
                    <div class="form-group">
                        <label for="title">Title</label>
                        <input type="text" id="title" value="${recipe.title}" required>
                    </div>
                    <div class="form-group">
                        <label for="category">Category</label>
                        <select id="category" required>
                            <option value="Breakfast" ${recipe.category === 'Breakfast' ? 'selected' : ''}>Breakfast</option>
                            <option value="Lunch" ${recipe.category === 'Lunch' ? 'selected' : ''}>Lunch</option>
                            <option value="Dinner" ${recipe.category === 'Dinner' ? 'selected' : ''}>Dinner</option>
                            <option value="Dessert" ${recipe.category === 'Dessert' ? 'selected' : ''}>Dessert</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="instructions">Instructions</label>
                        <textarea id="instructions" required>${recipe.instructions}</textarea>
                    </div>
                    <div class="form-actions">
                        <button type="submit" class="btn btn-primary">Update Recipe</button>
                        <button type="button" class="btn btn-secondary" onclick="loadAllRecipes()">Cancel</button>
                    </div>
                </form>
            </div>
        `;
        app.innerHTML = html;
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to load recipe');
    }
}

// Update recipe
async function updateRecipe(event, id) {
    event.preventDefault();
    const recipe = {
        title: document.getElementById('title').value,
        category: document.getElementById('category').value,
        instructions: document.getElementById('instructions').value
    };

    try {
        const response = await fetch(`${API_URL}/recipes/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(recipe)
        });

        if (response.ok) {
            loadCategory(recipe.category);
        } else {
            throw new Error('Failed to update recipe');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to update recipe');
    }
}

// Load all recipes when the page loads
document.addEventListener('DOMContentLoaded', loadAllRecipes);