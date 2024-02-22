import json
import os
import os.path
import sys
from pathlib import Path

import pexpect
import typer
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from rich import print
from rich.console import Console
from rich.table import Table
from typing_extensions import Annotated

app = typer.Typer()
console = Console()
data = {}


def run_cli():
    global data
    PATH = os.path.dirname(__file__)
    config_filename = f"{PATH}/config.json"
    if not os.path.exists(config_filename):
        with open(config_filename, "w") as f:
            json.dump({}, f)
    data = json.loads(open(config_filename, "r").read())
    app()


def select_environment_option():
    options = data.keys()
    if len(options) == 0:
        print("No Environment found!!!")
        sys.exit()
    completer = WordCompleter(options)
    selected_option = prompt("Select an environment: ", completer=completer)
    return selected_option


def select_server_option(environment):
    options = data.get(environment, {}).keys()
    if len(options) == 0:
        print("No Server found!!!")
        sys.exit()
    completer = WordCompleter(options)
    selected_option = prompt("Select a server: ", completer=completer)
    return selected_option


def list_environments():
    table = Table("Available Environments")
    for env in data:
        table.add_row(env)
    console.print(table)


def list_servers(environment):
    table = Table("Availbale Servers")
    for server in data.get(environment, {}):
        table.add_row(server)
    console.print(table)


def update_config(data):
    PATH = os.path.dirname(__file__)
    with open(f"{PATH}/config.json", "w") as json_file:
        json.dump(data, json_file)


def is_valid_file(file_path: str):
    if Path(file_path) and Path(file_path).is_file():
        pass
    else:
        print(f"File does not exist or is not a file at location {file_path}")
        sys.exit()


def ssh_interactive_shell(
    hostname, username, bastion_server_data, password=None, port=22, key_file_path=None
):
    try:
        # Spawn SSH session
        ssh_newkey = "Are you sure you want to continue connecting"
        flags = f" -p {port} "
        message = None

        if key_file_path:
            flags += f" -i {key_file_path} "
        if bastion_server_data:
            bastion_server_user = bastion_server_data.get("user")
            bastion_server_host = bastion_server_data.get("host")
            flags += f" -J {bastion_server_user}@{bastion_server_host} "
            message = f"[bold blue]Connecting to target server {username}@{hostname} via bastion server {bastion_server_user}@{bastion_server_host}[/bold blue] :boom:"
        server_connection_command = f"ssh {flags} {username}@{hostname}"
        p = pexpect.spawn(server_connection_command)
        if message:
            print(message)

        # Expect SSH password prompt
        i = p.expect([ssh_newkey, "password:", pexpect.EOF, pexpect.TIMEOUT])
        if i == 0:
            p.sendline("yes")
            i = p.expect([ssh_newkey, "password:", pexpect.EOF, pexpect.TIMEOUT])

        # Enter SSH password
        if i == 1:
            p.sendline(password)
            p.expect("Last login")

        # Interactive shell
        p.interact()

    except pexpect.exceptions.TIMEOUT:
        print("Timeout occurred. Unable to connect to SSH server.")
    except pexpect.exceptions.EOF:
        print("EOF occurred. SSH connection closed unexpectedly.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


@app.command()
def connect_to_server(
    environment: Annotated[
        str,
        typer.Option(help="Environment name", rich_help_panel="Environment name"),
    ],
):
    list_servers(environment)
    server_name = select_server_option(environment)
    if server_name not in data.get(environment):
        print(f"[bold red]ERROR: Server name {server_name} not found![/bold red]")
        sys.exit()
    server_config = data.get(environment, {}).get(server_name)
    user = server_config.get("user")
    host = server_config.get("host")
    key_file_path = server_config.get("key_file")
    bastion_server_data = server_config.get("bastion_data", {})
    print(f"[bold yellow]Environment:{environment} Server:{server_name}![/bold yellow]")
    print(f"[bold green]Connecting to {user}@{host}![/bold green] :boom:")
    ssh_interactive_shell(host, user, bastion_server_data, key_file_path=key_file_path)


@app.command()
def connect():
    list_environments()
    environment = select_environment_option()
    if environment not in data:
        print(f"[bold red]ERROR: Invalid environment {environment}![/bold red] :boom:")
        sys.exit()
    connect_to_server(environment=environment)


@app.command()
def addenv():
    list_environments()
    environment = prompt("New Environment name: ")
    if environment in data:
        print(f"[bold red]ERROR: Environment {environment} already exists![/bold red]")
        sys.exit()
    data[environment] = {}
    update_config(data)


@app.command()
def dlenv():
    list_environments()
    environment = select_environment_option()
    del data[environment]
    update_config(data)


@app.command()
def addserver():
    list_environments()
    environment = select_environment_option()
    list_servers(environment)
    server_name = prompt("New Server name: ")
    if server_name in data.get(environment, {}):
        print(f"[bold red]ERROR: Server {server_name} already exists![/bold red]")
        sys.exit()
    username = prompt("Server username: ")
    hostname = prompt("Server hostname: ")
    key_file = prompt(
        "Custom key path(path should be absolute)(Press enter if no change): "
    )
    if key_file:
        is_valid_file(key_file)
    bastion_server_data = {}
    is_bastion = prompt("Does this server use bastion server y/n: ")
    if is_bastion == "y":
        bastion_username = prompt("Bastion username: ")
        bastion_hostname = prompt("Bastion hostname: ")
        bastion_server_data["user"] = bastion_username
        bastion_server_data["host"] = bastion_hostname
    server_data = {
        "user": username,
        "host": hostname,
        "bastion_data": bastion_server_data,
        "key_file": key_file,
    }
    data[environment][server_name] = server_data
    update_config(data)


@app.command()
def dlserver():
    list_environments()
    environment = select_environment_option()
    list_servers(environment)
    server_name = select_server_option(environment)
    del data[environment][server_name]
    print("[bold green]Success![/bold green] :boom:")
    update_config(data)


@app.command()
def modserver():
    list_environments()
    environment = select_environment_option()
    list_servers(environment)
    server_name = select_server_option(environment)
    server_data = data[environment][server_name]
    user = server_data.get("user")
    host = server_data.get("host")
    print(f"Current Username - [bold]{user}[/bold] Hostname - [bold]{host}[/bold]")
    new_user = prompt("New Username(Press enter if no change): ")
    new_host = prompt("New Hostname(Press enter if no change): ")
    new_keyfile = prompt(
        "New key path(path should be absolute)(Press enter if no change): "
    )
    if new_user:
        server_data["user"] = new_user
    if new_host:
        server_data["host"] = new_host
    if new_keyfile:
        is_valid_file(new_keyfile)
        server_data["key_file"] = new_keyfile
    bastion_server_data = server_data.get("bastion_data", {})
    is_bastion = prompt("Do you want to update bastion server(y/n): ")
    if is_bastion.lower() == "y":
        bastion_username = prompt("New Bastion username(Press enter if no change): ")
        bastion_hostname = prompt("New Bastion hostname(Press enter if no change): ")
        if bastion_username:
            bastion_server_data["user"] = bastion_username
        if bastion_hostname:
            bastion_server_data["host"] = bastion_hostname
        server_data["bastion_data"] = bastion_server_data
    data[environment][server_name] = server_data
    print("[bold green]Success![/bold green] :boom:")
    update_config(data)
