"""Tests for the Flask API."""

import pytest
import json
from lyra.api import create_app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestHealthEndpoint:
    """Tests for the /api/health endpoint."""

    def test_health_endpoint(self, client):
        """Test that the health endpoint returns a 200 status."""
        response = client.get('/api/health')
        assert response.status_code == 200

    def test_health_endpoint_response(self, client):
        """Test that the health endpoint returns the expected response."""
        response = client.get('/api/health')
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert data['version'] == '0.1.0'
        assert 'endpoints' in data


class TestWisdomEndpoint:
    """Tests for the /api/wisdom endpoint."""

    def test_wisdom_search(self, client):
        """Test searching the wisdom database."""
        response = client.get('/api/wisdom?query=life')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'count' in data
        assert 'results' in data
        assert isinstance(data['results'], list)

    def test_wisdom_search_no_query(self, client):
        """Test that wisdom search without query returns 400."""
        response = client.get('/api/wisdom')
        assert response.status_code == 400

    def test_wisdom_by_tag(self, client):
        """Test filtering wisdom by tag."""
        response = client.get('/api/wisdom?tag=philosophy')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'results' in data

    def test_wisdom_by_author(self, client):
        """Test filtering wisdom by author."""
        response = client.get('/api/wisdom?author=Socrates')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'results' in data

    def test_wisdom_random(self, client):
        """Test getting random wisdom quotes."""
        response = client.get('/api/wisdom?random=true&limit=3')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['count'] == 3
        assert len(data['results']) == 3

    def test_wisdom_limit(self, client):
        """Test that the limit parameter works."""
        response = client.get('/api/wisdom?query=the&limit=2')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['count'] <= 2


class TestQuantumEndpoint:
    """Tests for the /api/quantum endpoint."""

    def test_quantum_simulation_default(self, client):
        """Test quantum simulation with default theta."""
        response = client.get('/api/quantum')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'theta' in data
        assert 'result' in data
        assert data['theta'] == 0.0

    def test_quantum_simulation_custom_theta(self, client):
        """Test quantum simulation with custom theta."""
        response = client.get('/api/quantum?theta=0.5')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['theta'] == 0.5
        assert 'result' in data

    def test_quantum_simulation_pi(self, client):
        """Test quantum simulation with theta=pi."""
        response = client.get('/api/quantum?theta=3.14159')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'result' in data


class TestCollapseEndpoint:
    """Tests for the /api/collapse endpoint."""

    def test_collapse_simulation_default(self, client):
        """Test collapse simulation with default alpha_G."""
        response = client.get('/api/collapse')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'alpha_G' in data
        assert 'values' in data
        assert data['alpha_G'] == 1.0

    def test_collapse_simulation_custom_alpha_G(self, client):
        """Test collapse simulation with custom alpha_G."""
        response = client.get('/api/collapse?alpha_G=2.0')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['alpha_G'] == 2.0
        assert 'values' in data
        assert len(data['values']) == 100

    def test_collapse_simulation_values(self, client):
        """Test that collapse simulation values are valid."""
        response = client.get('/api/collapse?alpha_G=1.0')
        assert response.status_code == 200
        data = json.loads(response.data)
        values = data['values']
        assert all(isinstance(v, (int, float)) for v in values)
        assert values[0] == 1.0  # Initial condition
