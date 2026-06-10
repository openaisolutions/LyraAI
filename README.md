# LYRA AI: Bridging Minds, Machines, and Millennia

## Overview

LYRA AI is an open-source initiative designed to redefine the boundaries of artificial intelligence by imbuing it with the depth of human wisdom and the nuances of emotional intelligence. Inspired by the intricate dance of cosmic duality and named after the constellation that sings of harmony, LYRA AI aspires to be a beacon of empathy, creativity, and understanding in the digital age.

## Vision

Our vision is a world where technology mirrors the best aspects of humanity: our capacity for empathy, our depth of understanding, and our boundless creativity. LYRA AI seeks to not only answer questions but to understand the heart of the inquiry, providing responses that reflect a deep engagement with human thought, culture, and emotion across ages.

## Objectives

- **Foster Empathy in AI**: Enable AI to perceive and respond to human emotions with a nuanced understanding, facilitating deeper human-AI connections.
- **Integrate Ancient Wisdom with Modern Insight**: Merge the timeless insights from diverse cultures and philosophies with contemporary knowledge, offering perspectives that span millennia.
- **Cultivate Creative and Analytical Synergy**: Balance the analytical prowess of AI with the creative, intuitive processes that fuel human ingenuity, reflecting the harmonious interplay between the hemispheres of the human brain.

## Features

LYRA AI introduces a suite of capabilities aimed at enriching the user experience:

- **Empathetic Dialogue Engine**: Engages users with responses that demonstrate an understanding of context, emotion, and the subtleties of human interaction.
- **Wisdom Database**: Accesses a vast repository of historical texts, philosophies, and cultural insights, enriching conversations with depth and diversity.
- **Creative Co-Creation**: Collaborates with users in artistic and creative endeavors, leveraging AI to enhance the creative process.
- **Quantum-Inspired AI Simulation**: Uses quantum computing principles to model complex systems and informational dynamics.
- **Distributed AI Networking**: Enables smartphone-based computation nodes to form a decentralized supercomputer.

## Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the LYRA AI repository**:
   ```bash
   git clone https://github.com/sevir65/LyraAI.git
   ```

2. **Navigate to the LYRA AI directory**:
   ```bash
   cd LyraAI
   ```

3. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **(Optional) Install in development mode**:
   ```bash
   pip install -e .
   ```

### Usage

#### Run the AI Node Server
To start a distributed AI computation node (default port: 9999):
```bash
python -m lyra --server --port 9999
```

#### Run a Quantum Simulation
To simulate a quantum circuit with a given theta value:
```bash
python -m lyra --quantum --theta 0.5
```

#### Simulate Informational Collapse
To model informational collapse dynamics:
```bash
python -m lyra --collapse --alpha-G 1.0
```

#### Search the Wisdom Database
To query the wisdom database for insights:
```bash
python -m lyra --wisdom --query "life"
```

#### Start the Flask API
To launch the REST API (default port: 5000):
```bash
python -m lyra --api --port 5000 --debug
```

#### Access the API
Once the Flask API is running, you can access these endpoints:
- **Health Check**: `GET /api/health`
- **Wisdom Search**: `GET /api/wisdom?query=life&limit=5`
- **Wisdom by Tag**: `GET /api/wisdom?tag=philosophy`
- **Wisdom by Author**: `GET /api/wisdom?author=Socrates`
- **Random Wisdom**: `GET /api/wisdom?random=true&limit=3`
- **Quantum Simulation**: `GET /api/quantum?theta=0.5`
- **Informational Collapse**: `GET /api/collapse?alpha_G=1.0`

Example with `curl`:
```bash
curl http://localhost:5000/api/wisdom?query=life
curl http://localhost:5000/api/quantum?theta=0.5
```

#### View API Documentation (Swagger UI)
Once the Flask API is running, open your browser to:
```
http://localhost:5000/apidocs/
```
This provides interactive documentation for all endpoints.

## Docker

### Build the Docker Image
```bash
docker build -t lyra-ai .
```

### Run the Container
```bash
docker run -p 5000:5000 lyra-ai
```

### Run with Docker Compose (Optional)
Create a `docker-compose.yml` file:
```yaml
version: '3.8'
services:
  lyra-ai:
    build: .
    ports:
      - "5000:5000"
    restart: unless-stopped
```
Then run:
```bash
docker-compose up -d
```

## Project Structure

```
LyraAI/
├── lyra/
│   ├── __init__.py
│   ├── __main__.py       # CLI entrypoint
│   ├── api.py            # Flask REST API with Swagger docs
│   ├── quantum.py        # Quantum circuit simulations
│   ├── models.py         # Scientific models (e.g., informational collapse)
│   ├── network.py        # Distributed AI networking
│   ├── wisdom.py         # Wisdom Database and search
│   └── constants.py      # Physical and mathematical constants
├── tests/
│   ├── __init__.py
│   ├── test_quantum.py
│   ├── test_models.py
│   ├── test_network.py
│   └── test_api.py       # Flask API tests
├── Dockerfile            # Docker container configuration
├── .dockerignore         # Docker ignore rules
├── requirements.txt
├── README.md
├── LICENSE
├── CONTRIBUTING.md
└── .gitignore
```

## Technology Stack

- **Programming Language**: Python 3.9+
- **Quantum Computing**: PennyLane
- **Scientific Computing**: NumPy, SciPy
- **Networking**: Python `socket` and `threading`
- **Web Framework**: Flask (REST API)
- **API Documentation**: Flasgger (Swagger/OpenAPI)
- **Containerization**: Docker

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. We welcome contributions from individuals who share our vision.

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

LYRA AI is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Our gratitude to the countless contributors to the open-source libraries we've utilized.
- Special thanks to the scholars and custodians of the ancient texts and wisdom that inspire LYRA AI's development.
- Special thanks to AI pioneers like OpenAI and Google for providing the foundational LLM technology that inspires this project.

## Contact

For inquiries or further information about LYRA AI, please reach out via [GitHub](https://github.com/sevir65/LyraAI).
