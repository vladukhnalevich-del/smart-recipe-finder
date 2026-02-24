const API_URL = '/api/recipes/';

function showTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.tab').forEach(el => el.classList.remove('active'));
    document.getElementById(tabName + '-tab').classList.add('active');
    event.target.classList.add('active');
}

function displayRecipe(recipe) {
    return `<div class="recipe-card">
        <b>#${recipe.id}. ${recipe.name}</b>
        <div class="recipe-meta">
            <span class="badge">${recipe.cuisine || 'Русская'}</span>
            <span class="badge">${recipe.difficulty || 'Средняя'}</span>
            <span class="badge">${recipe.cooking_time} мин</span>
        </div>
        <div>Ингредиенты: ${Array.isArray(recipe.ingredients) ? recipe.ingredients.join(', ') : recipe.ingredients}</div>
    </div>`;
}

async function getAllRecipes() {
    const res = await fetch(API_URL);
    const recipes = await res.json();
    const html = recipes.map(r => displayRecipe(r)).join('');
    document.getElementById('allResult').innerHTML = html || 'Нет рецептов';
}

async function searchRecipe() {
    const query = document.getElementById('searchInput').value.toLowerCase();
    const res = await fetch(API_URL);
    const recipes = await res.json();
    const found = recipes.filter(r => r.name.toLowerCase().includes(query));
    const html = found.map(r => displayRecipe(r)).join('');
    document.getElementById('searchResult').innerHTML = html || 'Не найдено';
}

async function createRecipe() {
    const data = {
        name: document.getElementById('name').value,
        ingredients: document.getElementById('ingredients').value.split('\n').filter(i => i),
        instructions: document.getElementById('instructions').value,
        cooking_time: parseInt(document.getElementById('cooking_time').value),
        cuisine: document.getElementById('cuisine').value,
        difficulty: document.getElementById('difficulty').value
    };

    const res = await fetch(API_URL, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    });

    if (res.ok) {
        document.getElementById('createResult').innerHTML = 'Рецепт создан';
        document.getElementById('name').value = '';
        document.getElementById('ingredients').value = '';
        document.getElementById('instructions').value = '';
    }
}

async function deleteRecipe() {
    const id = document.getElementById('deleteId').value;
    if (!id || !confirm('Удалить рецепт?')) return;

    const res = await fetch(API_URL + id + '/', {method: 'DELETE'});
    document.getElementById('deleteResult').innerHTML = res.ok ? 'Удалено' : 'Ошибка';
}