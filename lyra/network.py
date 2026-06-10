"""
Distributed AI networking for smartphone-based computation nodes.
"""

import socket
import threading
import json
import logging
from typing import Callable, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class AINodeServer:
    """
    A socket server for distributed AI computation nodes.

    Attributes:
        host: Host address to bind the server to.
        port: Port to bind the server to.
        task_handlers: Dictionary mapping task names to handler functions.
    """

    def __init__(self, host: str = "localhost", port: int = 9999):
        """
        Initialize the AI Node Server.

        Args:
            host: Host address (default: "localhost").
            port: Port number (default: 9999).
        """
        self.host = host
        self.port = port
        self.task_handlers: dict[str, Callable[[dict], Any]] = {}
        self.server: Optional[socket.socket] = None
        self.running = False

    def register_task(self, task_name: str, handler: Callable[[dict], Any]) -> None:
        """
        Register a task handler for a specific task name.

        Args:
            task_name: Name of the task (e.g., "quantum", "collapse").
            handler: Function to handle the task. Takes a dict (request)
                and returns a result.
        """
        self.task_handlers[task_name] = handler
        logger.info(f"Registered task handler for '{task_name}'")

    def _handle_client(self, client_socket: socket.socket) -> None:
        """
        Handle a client connection.

        Args:
            client_socket: Socket object for the client connection.
        """
        try:
            data = client_socket.recv(4096)
            if not data:
                return

            request = json.loads(data.decode("utf-8"))
            task = request.get("task")

            if task not in self.task_handlers:
                response = {"error": f"Unknown task: {task}"}
            else:
                try:
                    result = self.task_handlers[task](request)
                    response = {"result": result}
                except Exception as e:
                    response = {"error": str(e)}

            client_socket.send(json.dumps(response).encode("utf-8"))
        except json.JSONDecodeError:
            client_socket.send(
                json.dumps({"error": "Invalid JSON"}).encode("utf-8")
            )
        except Exception as e:
            logger.error(f"Error handling client: {e}")
            client_socket.send(
                json.dumps({"error": "Internal server error"}).encode("utf-8")
            )
        finally:
            client_socket.close()

    def start(self) -> None:
        """
        Start the AI Node Server.
        """
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.running = True

        try:
            self.server.bind((self.host, self.port))
            self.server.listen(5)
            logger.info(f"AI Node Server running on {self.host}:{self.port}")

            while self.running:
                client_socket, addr = self.server.accept()
                logger.info(f"Accepted connection from {addr}")
                client_handler = threading.Thread(
                    target=self._handle_client,
                    args=(client_socket,),
                    daemon=True
                )
                client_handler.start()
        except OSError as e:
            logger.error(f"Network binding failed: {e}")
            self.running = False
        except KeyboardInterrupt:
            logger.info("Server shutting down...")
            self.running = False
        finally:
            if self.server:
                self.server.close()

    def stop(self) -> None:
        """
        Stop the AI Node Server.
        """
        self.running = False
        if self.server:
            self.server.close()
        logger.info("AI Node Server stopped")


def ai_node_server(
    host: str = "localhost",
    port: int = 9999,
    task_handlers: Optional[dict[str, Callable[[dict], Any]]] = None
) -> None:
    """
    Legacy function to start an AI Node Server (for backward compatibility).

    Args:
        host: Host address (default: "localhost").
        port: Port number (default: 9999).
        task_handlers: Optional dictionary of task handlers.
    """
    server = AINodeServer(host, port)
    if task_handlers:
        for task_name, handler in task_handlers.items():
            server.register_task(task_name, handler)
    server.start()
