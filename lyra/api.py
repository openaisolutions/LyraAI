"""
Flask REST API for LYRA AI.
Provides endpoints for quantum simulations, wisdom search, and scientific models.
Includes OpenAPI/Swagger documentation via Flasgger.
"""

from flask import Blueprint, Flask, jsonify, request
from werkzeug.exceptions import BadRequest
from flasgger import Swagger

from .quantum import quantum_simulation
from .models import simulate_collapse
from .wisdom import WisdomDatabase

# Create a Blueprint for the API
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Initialize Wisdom Database
wisdom_db = WisdomDatabase()

# Swagger configuration
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": '/flasgger_static',
    "swagger_ui": True,
    "specs_route": '/apidocs/'
}

swagger = Swagger(config=swagger_config)


@api_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    ---
    responses:
      200:
        description: API is healthy
        schema:
          type: object
          properties:
            status:
              type: string
              example: healthy
            version:
              type: string
              example: 0.1.0
            endpoints:
              type: array
              items:
                type: string
    """
    return jsonify({
        'status': 'healthy',
        'version': '0.1.0',
        'endpoints': [
            '/api/health',
            '/api/wisdom',
            '/api/quantum',
            '/api/collapse',
            '/apidocs/'
        ]
    }), 200


@api_bp.route('/wisdom', methods=['GET'])
def search_wisdom():
    """
    Search the Wisdom Database.
    ---
    parameters:
      - name: query
        in: query
        type: string
        required: false
        description: Search term for wisdom quotes
      - name: limit
        in: query
        type: integer
        required: false
        default: 5
        description: Maximum number of results
      - name: tag
        in: query
        type: string
        required: false
        description: Filter by tag
      - name: author
        in: query
        type: string
        required: false
        description: Filter by author
      - name: random
        in: query
        type: boolean
        required: false
        default: false
        description: Return random quotes if true
    responses:
      200:
        description: List of matching quotes
        schema:
          type: object
          properties:
            count:
              type: integer
              example: 3
            results:
              type: array
              items:
                type: object
                properties:
                  text:
                    type: string
                    example: The only true wisdom is in knowing you know nothing.
                  author:
                    type: string
                    example: Socrates
                  tags:
                    type: array
                    items:
                      type: string
                    example: [humility, knowledge, philosophy]
      400:
        description: No search parameters provided
    """
    query = request.args.get('query', '')
    limit = int(request.args.get('limit', 5))
    tag = request.args.get('tag', None)
    author = request.args.get('author', None)
    random = request.args.get('random', 'false').lower() == 'true'

    if random:
        results = wisdom_db.get_random(limit=limit)
    elif tag:
        results = wisdom_db.get_by_tag(tag, limit=limit)
    elif author:
        results = wisdom_db.get_by_author(author, limit=limit)
    elif query:
        results = wisdom_db.search(query, limit=limit)
    else:
        msg = "At least one of query, tag, author, or random=true must be provided"
        raise BadRequest(msg)

    return jsonify({
        'count': len(results),
        'results': results
    }), 200


@api_bp.route('/quantum', methods=['GET'])
def quantum_simulation_api():
    """
    Run a quantum circuit simulation.
    ---
    parameters:
      - name: theta
        in: query
        type: number
        required: false
        default: 0.0
        description: Rotation angle in radians for the RX gate
    responses:
      200:
        description: Result of the quantum simulation
        schema:
          type: object
          properties:
            theta:
              type: number
              example: 0.5
            result:
              type: number
              example: 0.8775825618903726
            interpretation:
              type: string
              example: Expectation value of PauliZ operator (range: [-1, 1])
    """
    theta = float(request.args.get('theta', 0.0))
    result = quantum_simulation(theta)

    return jsonify({
        'theta': theta,
        'result': result,
        'interpretation': 'Expectation value of PauliZ operator (range: [-1, 1])'
    }), 200


@api_bp.route('/collapse', methods=['GET'])
def collapse_simulation_api():
    """
    Simulate informational collapse dynamics.
    ---
    parameters:
      - name: alpha_G
        in: query
        type: number
        required: false
        default: 1.0
        description: Coupling constant for the collapse process
    responses:
      200:
        description: Time series of informational gradient values
        schema:
          type: object
          properties:
            alpha_G:
              type: number
              example: 1.0
            time_points:
              type: integer
              example: 100
            values:
              type: array
              items:
                type: number
              example: [1.0, 0.95, 0.90, ...]
            interpretation:
              type: string
              example: Informational gradient over time (decaying exponential)
    """
    alpha_G = float(request.args.get('alpha_G', 1.0))
    results = simulate_collapse(alpha_G=alpha_G)

    return jsonify({
        'alpha_G': alpha_G,
        'time_points': len(results),
        'values': results,
        'interpretation': 'Informational gradient over time (decaying exponential)'
    }), 200


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.register_blueprint(api_bp)
    swagger.init_app(app)
    return app


# Create a default app instance for direct import
app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
