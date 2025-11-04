# Configuration File Setup

To avoid hardcoding credentials in multiple files, you can use a shared `config.py` file.

## Setup

1. Copy the example config file:
   ```bash
   cp config.py.example config.py
   ```

2. Edit `config.py` and fill in your actual credentials:
   ```python
   organizationId = "your-org-id-here"
   clientId = "your-client-id-here"
   clientSecret = "your-client-secret-here"
   ```

3. In your Python scripts, use placeholders like `<clientId>`, `<clientSecret>`, or `<organizationId>`. The `util.py` functions will automatically load the values from `config.py` if placeholders are detected.

## Example Usage

In your Python files, you can now use placeholders:

```python
import util

organizationId = "<organizationId>"  # Will load from config.py
clientId = "<clientId>"              # Will load from config.py
clientSecret = "<clientSecret>"       # Will load from config.py

# These will automatically use values from config.py
accessToken = util.getAccessToken(clientId, clientSecret)
orgId = util.getOrganizationId(organizationId)
```

## Alternative: Direct Values

You can still provide values directly in your scripts if you prefer:

```python
clientId = "my-actual-client-id"  # Will use this directly
clientSecret = "my-actual-secret"  # Will use this directly
```

## Security Note

- `config.py` is already added to `.gitignore` and will NOT be committed to version control
- `config.py.example` is a template that IS committed (with placeholders)
- Never commit your actual `config.py` file with real credentials!

