from abc import ABC, abstractmethod
from typing import List, Union, Callable
from fastapi import Request


class AuthorizationFilter(ABC):
    """Base class for authorization filters"""

    @abstractmethod
    async def authorize(self, user, request: Request) -> bool:
        pass

    def __or__(self, other: "AuthorizationFilter") -> "CompositeFilter":
        return CompositeFilter([self, other], match_any=True)

    def __and__(self, other: "AuthorizationFilter") -> "CompositeFilter":
        return CompositeFilter([self, other], match_any=False)


class RoleFilter(AuthorizationFilter):
    def __init__(self, required_roles: Union[str, List[str]], match_any: bool = False):
        self.required_roles = [required_roles] if isinstance(required_roles, str) else required_roles
        self.match_any = match_any

    async def authorize(self, user, request: Request) -> bool:
        if self.match_any:
            return any(role in user.role.value for role in self.required_roles)
        return all(role in user.role.value for role in self.required_roles)


class PermissionFilter(AuthorizationFilter):
    def __init__(self, required_permissions: Union[str, List[str]], match_any: bool = False):
        self.required_permissions = [required_permissions] if isinstance(required_permissions, str) else required_permissions
        self.match_any = match_any

    async def authorize(self, user, request: Request) -> bool:
        if self.match_any:
            return any(perm in user.permissions for perm in self.required_permissions)
        return all(perm in user.permissions for perm in self.required_permissions)


class CompositeFilter(AuthorizationFilter):
    def __init__(self, filters: List[AuthorizationFilter], match_any: bool = False):
        self.filters = filters
        self.match_any = match_any

    async def authorize(self, user, request: Request) -> bool:
        results = [await f.authorize(user, request) for f in self.filters]
        return any(results) if self.match_any else all(results)


class CustomFilter(AuthorizationFilter):
    def __init__(self, auth_func: Callable[[dict, Request], bool]):
        self.auth_func = auth_func

    async def authorize(self, user, request: Request) -> bool:
        return await self.auth_func(user, request)
