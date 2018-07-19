# StupidMart

暑期实训作业

## Quickstart

First, set your app's secret key as an environment variable. For example, add the following to `.bashrc` or `.bash_profile`.

``` {.sourceCode .bash}
export STUPIDMART_SECRET='something-really-secret'
```

Run the following commands to bootstrap your environment :

    git clone https://github.com/Zhiwei1996/StupidMart
    cd StupidMart
    pip install -r requirements/dev.txt

In general, before running shell commands, set the `FLASK_APP` and `FLASK_DEBUG` environment variables :

    export FLASK_APP=/path/to/autoapp.py
    export FLASK_DEBUG=1

Configure your sqlalchemy url in `settings.py` and create you database named `stupidmart`

```bash
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@host/stupidmart'
```

Once you have installed your DBMS, run the following to create your app's database tables and perform the initial migration :

    flask db init
    flask db migrate
    flask db upgrade
    flask run deploy

## Deployment

To deploy:

    export FLASK_DEBUG=0   # With setting to 1 you can use DebugToolbar
    
    flask run       # start the flask server

In your production environment, make sure the `FLASK_DEBUG` environment variable is unset or is set to `0`, so that `ProdConfig` is used.

## Shell

To open the interactive shell, run :

    flask shell

By default, you will have access to the flask `app`.

## Running Tests

To run all tests, run :

    flask test  # Write your own test codes, and then use this command to test 

## Migrations

Whenever a database migration needs to be made. Run the following commands :

    flask db migrate

This will generate a new migration script. Then run :

    flask db upgrade

To apply the migration.

For a full migration command reference, run `flask db --help`.

## Asset Management

Files placed inside the `assets` directory and its subdirectories (excluding `js` and `css`) will be copied by webpack's `file-loader` into the `static/build` directory, with hashes of their contents appended to their names. For instance, if you have the file `assets/img/favicon.ico`, this will get copied into something like `static/build/img/favicon.fec40b1d14528bf9179da3b6b78079ad.ico`. You can then put this line into your header:

    <link rel="shortcut icon" href="{{asset_url_for('img/favicon.ico') }}">

to refer to it inside your HTML page. If all of your static files are managed this way, then their filenames will change whenever their contents do, and you can ask Flask to tell web browsers that they should cache all your assets forever by including the following line in your `settings.py`:

    SEND_FILE_MAX_AGE_DEFAULT = 31556926  # one year
