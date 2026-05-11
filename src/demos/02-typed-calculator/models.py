"""Pydantic request/response models for typed MCP tool contracts."""

from __future__ import annotations

from pydantic import BaseModel, Field


class BinaryOpRequest(BaseModel):
    """Inputs shared by all calculator tools in this demo."""

    a: float = Field(description="First operand")
    b: float = Field(description="Second operand")


class BinaryOpResponse(BaseModel):
    """Structured tool output (serialized to JSON for MCP clients)."""

    result: float = Field(description="Numeric result of the operation")
