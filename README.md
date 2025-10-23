# Project CLI Tool
Command line tool for managing **users**, **projects**, and **tasks**.  
---
## Features
- Add and list users  
- Add and list projects  
- Add, list, and complete tasks  
- Save data in JSON files  
- Uses `rich` for colorful console output
---
## How to Run
1. Activate virtual environment:
   ```bash
   source .venv/bin/activate

2. Run commands:
Add user:
```bash
python main.py add-user --name "Alex" --email "alex@example.com"
```
List users:
```bash
python main.py list-users
```
Add project:
```bash
python main.py add-project --user "Alex" --title "CLI Tool"
```
List projects:
```bash
python main.py list-projects
```
Add task:
```bash
python main.py add-task --project "CLI Tool" --title "Write README" --assigned-to "Alex"
```
List tasks:
```bash
python main.py list-tasks
```
Mark task as done:
```bash
python main.py complete-task --id 1
```
## Testing

Run tests with pytest:

```bash
source .venv/bin/activate
pytest -v
```

### Files
 - **main.py** — entry point for the CLI application. Handles commands (`add-user`, `add-project`, `add-task`, etc.).
- **models/** — contains data model classes (`User`, `Project`, `Task`) representing core entities.
- **utils/** — helper functions for printing tables, saving/loading JSON files, and general utilities.
- **data/** — folder with stored JSON files (`users.json`, `projects.json`, `tasks.json`) that keep persistent data between sessions.
- **tests/** — contains automated tests (`test_main.py`) verifying CLI behavior with `pytest`.
- **requirements.txt** — list of Python dependencies used in the project.
- **README.md** — documentation with usage instructions and author info.

⸻

### Author
Nataliya Katina