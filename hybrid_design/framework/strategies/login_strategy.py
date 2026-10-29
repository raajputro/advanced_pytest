"""Strategy: vary credentials/scenarios while reusing the same UI interaction."""
from abc import ABC, abstractmethod
from framework.pages.login_page import LoginPage


class LoginStrategy(ABC):
    @abstractmethod
    async def authenticate(self, login_page: LoginPage) -> None: ...


class StandardLogin(LoginStrategy):
    async def authenticate(self, login_page: LoginPage) -> None:
        await login_page.submit("standard_user", "secret_sauce")


class LockedOutLogin(LoginStrategy):
    async def authenticate(self, login_page: LoginPage) -> None:
        await login_page.submit("locked_out_user", "secret_sauce")
