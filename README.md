Backend for VoteCatcher made with [FastAPI](https://fastapi.tiangolo.com/) and [Piccolo ORM](https://www.piccolo-orm.com/) ecosystem.

-------------------------------------------------------

### Installation

Clone repository in fresh virtualenv.

```bash
git clone https://github.com/andrewshaodev/votecatcher.git
cd votecatcher
```

### Initialize project and install requirements (using uv)


```bash
uv sync --all-extras --dev

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

```

### Create database


```bash
sudo -i -u yourpostgresusername psql
CREATE DATABASE votecatcher;
\q;
```

### Setup
-------------------------------------------------------
Create ``.env`` file in root of the project.

```bash
DB_NAME=your db name
DB_USER=your db username
DB_PASSWORD=your db password
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=your secret key
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Migrations

```bash
./scripts/migrations.sh
```

### Create admin user

```bash
./scripts/user.sh
```

Quickly creating a test user:

```bash

piccolo user create --username=admin --password=admin123 --email=admin@example.com --is_admin=t --is_superuser=t --is_active=t

```

### Linting

```bash
./scripts/lint.sh
```

### Getting started 

```bash
./scripts/start.sh
```

After site is running log in as admin user on [localhost:8000/admin/](http://localhost:8000/admin/) and add apikeys etc. 

For non admin user go to API docs [localhost:8000/docs/](http://localhost:8000/docs/) where you can register.

After that you can login with Authorize button to access protected routes.

### Migration:

After updating tables, create the piccolo migration file:

```bash
piccolo migrations new votecatcher --auto
```

Then run:

```bash
./scripts/migrations.sh
```

To update the database
