from flask import Flask, request, jsonify
from itertools import permutations

app = Flask(__name__)

# Define warehouse stock
stock = {
    'C1': {'A', 'B', 'C', 'G', 'H'},
    'C2': {'B', 'C', 'D', 'F', 'G', 'I'},
    'C3': {'C', 'D', 'E', 'F', 'H', 'I'}
}

# Cost from centers to L1
to_l1_cost = {'C1': 10, 'C2': 20, 'C3': 30}

# Cost between centers (symmetric)
travel_cost = {
    ('C1', 'C2'): 15, ('C2', 'C1'): 15,
    ('C1', 'C3'): 25, ('C3', 'C1'): 25,
    ('C2', 'C3'): 10, ('C3', 'C2'): 10
}


def get_centers_for_product(product):
    return [center for center in stock if product in stock[center]]


def get_min_cost(order):
    centers = ['C1', 'C2', 'C3']
    min_total_cost = float('inf')

    for start in centers:
        route = [start]
        used_centers = set()
        deliveries = []

        remaining = order.copy()

        while any(remaining.values()):
            for c in centers:
                for product in list(remaining):
                    if remaining[product] > 0 and product in stock[c]:
                        used_centers.add(c)
                        deliveries.append(c)
                        remaining[product] -= 1
                        if remaining[product] == 0:
                            del remaining[product]

        unique_deliveries = list(set(deliveries))
        for perm in permutations(unique_deliveries):
            cost = 0
            current = start
            for center in perm:
                if center != current:
                    cost += travel_cost.get((current, center), 0)
                    current = center
                cost += to_l1_cost[current]
            if cost < min_total_cost:
                min_total_cost = cost

    return min_total_cost


@app.route('/min-cost', methods=['POST'])
def calculate_min_cost():
    order = request.get_json()
    cost = get_min_cost(order)
    return jsonify({"minimum_cost": cost})





if __name__ == '__main__':
    app.run(debug=True)
