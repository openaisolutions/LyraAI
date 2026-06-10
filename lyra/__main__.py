"""
CLI entrypoint for LYRA AI.
Run with: python -m lyra
"""

import argparse
import logging
import sys
import threading
from typing import Any, Dict

from .quantum import quantum_simulation
from .models import simulate_collapse
from .network import AINodeServer
from .wisdom import WisdomDatabase
from .api import create_app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def run_quantum_simulation(args: argparse.Namespace) -> None:
    """Run a quantum simulation and print the result."""
    result = quantum_simulation(args.theta)
    print(f"Quantum simulation result (theta={args.theta}): {result}")


def run_collapse_simulation(args: argparse.Namespace) -> None:
    """Run an informational collapse simulation and print the results."""
    results = simulate_collapse(args.alpha_G)
    print(f"Informational collapse simulation (alpha_G={args.alpha_G}):")
    print(f"  First 5 values: {results[:5]}")
    print(f"  Total points: {len(results)}")


def run_wisdom_search(args: argparse.Namespace) -> None:
    """Search the wisdom database and print results."""
    db = WisdomDatabase()
    results = db.search(args.query, limit=args.limit)

    if not results:
        print(f"No wisdom found matching '{args.query}'")
        return

    print(f"Wisdom search results for '{args.query}':")
    for i, quote in enumerate(results, 1):
        print(f"\n  {i}. {quote['text']}")
        print(f"     — {quote['author']}")
        print(f"     Tags: {', '.join(quote['tags'])}")


def run_server(args: argparse.Namespace) -> None:
    """Start the AI Node Server."""
    # Define task handlers
    def quantum_handler(request: Dict[str, Any]) -> float:
        theta = request.get("theta", 0.0)
        return quantum_simulation(theta)

    def collapse_handler(request: Dict[str, Any]) -> list[float]:
        alpha_G = request.get("alpha_G", 1.0)
        return simulate_collapse(alpha_G)

    def wisdom_handler(request: Dict[str, Any]) -> list[Dict[str, str]]:
        query = request.get("query", "")
        limit = request.get("limit", 5)
        db = WisdomDatabase()
        return db.search(query, limit=limit)

    # Create and start server
    server = AINodeServer(host=args.host, port=args.port)
    server.register_task("quantum", quantum_handler)
    server.register_task("collapse", collapse_handler)
    server.register_task("wisdom", wisdom_handler)

    # Start server in a thread to allow KeyboardInterrupt
    server_thread = threading.Thread(target=server.start, daemon=True)
    server_thread.start()

    try:
        server_thread.join()
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
        server.stop()


def run_api(args: argparse.Namespace) -> None:
    """Start the Flask API server."""
    app = create_app()
    logger.info(f"Starting LYRA AI Flask API on {args.host}:{args.port}")
    app.run(host=args.host, port=args.port, debug=args.debug)


def main() -> None:
    """Parse arguments and execute the appropriate command."""
    parser = argparse.ArgumentParser(
        description=(
            "LYRA AI: Quantum-inspired AI framework for empathy, wisdom, "
            "and distributed computing."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m lyra --quantum --theta 0.5
  python -m lyra --collapse --alpha-G 1.0
  python -m lyra --wisdom --query "life"
  python -m lyra --server --port 9999
  python -m lyra --api --port 5000 --debug
        """
    )

    # Subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Quantum simulation command
    quantum_parser = subparsers.add_parser(
        "quantum",
        help="Run a quantum circuit simulation"
    )
    quantum_parser.add_argument(
        "--theta",
        type=float,
        default=0.0,
        help="Rotation angle in radians for the RX gate (default: 0.0)"
    )

    # Collapse simulation command
    collapse_parser = subparsers.add_parser(
        "collapse",
        help="Simulate informational collapse dynamics"
    )
    collapse_parser.add_argument(
        "--alpha-G",
        type=float,
        default=1.0,
        help="Coupling constant for the collapse process (default: 1.0)"
    )

    # Wisdom search command
    wisdom_parser = subparsers.add_parser(
        "wisdom",
        help="Search the wisdom database"
    )
    wisdom_parser.add_argument(
        "--query",
        type=str,
        required=True,
        help="Search term for wisdom quotes"
    )
    wisdom_parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Maximum number of results to return (default: 5)"
    )

    # Server command
    server_parser = subparsers.add_parser(
        "server",
        help="Start the AI Node Server"
    )
    server_parser.add_argument(
        "--host",
        type=str,
        default="localhost",
        help="Host address to bind the server to (default: localhost)"
    )
    server_parser.add_argument(
        "--port",
        type=int,
        default=9999,
        help="Port to bind the server to (default: 9999)"
    )

    # API command
    api_parser = subparsers.add_parser(
        "api",
        help="Start the Flask API server"
    )
    api_parser.add_argument(
        "--host",
        type=str,
        default="localhost",
        help="Host address to bind the API to (default: localhost)"
    )
    api_parser.add_argument(
        "--port",
        type=int,
        default=5000,
        help="Port to bind the API to (default: 5000)"
    )
    api_parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable Flask debug mode (default: False)"
    )

    # Parse arguments
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Execute the appropriate command
    if args.command == "quantum":
        run_quantum_simulation(args)
    elif args.command == "collapse":
        run_collapse_simulation(args)
    elif args.command == "wisdom":
        run_wisdom_search(args)
    elif args.command == "server":
        run_server(args)
    elif args.command == "api":
        run_api(args)
    elif args.command == "server":
        run_server(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
