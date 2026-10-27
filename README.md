# CodeReview AI

A Django code review workspace. It supports requirement-based project reviews and quick AI reviews from pasted code, a source file, or a ZIP. Uploaded source is read as text and never executed.

## Run locally on Windows

From the directory containing `manage.py`:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://localhost:8000/` (use `localhost` for Firebase Auth locally). Sign in with the administrator account you created. Use Django Admin at `/admin/` to create mentor and student accounts.

## AI code review and sign-in

- The quick review page offers GenSeraLabs (server-side `GENSARA_API_KEY`) or a local Ollama model. GenSera receives the selected source code; choose Local to keep code on the machine.
- Install [Ollama](https://ollama.com/download), then run `ollama pull qwen2.5-coder:1.5b-instruct`. The app calls Ollama at `http://127.0.0.1:11434`.
- Email/password verification and Google/GitHub sign-in use Firebase Authentication. Enable Email/Password, Google, and GitHub under Firebase Console → Authentication → Sign-in method. For GitHub, set the GitHub OAuth app's Authorization callback URL to `https://difftara-ai-139ec.firebaseapp.com/__/auth/handler`, then enter that app's client ID and secret in Firebase. For Google, make sure the Firebase provider uses the web OAuth client ID/secret from the linked Google Cloud project. Add `localhost`, `127.0.0.1`, and deployed domains to Firebase's authorized domains. Django verifies Firebase ID tokens against Google's signing certificates; no service-account file is needed.
- Set `GENSARA_API_KEY` in the server environment to enable GenSera. Never place it in JavaScript, templates, or Git.

The app uses SQLite by default. For local development, Django creates a temporary secret if `DJANGO_SECRET_KEY` is not set. Set that environment variable to a persistent secret when preserving sessions across restarts. `DJANGO_DEBUG` defaults to `true`; set it to `false` outside local development. `DJANGO_ALLOWED_HOSTS` accepts a comma-separated host list.

## Review workflow

1. A mentor uploads a ZIP file (up to 50 MB) and an optional TXT, PDF, DOCX, or CSV SRS.
2. Enter requirements manually when the SRS does not contain recognizable statements.
3. Run the review to inspect Python files, match requirements, score quality and testing evidence, and generate findings.
4. A mentor can record whether a finding is correct, adjust its final status, and add a comment.
5. Open or print the report. Each run remains in the project review history.

The SRS analyzer applies straightforward rules and can produce false positives or false negatives. AI review suggestions also require human verification; no code is executed and tests are not run.

## Project structure

- `accounts/` — authentication and user roles
- `projects/` — project records, safe ZIP handling, web views, and REST endpoints
- `requirements_app/` — SRS requirements
- `analyzer/` — source inspection, matching, quality checks, and scores
- `reviews/` — review history, findings, overrides, and review workflow
- `reports/` — report model and views
- `activities/` — action history
- `templates/`, `static/` — responsive web interface
- `tests/` — project tests
- `uploads/` — local uploaded and extracted project files
