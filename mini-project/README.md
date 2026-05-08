Mini Project: Monster Data Validation
Overview
This project is part of my ongoing learning in SQL, Python, data validation, and QA automation.
I built a small framework that compares data from a simulated pipeline (SQLite) against a “golden truth” CSV file. The goal is to practice:

validating data quality

detecting differences

writing automated tests

organizing Python modules

understanding how data pipelines can be tested

I’m still learning many of the tools used here, but everything in this project reflects real progress in my QA and data engineering skills.

Project Structure
Code
mini-project/
├── framework/              # Core validation framework (Python modules I'm learning to build)
│   ├── data_loader.py     # Loads data from SQLite & CSV
│   ├── validators.py      # Validation & comparison logic
│   ├── api_client.py      # Placeholder for future learning
│   ├── config.py          # Placeholder for configuration experiments
│   └── __init__.py
│
├── tests/                  # Pytest test suites (I'm learning how these work)
│   ├── test_monsters_perfect.py
│   ├── test_monsters_diffs.py
│   └── __init__.py
│
├── data/
│   ├── actual/            # Simulated pipeline outputs
│   └── expected/          # Golden truth CSV
│
├── basic_python_exercises.py   # My Python practice file
├── .gitignore
└── README.md
Framework Components
DataLoader (framework/data_loader.py)
What I’m learning here:

how to load data from SQLite

how to read CSV files

how to return structured Python objects

how to organize code into modules

Validators (framework/validators.py)
What I’m practicing:

comparing rows and columns

checking for differences

thinking like a QA engineer in Python

building reusable validation functions

Test Suites
test_monsters_perfect.py
This test checks the GOOD dataset:

loads monsters.sqlite

compares it to monsters.csv

expected result: all tests pass

I’m learning how pytest discovers and runs tests.

test_monsters_diffs.py
This test checks the BAD dataset:

loads monsters_bad.sqlite

compares it to monsters.csv

expected result: differences are found

This helps me understand how validation failures are reported.

Running Tests (with learning notes)
bash
# Run all tests
pytest tests/
This runs every test in the project.

bash
# Run a specific test file
pytest tests/test_monsters_perfect.py
Useful when I only want to check one dataset.

bash
# Run with verbose output (shows each test name)
pytest tests/ -v
I didn’t know what “verbose” meant at first — it just prints more detail.

bash
# Run with coverage (shows which files the tests executed)
pytest tests/ --cov=framework
I’m still learning how to interpret coverage reports, but this command works.

Running Python Exercises
bash
python basic_python_exercises.py
This file is where I practice Python syntax, functions, loops, and other basics.

Skills I’m Practicing
Data validation & ETL testing

SQLite querying

CSV processing

Python modules and functions

Pytest basics

Organizing code into a small framework

Thinking through QA logic in Python

Detecting and reporting data differences

Future Enhancements (learning goals)
[ ] Build an API client (api_client.py)

[ ] Add configuration management (config.py)

[ ] Add more data transformation steps

[ ] Validate SQL queries

[ ] Add performance tests

[ ] Improve error reporting

Notes
This project is part of my SQL and Python learning journey.
I’m using it to practice real QA concepts in a small, controlled environment.
As I learn more, I plan to expand the framework and add more validation rules.
