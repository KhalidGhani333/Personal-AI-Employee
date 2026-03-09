"""
Business MCP Server
Production-ready MCP server for external business actions
"""

__version__ = "1.0.0"
__author__ = "AI Employee"
__license__ = "MIT"

from .server import BusinessMCPServer, main

__all__ = ["BusinessMCPServer", "main"]
