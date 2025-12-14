from __future__ import annotations

import hashlib
from typing import Any, Dict, Optional


class User:
    """
    User class:
    - Stores username + hashed_password
    - Creates/owns one wallet
    """

    def __init__(self, username: str, hashed_password: str):
        self._username: str = username
        self._hashed_password: str = hashed_password

        # Creates a wallet (import here to avoid circular imports)
        from wallet import Wallet  # wallet.py should exist in your project
        self._wallet = Wallet()

    # -------------------------
    # Username
    # -------------------------
    def set_username(self, name: str) -> None:
        """Updates username (display name)."""
        self._username = name

    def get_username(self) -> str:
        """Returns username."""
        return self._username

    # -------------------------
    # Password
    # -------------------------
    def set_password(self, password: str) -> None:
        """
        Hashes and updates password.
        (Simple SHA-256 hash for a class project.)
        """
        self._hashed_password = self._hash_password(password)

    def verify_password(self, password: str) -> bool:
        """Compares entered password with stored hash (login credential check)."""
        return self._hash_password(password) == self._hashed_password

    @staticmethod
    def _hash_password(password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    # -------------------------
    # Wallet
    # -------------------------
    def get_wallet(self):
        """Returns the wallet object."""
        return self._wallet

    # -------------------------
    # Save / Load
    # -------------------------
    def to_dict(self) -> Dict[str, Any]:
        """Converts user data to dictionary (for saving)."""
        data: Dict[str, Any] = {
            "username": self._username,
            "hashed_password": self._hashed_password,
        }

        # Save wallet if it supports to_dict()
        if hasattr(self._wallet, "to_dict"):
            data["wallet"] = self._wallet.to_dict()

        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "User":
        """Restores user from saved dictionary."""
        user = cls(
            username=data.get("username", ""),
            hashed_password=data.get("hashed_password", ""),
        )

        # Restore wallet if present and Wallet supports from_dict()
        wallet_data: Optional[Dict[str, Any]] = data.get("wallet")
        if wallet_data is not None:
            from wallet import Wallet
            if hasattr(Wallet, "from_dict"):
                user._wallet = Wallet.from_dict(wallet_data)

        return user

    # -------------------------
    # Debug
    # -------------------------
    def display_information(self) -> None:
        """Print basic user information (debug)."""
        print(f"User: {self._username}")
        if hasattr(self._wallet, "get_balance"):
            print(f"Balance: {self._wallet.get_balance()}")
