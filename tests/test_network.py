"""Tests for distributed AI networking."""

import socket
import threading
import time
import json
from lyra.network import AINodeServer


class TestAINodeServer:
    """Test cases for AINodeServer class."""

    def test_server_initialization(self):
        """Test server initialization."""
        server = AINodeServer(host="localhost", port=9999)
        assert server.host == "localhost"
        assert server.port == 9999
        assert server.task_handlers == {}
        assert server.server is None
        assert server.running is False

    def test_register_task(self):
        """Test registering a task handler."""
        server = AINodeServer()

        def dummy_handler(request):
            return "test"

        server.register_task("test_task", dummy_handler)
        assert "test_task" in server.task_handlers
        assert server.task_handlers["test_task"] == dummy_handler

    def test_server_start_stop(self):
        """Test starting and stopping the server."""
        server = AINodeServer(host="localhost", port=19999)

        # Start server in a thread
        server_thread = threading.Thread(target=server.start, daemon=True)
        server_thread.start()

        # Give server time to start
        time.sleep(0.1)

        assert server.running is True

        # Stop server
        server.stop()
        time.sleep(0.1)

        assert server.running is False

    def test_client_connection(self):
        """Test client connection and task execution."""
        # Define a simple handler
        def echo_handler(request):
            return {"echo": request.get("message", "")}

        server = AINodeServer(host="localhost", port=19998)
        server.register_task("echo", echo_handler)

        # Start server in a thread
        server_thread = threading.Thread(target=server.start, daemon=True)
        server_thread.start()

        # Give server time to start
        time.sleep(0.5)

        try:
            # Create client socket
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(("localhost", 19998))

            # Send request
            request = json.dumps({"task": "echo", "message": "hello"})
            client.send(request.encode("utf-8"))

            # Receive response
            response = client.recv(4096).decode("utf-8")
            response_data = json.loads(response)

            assert "result" in response_data
            assert response_data["result"]["echo"] == "hello"

            client.close()
        finally:
            server.stop()
            time.sleep(0.1)

    def test_unknown_task(self):
        """Test handling of unknown tasks."""
        server = AINodeServer(host="localhost", port=19997)

        # Start server in a thread
        server_thread = threading.Thread(target=server.start, daemon=True)
        server_thread.start()

        time.sleep(0.5)

        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(("localhost", 19997))

            # Send request with unknown task
            request = json.dumps({"task": "unknown_task"})
            client.send(request.encode("utf-8"))

            response = client.recv(4096).decode("utf-8")
            response_data = json.loads(response)

            assert "error" in response_data
            assert "Unknown task" in response_data["error"]

            client.close()
        finally:
            server.stop()
            time.sleep(0.1)

    def test_invalid_json(self):
        """Test handling of invalid JSON."""
        server = AINodeServer(host="localhost", port=19996)

        server_thread = threading.Thread(target=server.start, daemon=True)
        server_thread.start()

        time.sleep(0.5)

        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(("localhost", 19996))

            # Send invalid JSON
            client.send(b"not valid json")

            response = client.recv(4096).decode("utf-8")
            response_data = json.loads(response)

            assert "error" in response_data
            assert "Invalid JSON" in response_data["error"]

            client.close()
        finally:
            server.stop()
            time.sleep(0.1)

    def test_handler_exception(self):
        """Test handling of exceptions in task handlers."""
        def failing_handler(request):
            raise ValueError("Test error")

        server = AINodeServer(host="localhost", port=19995)
        server.register_task("failing", failing_handler)

        server_thread = threading.Thread(target=server.start, daemon=True)
        server_thread.start()

        time.sleep(0.5)

        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(("localhost", 19995))

            request = json.dumps({"task": "failing"})
            client.send(request.encode("utf-8"))

            response = client.recv(4096).decode("utf-8")
            response_data = json.loads(response)

            assert "error" in response_data
            assert "Test error" in response_data["error"]

            client.close()
        finally:
            server.stop()
            time.sleep(0.1)
