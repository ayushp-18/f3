Deployment guide — invoice-extractor

Summary
- This project is a FastAPI application using `pdf2image` + `pytesseract` and requires system binaries: Poppler (pdfinfo/pdftoppm) and Tesseract-OCR.
- Because of those native dependencies, deploying as a container is the most reliable option. Vercel (serverless) is not recommended for this workload unless you rework the app to avoid native binaries.

Recommended approach (Docker) — works on Render, Fly.io, Railway, Azure Web App for Containers

1) Prepare repository
- Ensure the project is in a Git repo (GitHub/GitLab/Bitbucket).
- Root should contain `Dockerfile` and `requirements.txt` and the `app/` folder.

2) Build and test container locally (Windows PowerShell)
```powershell
# from project root (d:\invoice-2)
docker build -t invoice-extractor:local .
# run container, mount a folder containing test PDFs if needed
docker run --rm -p 8000:8000 -e POPPLER_BIN=/usr/bin -e TESSERACT_CMD=/usr/bin/tesseract invoice-extractor:local
# then test the API
Invoke-RestMethod -Method POST -Uri http://localhost:8000/extract-bill-data -Body (@{document='https://example.com/my.pdf'} | ConvertTo-Json) -ContentType 'application/json'
```

3) Deploy to Render (example)
- Create a Render web service, choose "Docker" as the environment.
- Connect your Git repo and set the build command to `docker build -t invoice-extractor .` (Render autodetects Dockerfile). Render will build and run the container.
- Set environment variables (if needed): `POPPLER_BIN=/usr/bin` and `TESSERACT_CMD=/usr/bin/tesseract`.

4) Deploy to Fly.io (example)
- Install Fly CLI and run `fly launch` from the repo root. Fly will create a `fly.toml` and deploy using the Dockerfile.

Vercel (serverless) — why it's not ideal
- Vercel Functions are sandboxed and do not provide apt package installation or a full container filesystem. Your app depends on native binaries (poppler, tesseract) which are not available by default.
- You could try bundling static Linux binaries into the repo and using a Python Serverless Function on Vercel, but:
  - Binary size and execution limits may block you.
  - You may run into compatibility/sandbox issues.
- If you still want Vercel, consider:
  - Rewriting the OCR pipeline to use a hosted OCR API (e.g., Google Cloud Vision, AWS Textract) and keep a lightweight API on Vercel that calls the hosted OCR service.
  - Or move to Next.js and implement an API route that proxies to a separate service that performs OCR.

Next steps I can do for you
- Create a `Dockerfile` (done).
- Patch `app/main.py` to use environment variables (done).
- Create a `fly.toml` or Render steps if you want a specific provider.
- Help push this repo to GitHub and walk through deploying on Render or Fly.io.

If you want, tell me which host you prefer (Render, Fly.io, Railway, Azure, or Vercel) and I will prepare provider-specific steps and files (e.g., `fly.toml`, Render settings, CI config).