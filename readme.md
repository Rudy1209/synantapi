# Install Dependencies
pip install -r requirements.txt

# Download NLTK Data
# In your project directory, run the Django shell:
python manage.py shell
# Then, run the following commands:
import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')

# Migrate the Database
python manage.py migrate

# Create a Superuser
python manage.py createsuperuser

# Run the Server
python manage.py runserver

# Generate User Tokens
## Open the Django shell:
python manage.py shell

## Inside the shell, run:
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

## Create a user (replace with your desired username, email, and password)
user = User.objects.create_user('username', 'email@example.com', 'password')

## Generate a token for the user
token, created = Token.objects.get_or_create(user=user)
print(token.key)

### API Endpoints ###
1. Obtain Auth Token
URL :  '/api-token-auth/'
Method : 'POST'
Description : 'Obtain an authentication token by providing a valid username and password.' (made by crearting a superuser)
Request Body : json
{
  "username": "your_username",
  "password": "your_password"
}
Response: json
{
  "token": "your_generated_token"
}

2. Synonym & Antonym Lookup: 
URL : '/api/word/'
Method : 'POST'
Authentication : Token authentication required. Include the token in the 'Authorization' header.
Description : Retrieve synonyms and antonyms for a given word, filtered by an educational dataset.
Request Body : json
{
  "word": "example"
}
Response : json
{
  "word": "example",
  "synonyms": ["illustration", "instance", ...],
  "antonyms": ["opposite_example", ...]
}

## Error Responses ##
400 Bad Request
# When the 'word' parameter is missing:
{
  "error": "Word parameter is missing."
}
# When the word is a bad word:
{
  "error": "The entered word is a bad word. Please enter a different word."
}

### Example Usage ###
# Obtain a Token #
POST http://localhost:8000/api-token-auth/ -H "Content-Type: application/json" -d '{"username": "your_username", "password": "your_password"}'
 
# Response: # JSON
{
  "token": "your_static_token"
}

# Synonym & Antonym Lookup #
POST http://localhost:8000/api/word/ -H "Content-Type: application/json" -H "Authorization: Token your_static_token" -d '{"word": "education"}'
# RESPONSE # JSON
{
  "word": "education",
  "synonyms": ["instruction", "teaching", ...],
  "antonyms": ["ignorance", ...]
}


## Troubleshooting ##
Authentication Credentials Error: Ensure you include the token in the Authorization header.
File Path Issues: Use raw string (r'') or double backslashes for file paths in Windows.

This documentation provides a comprehensive guide to setting up and using the Synonym & Antonym API. Ensure you follow the setup instructions carefully to avoid common pitfalls.






 