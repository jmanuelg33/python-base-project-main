# Python Base Service

Currently, we run this app locally as follows:
- App gets run in docker
- Database is run locally separately

# Local Development Setup

## 0. Prerequisites

- Docker
  - https://docs.docker.com/desktop/install/mac-install
  - Just create your own account for now
  - Accept all the defaults


## 1. Set up .env file

Follow example.env to create your own file called `.env`

## 2. Build and start the Docker containers:

```
docker-compose up --build
```

You can now test that the service is running:
```
curl localhost:8080/health
```

## 3. Run db migrations
```
docker-compose exec app flask db upgrade
```

## 4. Develop
### Making changes
With the hot-reloading feature implemented, any changes you make to the code will be recognized automatically, eliminating the need to manually rebuild the app.

### Creating interactive containers
You may want to get into a flask or bash shell inside an app container.

flask
```
docker-compose exec app flask shell
```

bash (app service)
```
docker-compose exec app bash
```

bash (postgres service)
```
docker-compose exec postgres bash
```

psql
```
docker-compose exec postgres psql -h localhost -U traxporta -e POSTGRES_PASSWORD=traxporta -d tms_test
```

### Testing
!! Run all tests in a bash shell inside an interactive container (see [Creating interactive containers](#creating-interactive-containers))

run pytest with coverage
```
poetry run pytest --cov=app --cov-report term-missing
```

get coverage report
```
poetry run coverage report
```

### Adding migrations
Migrations are done using [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) a library based on [Alembic](https://alembic.sqlalchemy.org/en/latest/)

If you're adding a new model, first register it in #app/__init__.py `create_app`

To add a new migration just change the model on  `/app/models/`  and run 

```
docker-compose exec app flask db migrate -m "short description of migration"
```

**important!!** check the autogenerated version file for accuracy.

after that run migration with
```
docker-compose exec app flask db upgrade
```
this will add the changes to local database

**important!!** check the database to ensure that the table was created as you expected:
```
shaun@Shauns-MacBook-Pro tms % docker-compose exec postgres psql -h localhost -U traxporta -d tms_test
psql (15.5 (Debian 15.5-1.pgdg120+1))
Type "help" for help.

tms_test=# \d organizations;
                                        Table "public.organizations"
   Column   |            Type             | Collation | Nullable |                 Default                  
------------+-----------------------------+-----------+----------+------------------------------------------
 name       | character varying(80)       |           | not null | 
 id         | character varying(36)       |           | not null | 
 created_at | timestamp without time zone |           |          | timezone('utc'::text, CURRENT_TIMESTAMP)
 updated_at | timestamp without time zone |           |          | timezone('utc'::text, CURRENT_TIMESTAMP)
Indexes:
    "pk_organizations" PRIMARY KEY, btree (id)
    "uq_organizations_id" UNIQUE CONSTRAINT, btree (id)
```

### Changing python dependencies

Yay poetry!

#### Full process
1. Enter a bash shell inside an interactive app service container (see [Creating interactive containers](#creating-interactive-containers))
2. Manage dependencies using Poetry. This will make the changes you need in your file system (so git is good to go) but not apply them to your image. See below for more
3. Re-build the image so your local app runs on the new dependencies

#### using poetry
Check out the [docs](https://python-poetry.org/docs/managing-dependencies/), and you will probably end up with some variation of-

`poetry add <name of package from pip>`

or

`poetry remove <name of package from pip>`

This will:

- update `pyproject.toml`
- update `poetry.lock`
- install the package

# Deployment

## Prod

This app is automatically deployed to prod on merge to `main` using Github Actions

## Dev

Follow these steps to manual deploy to dev environment

### 1. Install Github CLI on your local computer ([Github CLI](https://github.com/cli/cli)) 

`brew install gh`

### 2.  Login to Github using Github CLI

* Launch flow for login `gh auth login`
* `What account do you want to log into?` -> `GitHub.com`
* `What is your preferred protocol for Git operations on this host?` -> Probably `HTTPS` (`SSH` if you know better)
* `Authenticate Git with your GitHub credentials?` -> `Y`
* `How would you like to authenticate GitHub CLI?` -> `Login with a web browser` is the easiest

### 3.  Check login by running command to get all workflows 
`gh workflow list`

### 4.  Create PR and push changes to feature branch

### 5.  Run command to deploy manually to dev environment

`gh workflow run "Feature Pipeline" --ref branch_name -f deploy_env=dev`

Only thing to change in this endpoint is branch_name, you should put yours

