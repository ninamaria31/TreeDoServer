# TreeDo Server

This is the server for the TreeDo app. It is built using Python and Flask. It uses PostgreSQL as the database.
The corresponding TreeDo Repository can be found [here](https://github.com/ninamaria31/TreeDoList).

## Installation

### Prerequisites

- Python 3.x
- pip
- Virtual environment (recommended)
- PostgreSQL

### Setup

1. Clone the repository:
    ```bash
    git clone <https://github.com/ninamaria31/TreeDoList.git>
    ```

2. Navigate to the project directory:
    ```bash
    cd <project_directory>
    ```

3. (Optional) Create and activate a virtual environment:
    ```bash
    python3 -m venv env
    source env/bin/activate
    ```

4. Install the dependencies from the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```

### PostgreSQL Setup

1. Install PostgreSQL if you haven't already.
2. Create a new database for the project. (postgresql://postgres:example@localhost:5432/tree)
3. (user: postgres, password: example)
4. To create postgresql "tree" table: 
```bash
psql -U postgres
CREATE DATABASE tree;
\q
```

## Usage

To start the server, run:
```bash
python3 app.py
```
