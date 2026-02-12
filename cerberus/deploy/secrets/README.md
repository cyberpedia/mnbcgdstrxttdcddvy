# Secrets

Populate these files before deployment:

- `db_password.txt`
- `jwt_secret.txt`
- `signing_secret.txt`

Recommended permissions:

```bash
chmod 600 cerberus/deploy/secrets/*.txt
```

For encrypted-at-rest secret delivery, store encrypted copies in your vault/KMS and materialize these files only at deployment time.
