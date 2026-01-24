# SPDX-License-Identifier: MIT
# Copyright (c) 2024-2026 Xerolux
#
# This file contains encrypted logic for IDM Heat Pump authentication.
# The code is obfuscated to protect the authentication algorithm implementation.
#
# SECURITY NOTE: This module uses encrypted code execution which is a security risk.
# Consider replacing with a proper authentication module in the future.

import logging
import ast
from cryptography.fernet import Fernet

logger = logging.getLogger(__name__)

# Encrypted payload containing the technician code generation logic
_PAYLOAD = b"gAAAAABpZpu99iZL1togZnYCNBbiIiNrxrGuSkNnYUfRG1nL5JbHoTkeMjPkgdJcJZzX0VZC5-uGpXh9B9m9HVw3t2Fd3FyufU4uFsaBJDALpvrf3ZKMj4fgC0mvD7CMtUjtxx8qAFHGiHG9omleEfGAcsra9JxEHAlmR7l1OCk0Tne5rQCXT5EwgUrk8wW2e_I43FGngb43yGpwPLzl5_z5T00s9_FaTzrOaUAH34QwvdwNrHkHHKj4ARZbYTtKPNbYIHTQg8CqFmd5kxC7CyzIbW8mw_1KgA789pOBSyj5vuGbnVoWqZo4iKCj1k_eJB7XyHN5mWX1WkPOrC_PYJJOVKtgHtfMj95xGzAJQmycvIkbrxHEIoHXSToP8WMIHK6JLDsWDQFZAo34obz3C6HIrS-G1OcjAxVlvVEXOJax-iLmfbdcEvpd4uB1XDbqdWLLyOVYw5RNWDxHv6k27ybn1APivlJDgIMtKZOMl-KaDeXrb2Gsg2Y81EKAUagdQ1PrILty_HGWgkhaWnUBq1XUXuUcKB4IIAGUb27R-IOlmYVq0HCsV1X8JgDWAQFKs38x6egvmGy7GXDUL2WLwigR6EE5peNN1ZG0fapRotMS58V6HUF1Sa-irRQZPXD5I95rMceS42YvoWwsW4zqGvZm4AAANZmQWrMPE2-bpAYY7Ly5UxubgUUqrt1LmrjAu_a6Ob4J3dX_2VYQqnJ_1UdWTom25hp4kf9nqzY75IhNS-UWDAchfeEg__ntdnsYW7JVR7PR_XXQgk2XW953puZrF5Vy9t_orG2Vwj50Lwh9aaWDJ-6ZwfaoVUMYiiArzG28HctSgTlJDCslUPCGljEs5DF_bjw-Xg=="

# Restricted namespace for code execution (security hardening)
_ALLOWED_BUILTINS = {
    "int": int,
    "str": str,
    "len": len,
    "range": range,
    "abs": abs,
    "min": min,
    "max": max,
    "sum": sum,
    "pow": pow,
    "divmod": divmod,
    "round": round,
    "format": format,
    "chr": chr,
    "ord": ord,
    "hex": hex,
    "bin": bin,
    "True": True,
    "False": False,
    "None": None,
}


def _get_key():
    # Key reconstruction for in-memory decryption
    # Part 1: iYYeyAs
    k1 = "iYYeyAs"
    # Part 2: 9MbBuLxzH
    k2 = "9MbBuLxzH"
    # Part 3: Anacdiqd2h9f
    k3 = "Anacdiqd2h9f"
    # Part 4: N4UaeAYKPHxYZ0E=
    k4 = "N4UaeAYKPHxYZ0E="
    return (k1 + k2 + k3 + k4).encode()


def _validate_code(code_str: str) -> bool:
    """
    Validate decrypted code using AST parsing.
    Rejects code with dangerous constructs like imports, exec, eval, etc.
    """
    try:
        tree = ast.parse(code_str)
        for node in ast.walk(tree):
            # Block imports
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                logger.error("Security: Import statements not allowed")
                return False
            # Block dangerous function calls
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in ("exec", "eval", "compile", "__import__", "open"):
                        logger.error(f"Security: {node.func.id}() not allowed")
                        return False
        return True
    except SyntaxError as e:
        logger.error(f"Security: Code validation failed: {e}")
        return False


# Module-level namespace for executed code
_module_namespace = {"__builtins__": _ALLOWED_BUILTINS}

try:
    _cipher_suite = Fernet(_get_key())
    _decrypted_code = _cipher_suite.decrypt(_PAYLOAD).decode("utf-8")

    # Security: Validate code before execution
    if _validate_code(_decrypted_code):
        # Compile first to catch syntax errors
        _compiled_code = compile(_decrypted_code, "<technician_auth>", "exec")
        # Execute with restricted namespace
        exec(_compiled_code, _module_namespace)
        # Export any defined functions to module level
        for name, obj in _module_namespace.items():
            if callable(obj) and not name.startswith("_"):
                globals()[name] = obj
    else:
        logger.error("Authentication code validation failed")
except Exception as e:
    # Log error type but not details to prevent analysis
    logger.error(f"Authentication logic error: {type(e).__name__}")


def calculate_codes():
    """Fallback if decryption fails - returns empty codes."""
    if "calculate_codes" in _module_namespace:
        return _module_namespace["calculate_codes"]()
    return {"code1": "ERROR", "code2": "ERROR", "code3": "ERROR"}
