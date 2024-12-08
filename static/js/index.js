document.getElementById('solveForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    // Obtener datos de los inputs
    const supply = document.querySelector('input[name="supply"]').value.split(',').map(Number);
    const demand = document.querySelector('input[name="demand"]').value.split(',').map(Number);
    const costs = document.querySelector('textarea[name="costs"]').value
        .trim()
        .split('\n')
        .map(row => row.split(' ').map(Number));

    const data = { supply, demand, costs };

    try {
        // Enviar datos al servidor
        const response = await fetch('/api/solve', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        mostrarResultados(result);
    } catch (error) {
        alert('Error al procesar los datos. Verifica los datos ingresados.');
    }
});


function mostrarResultados(data) {
    const resultsDiv = document.getElementById('resultsContent');
    resultsDiv.innerHTML = '';

    if (data.error) {
        resultsDiv.innerHTML = `<p>Error: ${data.error}</p>`;
        return;
    }

    // Mostramos el método óptimo y su costo
    if (data.metodo_optimo && data.costo_optimo) {
        resultsDiv.innerHTML += `<h3>Método Óptimo: ${data.metodo_optimo}</h3>`;
        resultsDiv.innerHTML += `<p>Costo Óptimo: ${data.costo_optimo}</p>`;
    }

    // Mostrar la matriz óptima
    if (data.matriz_optima) {
        resultsDiv.innerHTML += '<h3>Matriz Óptima:</h3>';
        resultsDiv.innerHTML += formatTable(data.matriz_optima);
    }

    // Comparación de los métodos
    if (data.comparacion) {
        resultsDiv.innerHTML += '<h3>Comparación:</h3>';

        // Método de Mínimo Costo
        if (data.comparacion["Metodo de Mínimo Costo"]) {
            const minCost = data.comparacion["Metodo de Mínimo Costo"];
            resultsDiv.innerHTML += `<h4>Método de Mínimo Costo</h4>`;
            resultsDiv.innerHTML += `<p>Costo Total: ${minCost.costo_total}</p>`;
            resultsDiv.innerHTML += formatTable(minCost.matriz_asignacion);
        }

        // Método de Aproximación de Vogel
        if (data.comparacion["Metodo de Aproximación de Vogel"]) {
            const vogel = data.comparacion["Metodo de Aproximación de Vogel"];
            resultsDiv.innerHTML += `<h4>Método de Aproximación de Vogel</h4>`;
            resultsDiv.innerHTML += `<p>Costo Total: ${vogel.costo_total}</p>`;
            resultsDiv.innerHTML += formatTable(vogel.matriz_asignacion);
        }
    }
}

function formatTable(matrix) {
    let html = '<table border="1" style="border-collapse: collapse; width: 100%;">';
    matrix.forEach(row => {
        html += '<tr>';
        row.forEach(cell => {
            html += `<td style="padding: 8px; text-align: center;">${cell}</td>`;
        });
        html += '</tr>';
    });
    html += '</table>';
    return html;
}



function formatTable(matrix) {
    let html = '<table border="1" style="border-collapse: collapse; width: 100%;">';
    matrix.forEach(row => {
        html += '<tr>';
        row.forEach(cell => {
            html += `<td style="padding: 8px; text-align: center;">${cell}</td>`;
        });
        html += '</tr>';
    });
    html += '</table>';
    return html;
}
