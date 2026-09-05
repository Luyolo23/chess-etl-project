### Chess Data Pipeline ###

This project is an end-to-end ETL pipeline that extracts chess game data from the Lichess public API, transforms it into a structured format, and loads it into a PostgreSQL database. The workflow is orchestrated using Prefect.

The goal of this project was to move beyond theory and build a production-style data pipeline that works with real external data, handles failures, and is fully observable.

### What This Pipeline Does ###

Extract
Pulls chess game data for a given username from the Lichess REST API.

Transform

Parses API responses

Cleans and normalizes the data

Handles missing or inconsistent fields

Structures the data into a tabular format using Pandas

Load
Inserts the cleaned data into a PostgreSQL database table.

Orchestration
Prefect manages task dependencies, logging, execution, and monitoring.

### Architecture ###

Lichess API
↓
Extract Task
↓
Transform Task
↓
Load Task (PostgreSQL)
↓
Prefect Flow Orchestration

### Tech Stack ###

Python

Prefect (workflow orchestration)

PostgreSQL

Pandas

REST APIs (Lichess API)

Linux CLI

### Project Structure ###
chess-etl-project/
│
├── flows.py          # Prefect flow definition
├── extract.py        # API extraction logic
├── transform.py      # Data cleaning & transformation
├── load.py           # PostgreSQL loading logic
├── requirements.txt
└── README.md
### How to Run the Project ###

Create and activate a virtual environment

python -m venv chess_env
source chess_env/bin/activate

Install dependencies

pip install -r requirements.txt

Start Prefect server

prefect server start

Start a worker

prefect worker start -p default

Run the deployment

prefect deployment run chess-pipeline/daily-chess --params '{"username":"YOUR_USERNAME"}'

Open the Prefect UI

http://127.0.0.1:4200
### Key Concepts Practiced ###

External API integration (Lichess)

JSON parsing and schema validation

ETL design patterns

Database integration with PostgreSQL

Workflow orchestration with Prefect

Task-level logging and monitoring

Debugging real-world data inconsistencies

### Challenges Faced ###

Handling inconsistent API responses

Managing flow failures and debugging task-level errors

Structuring the project with clear separation between orchestration and business logic

Configuring and managing Prefect workers locally

### Future Improvements ###

Add retry logic with exponential backoff for API calls

Add a data validation layer before loading

Containerize the project with Docker

Deploy Prefect server to the cloud

Add automated scheduling
