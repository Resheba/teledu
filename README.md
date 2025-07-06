# Deploy

## Docker (recommended)

> `Docker` is required.

1. First of all, we need to build an image:

    ```bash
    docker build -t teledu .
    ```

2. Then, create a `.env` file in the root directory and fill it with the required variables. For more information on `env` variables, see the `.env.example` file.

    ```bash
    TELEGRAM_TOKEN=
    ADMIN_IDS=[]
    CONTACT_URL=https://t.me/username
    TEXTS_PATH=resources/texts.json (optional)
    ```

3. Just run the built image with the command:

   ```bash
   docker run --name=teledu --env-file=.env teledu
   ```

   > *(Optional) I highly recommend protecting your database file using Docker volume. To do so, follow the command below:

    ```bash
    docker run --rm --name=teledu -v "<your\path>\base.sql:\code\base.sql" --env-file=.env teledu
   ```

## Basic

> `Python 3.11` or higher is required.

1. Install all dependencies:

    ```bash
    python -m pip install -r requirements.txt
    ```

2. Run project with the command below:

   ```bash
   python -m src.main
   ```

# Develop

1. Install dependencies:

    ```bash
    python -m pip install pre-commit
    ```

2. Set up pre-commit hooks and venv:

    ```bash
    make init
    ```
