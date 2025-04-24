# Action Suggester API

This is a Django-based API for analyzing user messages, extracting tone and intent using an LLM (Google Gemini), and suggesting relevant actions. It logs the query details, including the analysis and suggested actions, to a PostgreSQL database.

## Project Overview

The Action Suggester API analyzes a short user text message (e.g., "I want to order pizza") to determine its tone (e.g., Happy, Urgent) and intent (e.g., Order Food, Ask Question). Based on this analysis, the API suggests relevant actions and stores the data in a PostgreSQL database.

### Core Features:
- Analyzes tone and intent using Google Gemini LLM API.
- Suggests relevant actions based on the identified tone and intent.
- Logs query, analysis, and suggestions in the PostgreSQL database.

## API Endpoint

### `POST /api/analyze/`

**Request Body:**
```json
{
  "query": "Your text message here"
}
```

**Response Body:**
```json
{
  "query": "User's message",
  "analysis": {
    "tone": "Identified Tone",
    "intent": "Identified Intent"
  },
  "suggested_actions": [
    {"action_code": "ACTION_1", "display_text": "Suggestion 1"},
    {"action_code": "ACTION_2", "display_text": "Suggestion 2"},
    {"action_code": "ACTION_3", "display_text": "Suggestion 3"}
  ]
}
```

## Project Setup
Follow the steps below to set up the project locally:

1. **Install PostgreSQL**  
   Ensure that PostgreSQL is installed on your machine. If you don't have it, you can download it from [here](https://www.postgresql.org/download/).

2. **Create a PostgreSQL Database**  
   You need to manually create a PostgreSQL database for the project. You can use pgAdmin or run the following SQL commands in `psql`:

   ```sql
   CREATE DATABASE actionsuggester;
   ```

3. **Set Up the Project**  
   - **Step 1: Clone the Repository**  
     Clone the project from GitHub:

     ```bash
     git clone https://github.com/yourusername/actionsuggester.git
     cd actionsuggester
     ```

    Add Your Database Credentials
    ```json
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'actionsuggester',
                'USER': 'your_username',
                'PASSWORD': 'your_password',
                'HOST': 'localhost',
                'PORT': '5432',
            }
        }
        Replace 'your_username' and 'your_password' with your actual PostgreSQL credentials.
    ```

   - **Step 2: Create a Virtual Environment**  
     - **Windows (via .bat script):**  
       Run the `setup.bat` file to automatically create a virtual environment, install dependencies, and set up the project.

     - **Linux/MacOS:**  
       ```bash
       python3 -m venv env
       source env/bin/activate
       ```

   - **Step 3: Install Dependencies**  
     Install the required packages:

     ```bash
     pip install -r requirements.txt
     ```

   - **Step 4: Configure the Environment Variables**  
     Rename the `.example.env` file to `.env` and set up the necessary environment variables. Ensure your `.env` file contains the following keys:

     ```ini
     GEMINI_API_KEY=your_google_gemini_api_key
     ```

     Replace `your_google_gemini_api_key` with your actual Gemini API key.

   - **Step 5: Apply Database Migrations**  
     Run the following commands to create the necessary tables in your PostgreSQL database:

     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```

1. **Run the Development Server**  
   To run the development server, use the following command:

   ```bash
   python manage.py runserver
   ```

   You can now test the API endpoint at `http://127.0.0.1:8000/api/analyze/`.

## Testing
You can use tools like Postman/Httpie or cURL to test the API:

- **POST request to `http://127.0.0.1:8000/api/analyze/`:**

  Example Request:

  ```json
  {
    "query": "I want to order pizza"
  }
  ```

  Example Response:

  ```json
  {
    "query": "I want to order pizza",
    "analysis": {
      "tone": "Neutral",
      "intent": "Order Food"
    },
    "suggested_actions": [
      {"action_code": "ORDER_FOOD", "display_text": "Order Food Online"},
      {"action_code": "FIND_RECIPE", "display_text": "Find Pizza Recipes"}
    ]
  }
  ```

## Database Schema
The database stores the following fields in the `QueryLog` table:

- `id`: Primary Key (Auto Increment)
- `query`: Text of the user's query.
- `timestamp`: Date and time when the query was processed.
- `tone`: Detected tone of the message (e.g., Happy, Sad).
- `intent`: Detected intent of the message (e.g., Order Food, Ask Question).
- `suggested_actions`: A list of suggested actions based on the tone and intent (stored as JSON).

Example Database Table:

| id  | query                     | timestamp           | tone    | intent      | suggested_actions                                                                 |
|-----|---------------------------|---------------------|---------|-------------|-----------------------------------------------------------------------------------|
| 1   | I want to order a pizza   | 2025-04-24 12:00:00 | Neutral | Order Food  | [{"action_code": "ORDER_FOOD", "display_text": "Order Food Online"}, {"action_code": "FIND_RECIPE", "display_text": "Find Pizza Recipes"}] |

## Requirements
- Python 3.x
- PostgreSQL
- Google Gemini API Key

## Install Dependencies
```bash
pip install -r requirements.txt
```

## Known Issues and Troubleshooting
- **404 Gemini API error:** - Ensure that you are using a valid Gemini API model and key in the `.env` file.
                            - The `/actionsuggester/api/models_google.py` script retrieves all available models from the Google AI platform.    
- **JSONDecodeError:** If the Gemini response format changes or is malformed, check the API call or inspect the raw response for errors.

