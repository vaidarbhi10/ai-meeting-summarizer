# AI Meeting Summarizer

## 🌐 Live Website

[AI Meeting Summarizer](https://frontend-j4ehfm1xt-vaidarbhi-goyal.vercel.app)

This repository contains:

- `frontend/`: React + Vite UI
- `BACKEND/`: FastAPI backend with Whisper transcription and Ollama summarization

## Deployment

### Vercel (Frontend)

1. Create a new Vercel project.
2. Connect to this GitHub repository.
3. Set the project root to `frontend`.
4. Use defaults: `npm install` and `npm run build`.
5. Vercel will automatically detect the `vercel.json` file in `frontend/`.

### Render (Backend)

1. Create a new `Web Service` on Render.
2. Connect to this GitHub repository.
3. Use `main` branch.
4. Render will detect `render.yaml` and create both frontend and backend services.

#### Backend notes

- The backend service is configured in `render.yaml`.
- It installs `ffmpeg` and backend dependencies from `BACKEND/requirement.txt`.
- It starts with:
  ```bash
  uvicorn main:app --host 0.0.0.0 --port $PORT
  ```

## Notes

- The frontend is deployed on Vercel as a static site.
- The backend is deployed on Render as a Python web service.
- If you need a custom backend domain, configure Render's service settings.
