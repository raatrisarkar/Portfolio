const apiKey = 'b5e96cb65888495fb926b657a61ae162';
const searchButton = document.getElementById('searchButton');
const ingredientsInput = document.getElementById('ingredients');
const recipesContainer = document.getElementById('recipes');

searchButton.addEventListener('click', async () => {
  const ingredients = ingredientsInput.value.trim();
  if (!ingredients) {
    alert('Please enter some ingredients!');
    return;
  }

  try {
    const response = await fetch(
      `https://api.spoonacular.com/recipes/findByIngredients?ingredients=${encodeURIComponent(ingredients)}&number=5&apiKey=${apiKey}`
    );

    if (!response.ok) {
      throw new Error('Failed to fetch recipes');
    }

    const recipes = await response.json();
    displayRecipes(recipes);
  } catch (error) {
    console.error(error);
    alert('Error fetching recipes. Please try again.');
  }
});

function displayRecipes(recipes) {
  recipesContainer.innerHTML = ''; // Clear previous results

  if (recipes.length === 0) {
    recipesContainer.innerHTML = '<p>No recipes found. Try different ingredients!</p>';
    return;
  }

  recipes.forEach((recipe, index) => {
    const recipeCard = document.createElement('div');
    recipeCard.classList.add('recipe');
    recipeCard.style.animationDelay = `${index * 0.2}s`; // Staggered animation
    recipeCard.innerHTML = `
      <img src="${recipe.image}" alt="${recipe.title}">
      <h3>${recipe.title}</h3>
      <a href="https://spoonacular.com/recipes/${recipe.title.replace(/ /g, '-')}-${recipe.id}" target="_blank">View Recipe</a>
    `;
    recipesContainer.appendChild(recipeCard);
  });
}
