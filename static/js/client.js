const API_URL = '/api/recipes/';

function showError(elementId, message) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = `<div class="error-message">${message}</div>`;
    }
}

function showSuccess(elementId, message) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = `<div class="success-message">${message}</div>`;
    }
}

function showLoading(elementId, message = 'Загрузка...') {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = `<div class="loading-message">${message}</div>`;
    }
}

function showTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.tab').forEach(el => el.classList.remove('active'));
    document.getElementById(tabName + '-tab').classList.add('active');

    const tabs = document.querySelectorAll('.tab');
    if (tabName === 'search') tabs[0].classList.add('active');
    else if (tabName === 'all') tabs[1].classList.add('active');
    else if (tabName === 'create') tabs[2].classList.add('active');
    else if (tabName === 'delete') tabs[3].classList.add('active');
}

function displayRecipe(recipe) {
    return `<div class="recipe-card">
        <div class="recipe-title">#${recipe.id}. ${recipe.name || recipe.title || 'Без названия'}</div>
        <div class="recipe-meta">
            <span class="badge cuisine">${recipe.cuisine || 'Не указана'}</span>
            <span class="badge difficulty-${recipe.difficulty || 'medium'}">${recipe.difficulty || 'Не указана'}</span>
            <span class="badge time">${recipe.cooking_time || '?'} мин</span>
        </div>
        <div class="ingredients">
            <strong>Ингредиенты:</strong>
            ${Array.isArray(recipe.ingredients) ? recipe.ingredients.join(', ') : (recipe.ingredients || 'Не указаны')}
        </div>
        <div class="instructions">
            <strong>Инструкции:</strong>
            ${(recipe.instructions || 'Не указаны').substring(0, 100)}${recipe.instructions && recipe.instructions.length > 100 ? '...' : ''}
        </div>
    </div>`;
}

async function getAllRecipes() {
    const resultDiv = document.getElementById('allResult');
    showLoading('allResult', 'Загрузка рецептов...');

    try {
        const response = await fetch(API_URL);

        if (!response.ok) {
            throw new Error(`HTTP ошибка! Статус: ${response.status}`);
        }

        const recipes = await response.json();

        if (recipes.length === 0) {
            resultDiv.innerHTML = '<div class="info-message">Рецептов пока нет. Создайте первый!</div>';
            return;
        }

        let html = '<h3>Все рецепты:</h3>';
        recipes.forEach(recipe => html += displayRecipe(recipe));
        resultDiv.innerHTML = html;

    } catch (error) {
        console.error('Ошибка при загрузке рецептов:', error);
        showError('allResult', `Не удалось загрузить рецепты: ${error.message}`);
    }
}

async function searchRecipe() {
    const query = document.getElementById('searchInput').value.trim();
    const resultDiv = document.getElementById('searchResult');

    if (!query) {
        showError('searchResult', 'Введите название рецепта для поиска');
        return;
    }

    showLoading('searchResult', `Поиск "${query}"...`);

    try {
        const response = await fetch(API_URL);

        if (!response.ok) {
            throw new Error(`HTTP ошибка! Статус: ${response.status}`);
        }

        const recipes = await response.json();

        const foundRecipes = recipes.filter(recipe =>
            (recipe.name || recipe.title || '').toLowerCase().includes(query.toLowerCase())
        );

        if (foundRecipes.length === 0) {
            resultDiv.innerHTML = `<div class="warning-message">По запросу "${query}" ничего не найдено</div>`;
            return;
        }

        let html = `<h3>Найдено рецептов: ${foundRecipes.length}</h3>`;
        foundRecipes.forEach(recipe => html += displayRecipe(recipe));
        resultDiv.innerHTML = html;

    } catch (error) {
        console.error('Ошибка при поиске:', error);
        showError('searchResult', `Ошибка при поиске: ${error.message}`);
    }
}

async function createRecipe() {
    const name = document.getElementById('name').value.trim();
    if (!name) {
        showError('createResult', 'Введите название рецепта');
        return;
    }

    const ingredientsText = document.getElementById('ingredients').value.trim();
    if (!ingredientsText) {
        showError('createResult', 'Введите ингредиенты');
        return;
    }

    const ingredients = ingredientsText.split('\n').filter(i => i.trim().length > 0);
    const cooking_time = parseInt(document.getElementById('cooking_time').value);

    if (isNaN(cooking_time) || cooking_time <= 0) {
        showError('createResult', 'Введите корректное время приготовления (положительное число)');
        return;
    }

    const cuisine = document.getElementById('cuisine').value;
    const difficulty = document.getElementById('difficulty').value;

    const recipeData = {
        name: name,
        ingredients: ingredients,
        instructions: document.getElementById('instructions').value.trim(),
        cooking_time: cooking_time,
        cuisine: cuisine,
        difficulty: difficulty
    };

    showLoading('createResult', 'Сохранение рецепта...');

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(recipeData)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || `HTTP ошибка! Статус: ${response.status}`);
        }

        showSuccess('createResult', 'Рецепт успешно создан!');

        document.getElementById('name').value = '';
        document.getElementById('ingredients').value = '';
        document.getElementById('instructions').value = '';
        document.getElementById('cooking_time').value = '30';

        getAllRecipes();

    } catch (error) {
        console.error('Ошибка при создании рецепта:', error);
        showError('createResult', `Ошибка при создании: ${error.message}`);
    }
}

async function deleteRecipe() {
    const id = document.getElementById('deleteId').value.trim();
    const resultDiv = document.getElementById('deleteResult');

    if (!id) {
        showError('deleteResult', 'Введите ID рецепта');
        return;
    }

    if (!confirm(`Удалить рецепт с ID ${id}?`)) return;

    showLoading('deleteResult', `Удаление рецепта #${id}...`);

    try {
        const response = await fetch(API_URL + id + '/', {
            method: 'DELETE'
        });

        if (!response.ok) {
            if (response.status === 404) {
                throw new Error(`Рецепт с ID ${id} не найден`);
            }
            throw new Error(`HTTP ошибка! Статус: ${response.status}`);
        }

        showSuccess('deleteResult', `Рецепт #${id} успешно удален!`);
        document.getElementById('deleteId').value = '';

        getAllRecipes();

    } catch (error) {
        console.error('Ошибка при удалении:', error);
        showError('deleteResult', `Ошибка при удалении: ${error.message}`);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') searchRecipe();
        });
    }

    const deleteInput = document.getElementById('deleteId');
    if (deleteInput) {
        deleteInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') deleteRecipe();
        });
    }

    getAllRecipes();
});