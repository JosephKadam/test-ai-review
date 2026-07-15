# AI Code Reviewer

An intelligent code review tool that integrates with GitHub pull requests to provide
security analysis, architectural feedback, and bug detection using Claude AI.

**Why this is different from basic linting:**
- Understands code *context* across multiple files using AST analysis
- Detects architectural problems, not just syntax errors
- Identifies security vulnerabilities with specific remediation steps
- Tracks code quality metrics over time via a dashboard

---

## How it works

1. You open a PR on GitHub
2. GitHub sends a webhook to this server
3. The server fetches all changed files and builds a rich context (using AST parsing)
4. Claude analyses the context and returns structured suggestions
5. The tool posts a formatted review comment directly on your PR
6. Results are saved to a database and shown on the dashboard

---

## Setup (5 steps, ~20 minutes)

### Step 1 — Clone and install

```bash
git clone https://github.com/YOUR_USERNAME/ai-code-reviewer
cd ai-code-reviewer/backend
pip install -r requirements.txt
```

### Step 2 — Set up your environment variables

```bash
cp .env.example .env
```

Edit `.env` and fill in:
- `ANTHROPIC_API_KEY` — get from https://platform.anthropic.com/api-keys
- `GITHUB_TOKEN` — create at https://github.com/settings/tokens (needs `repo` scope)
- `GITHUB_WEBHOOK_SECRET` — any random string you choose (e.g. run `openssl rand -hex 20`)

### Step 3 — Run locally with ngrok (for testing)

```bash
# Terminal 1 — start the server
cd backend
uvicorn main:app --reload --port 8000

# Terminal 2 — expose it to the internet
# Install ngrok from https://ngrok.com if you don't have it
ngrok http 8000
```

Copy the ngrok HTTPS URL (looks like `https://abc123.ngrok.io`).

### Step 4 — Create a GitHub App

1. Go to https://github.com/settings/apps/new
2. Fill in:
   - **GitHub App name**: `my-ai-reviewer` (must be unique)
   - **Homepage URL**: your ngrok URL
   - **Webhook URL**: `your-ngrok-url/webhook`
   - **Webhook secret**: the same value as `GITHUB_WEBHOOK_SECRET` in your `.env`
3. Set **Repository permissions**:
   - Contents → Read
   - Pull requests → Read & Write
4. Subscribe to events: ✅ Pull request
5. Click **Create GitHub App**
6. Note your **App ID** — add it to `.env` as `GITHUB_APP_ID`
7. Click **Generate a private key** → download the `.pem` file → save as `backend/private-key.pem`
8. Install the app on your test repo: sidebar → **Install App** → choose your repo

### Step 5 — Test it!

Open a pull request on the repo you installed the app on.
Within a few seconds, you should see a review comment appear.

---

## Deploy to Railway (free, permanent URL)

Railway gives you a free tier with a permanent HTTPS URL — no more ngrok needed.

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
cd backend
railway init
railway up
```

Then go to your Railway dashboard → copy the public URL → update your GitHub App's webhook URL.

Set environment variables in Railway dashboard under **Variables**:
- `ANTHROPIC_API_KEY`
- `GITHUB_TOKEN`
- `GITHUB_WEBHOOK_SECRET`
- `GITHUB_APP_ID`

---

## Run the dashboard

```bash
cd dashboard
npm install
npm run dev
```

Open http://localhost:5173 and enter `owner/repo-name` to see your stats.

---

## Project structure

```
ai-code-reviewer/
├── backend/
│   ├── main.py            # FastAPI server + webhook handler
│   ├── github_client.py   # GitHub API (fetch files, post comments)
│   ├── ast_analyzer.py    # Tree-sitter code structure analysis
│   ├── context_builder.py # Assembles multi-file context for the AI
│   ├── ai_engine.py       # Claude API integration
│   ├── classifier.py      # Deduplicates + prioritises suggestions
│   ├── db.py              # SQLite/PostgreSQL storage
│   └── requirements.txt
├── dashboard/
│   └── src/App.jsx        # React metrics dashboard
├── docker-compose.yml
└── .env.example
```

---

## Tech stack

| Component | Technology | Why |
|---|---|---|
| Web server | FastAPI + uvicorn | Async, fast, auto-generates API docs |
| Code parsing | tree-sitter | Language-aware AST, not regex |
| AI analysis | Claude claude-sonnet-4-20250514 | Best code understanding available |
| Database | SQLite (dev) / PostgreSQL (prod) | SQLAlchemy handles both |
| Dashboard | React + Recharts | Fast to build, easy to extend |
| Deployment | Railway | Free tier, one-command deploy |

---

## Adding support for more languages

Edit `ast_analyzer.py` — add the language to `_ast_analyse()` or `_regex_analyse()`.
Then install the tree-sitter grammar: `pip install tree-sitter-java` etc.

---

## Benchmarking your suggestions (for your resume)

To measure precision/recall against real PRs:

1. Pick 50 open source PRs where humans wrote detailed reviews
2. Run your tool on the same PRs
3. Compare: did you find the same issues? Did you have false positives?
4. Track this number as you improve your prompts

A precision rate of 80%+ on security suggestions is genuinely impressive.
