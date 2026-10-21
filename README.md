# CCA 2 To-Do App
A simple Flask and SQLite to-do web application for a CI/CD demonstration.

## Run locally
```bash
python -m venv .venv
# Activate your virtual environment, then:
pip install -r requirements.txt
python app.py
```
Visit http://localhost:5000

## Run tests
```bash
python -m unittest discover -s tests -v
```

## Docker
```bash
docker build -t cca2-todo .
docker run --rm -p 5000:5000 cca2-todo
```

Note: SQLite data stored inside the container is ephemeral unless you mount persistent storage. For this classroom demo, data persistence across Kubernetes pod replacements is not required.
