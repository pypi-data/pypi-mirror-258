import logging

from pydantic import BaseModel
from typing import Dict, Any, List, Optional, Tuple

logger = logging.getLogger(__name__)


class Request(BaseModel):
    method_name: str
    arguments: Dict[str, Any] = {}
    context: Optional[Any] = None
    timings: List[Tuple[str, float]] = []
    correlation_id: str | None = None
    reply_to: str = ""


class Response(BaseModel):
    result: Optional[Any] = None
    context: Optional[Any] = None
    timings: List[Tuple[str, float]] = []
    reply_to: str = ""