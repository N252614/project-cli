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
### Files
 • main.py — CLI entry point
 • models/ — user, project, and task classes
 • utils/ — helper functions
 • data/ — JSON files with saved data

⸻

### Author
Nataliya Katina