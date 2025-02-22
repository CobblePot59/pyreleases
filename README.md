# pyreleases

This project provides a command-line tool to facilitate the deployment of a Python application. It allows you to generate either a Docker container or a systemd service package (.deb) from your Python code located in the `src` directory. The generated files are placed in the `releases` directory.

## Getting Started

1. **Clone the repository:**

```bash
   git clone https://github.com/CobblePot59/pyreleases.git
   cd pyreleases
```

2. **Set up your environment variables:** Make sure to set the following environment variables before running the tool:

- `APP_NAME`: The name of your application.
- `PORT`: The port your application will run on.
- `MAIN`: The main Python file to be executed.

You can create a `.env` file in the root of your project with the following content:

```env
APP_NAME=hello
PORT=80
MAIN=wsgi.py
```

3. **Build the Docker image:** Run the following command to build the Docker image:

```bash
  sudo docker build -t pyreleases .
```

4. **Run the tool to generate the desired output:**

To generate a Docker setup, run:

```bash
  sudo docker run --rm --env-file .env -v $(pwd)/releases:/opt/releases pyreleases -o docker
```

To generate a systemd service package, run:

```bash
    sudo docker run --rm --env-file .env -v $(pwd)/releases:/opt/releases pyreleases -o systemd
```

## Output

- If you choose `docker`, the following files will be generated in the `releases/docker` directory:
  - `docker-compose.yml`
  - `Dockerfile`
  
  Additionally, your application source code will be copied to `releases/docker/volumes/app`.

- If you choose `systemd`, a `.deb` package will be created in the `releases/systemd` directory, along with the necessary service files.
