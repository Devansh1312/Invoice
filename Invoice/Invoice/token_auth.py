from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from urllib.parse import parse_qs
from django.contrib.auth import get_user_model
from django.middleware.csrf import CsrfViewMiddleware
from django.conf import settings

User = get_user_model()

class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        # Extract token from query string or headers
        query_string = scope.get("query_string", b"").decode()
        query_params = parse_qs(query_string)
        token = query_params.get("token", [None])[0]
        
        # Fallback to cookies for web users
        headers = dict(scope.get("headers", []))
        cookies = {}
        if b'cookie' in headers:
            from django.http import SimpleCookie
            cookie = SimpleCookie()
            cookie.load(headers[b'cookie'].decode())
            cookies = {k: v.value for k, v in cookie.items()}
            token = token or cookies.get('access_token')

        # Try JWT token authentication first
        if token:
            try:
                user = await self.get_user_from_token(token)
                if user:
                    scope["user"] = user
                    return await self.inner(scope, receive, send)
            except (InvalidToken, TokenError):
                pass

        # Fallback to session authentication for web users
        if cookies:
            user = await self.get_user_from_session(scope, cookies)
            if user:
                scope["user"] = user
                return await self.inner(scope, receive, send)

        # No valid authentication found
        scope["user"] = AnonymousUser()
        return await self.inner(scope, receive, send)

    @database_sync_to_async
    def get_user_from_token(self, token):
        jwt_auth = JWTAuthentication()
        validated_token = jwt_auth.get_validated_token(token)
        return jwt_auth.get_user(validated_token)

    @database_sync_to_async
    def get_user_from_session(self, scope, cookies):
        from django.contrib.sessions.backends.db import SessionStore
        from django.contrib.auth import SESSION_KEY
        
        session_key = cookies.get(settings.SESSION_COOKIE_NAME)
        if not session_key:
            return None
            
        session = SessionStore(session_key=session_key)
        user_id = session.get(SESSION_KEY)
        if not user_id:
            return None
            
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None