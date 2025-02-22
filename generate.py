import os
import argparse
import shutil
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--output', help='Specify the output', required=True)
args = parser.parse_args()

app_name = os.getenv("APP_NAME")
port = os.getenv("PORT")
main = os.getenv("MAIN")

def run_command(command, check=True):
    try:
        subprocess.run(command, shell=True, check=check, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        exit(1)

if args.output == 'docker':
    templates = {
        "docker-compose.yml": "templates/docker/docker-compose.yml",
        "Dockerfile": "templates/docker/Dockerfile",
    }

    for filename, template_path in templates.items():
        with open(template_path, 'r') as template_file:
            content = template_file.read()
            content = content.replace("${app_name}", app_name)
            content = content.replace("${port}", port)
            content = content.replace("${main}", main)

        with open(f"/opt/releases/docker/{filename}", 'w') as output_file:
            output_file.write(content)

    source_directory = "/opt/pyreleases/src"
    destination_directory = "/opt/releases/docker/volumes/app"
    os.makedirs(destination_directory, exist_ok=True)

    try:
        if os.path.isdir(source_directory):
            for item in os.listdir(source_directory):
                s = os.path.join(source_directory, item)
                d = os.path.join(destination_directory, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, False, None)
                else:
                    shutil.copy2(s, d)
        else:
            print("The source path is invalid.")
    except Exception as e:
        print(f"Error copying directory or file: {e}")

    print("Docker files generated successfully.")

elif args.output == 'systemd':
    templates = {
        f"{app_name}.service": "templates/systemd/app.service",
        "postinst": "templates/systemd/postinst",
        "prerm": "templates/systemd/prerm",
    }

    for filename, template_path in templates.items():
        with open(template_path, 'r') as template_file:
            content = template_file.read()
            content = content.replace("${app_name}", app_name)

        with open(f"templates/systemd/{filename}", 'w') as output_file:
            output_file.write(content)

    run_command("pip install -r /opt/pyreleases/src/requirements.txt")
    run_command(f"pyinstaller --onefile --name {app_name} /opt/pyreleases/src/{main}")
    run_command(f"fpm -s dir -t deb -n {app_name} -v 0.1.0 --after-install templates/systemd/postinst --before-remove templates/systemd/prerm dist/{app_name}=/usr/local/bin/{app_name} templates/systemd/{app_name}.service=/etc/systemd/system/{app_name}.service")
    run_command(f"mv {app_name}_0.1.0_amd64.deb /opt/releases/systemd/")

    print("Systemd files generated successfully.")