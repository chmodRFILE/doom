// Random Crawler Generator JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log('Random Crawler Generator loaded');
});

function generateRandomConfig() {
    fetch('/tools/generate-random-config')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const resultDiv = document.getElementById('configResult');
                resultDiv.innerHTML = '<h3>Generated Configuration:</h3><pre>' + JSON.stringify(data.config, null, 2) + '</pre>';
            } else {
                alert('Error: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to generate configuration');
        });
}

function createRandomCrawler() {
    fetch('/tools/create-random-crawler', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const resultDiv = document.getElementById('crawlerResult');
            resultDiv.innerHTML = '<h3>Crawler Created Successfully!</h3><p>' + data.message + '</p>';
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to create crawler');
    });
}

function generateRecipe() {
    fetch('/tools/generate-recipe')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const resultDiv = document.getElementById('recipeResult');
                const recipe = data.recipe;
                resultDiv.innerHTML = `
                    <h3>Generated Recipe:</h3>
                    <p><strong>Name:</strong> ${recipe.name}</p>
                    <p><strong>Description:</strong> ${recipe.description}</p>
                    <p><strong>Features:</strong> ${recipe.features.join(', ')}</p>
                    <h4>Configuration:</h4>
                    <pre>${JSON.stringify(recipe.config, null, 2)}</pre>
                `;
            } else {
                alert('Error: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to generate recipe');
        });
}

function createMultipleCrawlers() {
    // This would be implemented in the backend
    alert('Multiple crawler creation functionality would go here');
}