AI Assistant

A Django-based AI assistant that explains topics with PPT and video resources fetched from Supabase.



## How to Run
1. Install dependencies: 'pip install -r requirements.txt'
2. Set Supabase credentials in '.env' or 'supabase_client.py'
3. Apply migrations: `python manage.py migrate`
4. Run server: `python manage.py runserver`
5. Open `http://127.0.0.1:8000/` in browser.



## API Endpoint
'POST /ask-jiji/'
Request: '{"question": "RAG"}'
Response:
json
{
"answer": "RAG (Retrieval Augmented Generation) explanation...",
"ppt": [{"title": "RAG Basics", "url": "..."}],
"video": [{"title": "RAG Explained Video", "url": "..."}]
}

## Auth & RLS
1.Profiles table: users can read only their own profile.
2.Queries table: users can insert and read only their own queries.
3.Resources table: publicly readable.
4.RLS policies enforce access control on Supabase tables.

## Improvement with More Time
1.Auto-generate AI explanations for topics without resources.
2.Enhance UI/UX with suggestions, polished formatting, and caching.
