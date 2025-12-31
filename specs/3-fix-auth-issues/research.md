# Research: Fix Authentication & API Issues

**Feature**: Fix Authentication & API Issues
**Date**: 2025-12-30
**Status**: Complete

## Research Questions

### Q1: Better Auth JWT Plugin Configuration

**Question**: How does Better Auth JWT plugin integrate with existing FastAPI JWT validation?

**Finding**:
Better Auth's JWT plugin generates JWT tokens that can be validated by any JWT-compatible library. The key is sharing the same JWT secret between Better Auth and FastAPI.

Better Auth JWT Plugin configuration:
```typescript
jwt({
  jwt: {
    secret: process.env.BETTER_AUTH_SECRET!,
    expiresIn: "7d",
  },
})
```

FastAPI JWT validation:
```python
from fastapi import Depends, HTTPException, Header
import jwt

async def verify_jwt(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    payload = jwt.decode(
        token,
        os.environ["BETTER_AUTH_SECRET"],
        algorithms=["HS256"]
    )
    return payload["sub"]
```

**Decision**: Share `BETTER_AUTH_SECRET` environment variable between frontend and backend.

---

### Q2: JWT Token Format Compatibility

**Question**: Is the JWT "sub" claim a string (Better Auth) or integer (FastAPI expects)?

**Finding**:
Better Auth generates user IDs as strings (UUID format like `user_abc123`). FastAPI's current `get_current_user_id` tries to convert `sub` to `int(user_id_str)` which fails.

Current FastAPI code:
```python
try:
    user_id = int(user_id_str)
except ValueError:
    raise credentials_exception
```

Better Auth token payload:
```json
{
  "sub": "user_abc123",
  "exp": 1234567890,
  "iat": 1234567890
}
```

**Decision**: Update FastAPI to accept string user IDs from JWT. The `user_id` in database can remain integer, but JWT will carry string identifier. Backend will need to:
1. Accept string `sub` claim
2. Query user by string ID or map string ID to integer database ID

---

### Q3: CORS Configuration

**Question**: Is CORS blocking the Authorization header?

**Finding**:
For requests with credentials (including Authorization header), CORS requires:
1. `allow_credentials: True` in CORS config
2. `allow_origins` cannot be `["*"]` - must be specific origins
3. Preflight (OPTIONS) requests must be handled

Current backend CORS config (from `backend/src/main.py`):
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

This looks correct. The `cors_origins_list` should include `http://localhost:3000`.

**Verification**: Check `backend/.env` for `CORS_ORIGINS` includes `http://localhost:3000`.

---

## Key Decisions Summary

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Auth Strategy | Better Auth + FastAPI JWT | Better Auth handles UI auth, FastAPI validates JWT independently |
| JWT Secret | Share BETTER_AUTH_SECRET | Single source of truth for token validation |
| Token Format | Use Better Auth string user ID | Better Auth generates string IDs, backend must adapt |
| CORS Config | `allow_credentials: True` + specific origins | Required for Authorization header to work |
| Token Storage | Better Auth cookies | Better Auth manages session cookies automatically |

## References

- [Better Auth Documentation](https://www.better-auth.com/docs)
- [Better Auth JWT Plugin](https://www.better-auth.com/docs/plugins/jwt)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [CORS with Credentials](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#requests_with_credentials)
