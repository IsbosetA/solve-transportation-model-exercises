from flask import Flask, request, jsonify, render_template
import numpy as np
from scipy.optimize import linprog

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/solve', methods=['POST'])
def api_solve():
    try:
        # Obtener los datos de la solicitud
        data = request.get_json()
        supply = data['supply']
        demand = data['demand']
        costs = data['costs']

        # Llamar a los algoritmos
        allocation_min_cost = minimo_costo(supply, demand, costs)
        allocation_vogel = vogel_approximation(supply, demand, costs)

        # Calcular los costos totales de ambas asignaciones
        cost_min_cost = calcular_costo_total(allocation_min_cost, costs)
        cost_vogel = calcular_costo_total(allocation_vogel, costs)

        # Determinar el método óptimo basándonos en el costo total
        if cost_min_cost < cost_vogel:
            metodo_optimo = "Método de Mínimo Costo"
            allocation_optima = allocation_min_cost
            costo_optimo = cost_min_cost
        else:
            metodo_optimo = "Método de Aproximación de Vogel"
            allocation_optima = allocation_vogel
            costo_optimo = cost_vogel

        # Preparar la respuesta con los resultados
        return jsonify({
            "metodo_optimo": metodo_optimo,
            "costo_optimo": costo_optimo,
            "matriz_optima": allocation_optima,
            "comparacion": {
                "Metodo de Mínimo Costo": {
                    "costo_total": cost_min_cost,
                    "matriz_asignacion": allocation_min_cost
                },
                "Metodo de Aproximación de Vogel": {
                    "costo_total": cost_vogel,
                    "matriz_asignacion": allocation_vogel
                }
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)})

def minimo_costo(supply, demand, costs):
    supply = supply[:]
    demand = demand[:]
    allocation = [[0] * len(demand) for _ in supply]
    costs_flat = [(cost, i, j) for i, row in enumerate(costs) for j, cost in enumerate(row)]
    costs_flat.sort()  # Ordenar por costo más bajo

    for cost, i, j in costs_flat:
        if supply[i] == 0 or demand[j] == 0:
            continue
        qty = min(supply[i], demand[j])
        allocation[i][j] = qty
        supply[i] -= qty
        demand[j] -= qty

    return allocation

def vogel_approximation(supply, demand, costs):
    supply = supply[:]
    demand = demand[:]
    allocation = [[0] * len(demand) for _ in supply]

    while sum(supply) > 0 and sum(demand) > 0:
        penalties = []
        # Calcular penalizaciones para filas
        for i, s in enumerate(supply):
            if s > 0:
                row = sorted((c, j) for j, c in enumerate(costs[i]) if demand[j] > 0)
                penalty = row[1][0] - row[0][0] if len(row) > 1 else row[0][0]
                penalties.append((penalty, i, 'row'))

        # Calcular penalizaciones para columnas
        for j, d in enumerate(demand):
            if d > 0:
                col = sorted((costs[i][j], i) for i in range(len(supply)) if supply[i] > 0)
                penalty = col[1][0] - col[0][0] if len(col) > 1 else col[0][0]
                penalties.append((penalty, j, 'col'))

        penalties.sort(reverse=True)
        _, idx, mode = penalties[0]

        if mode == 'row':
            i = idx
            j = min((j for j, d in enumerate(demand) if d > 0), key=lambda j: costs[i][j])
        else:
            j = idx
            i = min((i for i, s in enumerate(supply) if s > 0), key=lambda i: costs[i][j])

        qty = min(supply[i], demand[j])
        allocation[i][j] = qty
        supply[i] -= qty
        demand[j] -= qty

    return allocation

def calcular_costo_total(allocation, costs):
    costo_total = 0
    for i in range(len(allocation)):
        for j in range(len(allocation[i])):
            costo_total += allocation[i][j] * costs[i][j]
    return costo_total


if __name__ == '__main__':
    app.run(debug=True)
