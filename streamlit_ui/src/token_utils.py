import time
import base64
import json
from typing import Any, Dict, Optional, Tuple


class TokenValidator:
    def __init__(self, token_str: Optional[str] = None):
        self.token_str = token_str

    def validate_token_string(self, token_str: Any) -> Dict[str, Any]:
        """
        Validates whether the provided string is a correctly formatted JWT
        and whether it has expired (based on the 'exp' field in the payload).
        It does not verify the cryptographic signature.

        Returns dictionary:
          {
            "is_valid": bool,
            "error": Optional[str],
            "payload": Optional[dict],
            "header": Optional[dict],
          }
        """
        if token_str is None:
            return {
                "is_valid": False,
                "error": "No token provided",
                "payload": None,
                "header": None,
            }
        if not isinstance(token_str, str):
            return {
                "is_valid": False,
                "error": "Token must be a string",
                "payload": None,
                "header": None,
            }
        candidate = token_str.strip()
        if not candidate:
            return {
                "is_valid": False,
                "error": "Pusty token",
                "payload": None,
                "header": None,
            }
        if "." not in candidate:
            return {
                "is_valid": False,
                "error": "Not a valid token type",
                "payload": None,
                "header": None,
            }

        header, payload = self._decode_jwt_parts(candidate)
        if header is None or payload is None:
            return {
                "is_valid": False,
                "error": "Cannot decode payload!",
                "payload": None,
                "header": None,
            }

        if not self._token_valid_exp(payload):
            return {
                "is_valid": False,
                "error": "Token expired!",
                "payload": payload,
                "header": header,
            }

        return {
            "is_valid": True,
            "error": None,
            "payload": payload,
            "header": header,
        }

    @staticmethod
    def _token_valid_exp(token_info: dict) -> bool:
        """
        Checks whether a JWT token (decoded payload) is still valid.
        Expects the token payload to contain an ``exp`` claim with a UNIX timestamp.
        """
        exp = token_info.get("exp")
        if exp is None:
            # No expiration claim – consider it invalid
            return False
        # Compare expiration time with the current UTC timestamp
        return exp > int(time.time())

    @staticmethod
    def _b64url_decode(data: str) -> bytes:
        """
        Decode Base64 URL-safe string with automatic padding handling.
        """
        padding = "=" * (-len(data) % 4)
        return base64.urlsafe_b64decode(data + padding)

    def _decode_jwt_parts(
        self, token_str: str
    ) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
        """
        Trying to decode the JWT header and payload without signature verification.
        It returns a tuple (header, payload) or (None, None) if it fails.
        """
        try:
            parts = token_str.split(".")
            if len(parts) != 3 or not all(parts):
                return None, None
            header_raw = self._b64url_decode(parts[0])
            payload_raw = self._b64url_decode(parts[1])
            header = json.loads(header_raw.decode("utf-8"))
            payload = json.loads(payload_raw.decode("utf-8"))
            if not isinstance(header, dict) or not isinstance(payload, dict):
                return None, None
            return header, payload
        except Exception:
            return None, None
