from werkzeug.security import generate_password_hash

# Generate hash for the password 'admin123'
password_hash = generate_password_hash('admin123')
print(f"Password hash for 'admin123': {password_hash}")