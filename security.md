# Security Overview

## Authentication

- Uses JSON Web Tokens (JWT)
- User must log in to access `/chat`
- Tokens are stored in Streamlit's session state

## Token Flow

1. Login → `/login` endpoint verifies credentials
2. If valid → JWT is returned
3. Streamlit stores token securely in memory
4. Token attached to every `/chat` request in `Authorization` header

## Backend Protections

- All endpoints except `/login` require valid JWT
- Signature verified using HS256 and secret key
- Token expiry enforced (default: 1 hour)
- Exception handling returns 401/403 if tampered or expired

## Secrets & Keys

- All keys are stored in `.env` and accessed via `os.getenv()`
- Never committed to version control (listed in `.gitignore`)

## Known Gaps

| Risk                        | Mitigation                          |
|-----------------------------|-------------------------------------|
| No database for user auth   | Use static `users = {...}` for now |
| No HTTPS in local dev       | Deploy via secure proxy/Gateway    |
| No rate limiting            | Consider API Gateway/WAF           |

## Recommendations

- Rotate AWS keys regularly
- Use AWS IAM policies to restrict Bedrock actions
- Move auth to Amazon Cognito or Auth0 for scale
- Set up logging of failed auth attempts
