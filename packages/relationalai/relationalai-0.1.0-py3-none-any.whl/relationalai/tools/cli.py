#pyright: reportPrivateImportUsage=false
from collections import defaultdict
import io
from typing import cast
from click.core import Context
from click.formatting import HelpFormatter
from ..clients.client import ResourceProvider
from .. import Resources
import rich
from rich.console import Console
from rich import box as rich_box
from rich.table import Table
from ..tools import debugger as deb
from ..clients import config, snowflake

import sys
import click
from InquirerPy import inquirer
from pathlib import Path
from .cli_controls import divider, fuzzy, prompt, Spinner

#--------------------------------------------------
# Constants
#--------------------------------------------------

ENGINE_SIZES = ["XS", "S", "M", "L", "XL"]
PROFILE = None

#--------------------------------------------------
# Helpers
#--------------------------------------------------

def get_resource_provider(platform:str|None=None, _cfg:config.Config|None = None) -> ResourceProvider:
    cfg = _cfg or config.Config(PROFILE)
    provider = Resources(cfg=cfg)
    return provider

group_platforms = {
    "imports": ["snowflake"],
    "exports": ["snowflake"],
}

def group_available(group:str) -> bool:
    return group not in group_platforms \
           or config.Config(PROFILE).get("platform", "") in group_platforms[group]

def check_group(group:str):
    if not group_available(group):
        rich.print(f"[yellow]{group.capitalize()} are only available for {', '.join(group_platforms[group])}")
        divider()
        sys.exit(1)

def coming_soon():
    rich.print("[yellow]This isn't quite ready yet, but it's coming soon!")
    divider()
    sys.exit(1)

#--------------------------------------------------
# Custom help printer
#--------------------------------------------------


class RichGroup(click.Group):
    def format_help(self, ctx: Context, formatter: HelpFormatter) -> None:
        sio = io.StringIO()
        console = Console(file=sio, force_terminal=True)
        divider(console)
        console.print("[bold]Welcome to [green]RelationalAI![/bold]")
        console.print()
        console.print("rai [magenta]\\[options][/magenta] [cyan]command[/cyan]")

        console.print()
        console.print("[magenta]--profile[/magenta][dim] - which config profile to use")

        groups = defaultdict(list)
        for command in self.commands.keys():
            if ":" in command:
                group, _ = command.split(":")
                groups[group].append(command)
            else:
                groups[""].append(command)

        console.print()
        for command in groups[""]:
            console.print(f"[cyan]{command}[/cyan][dim] - {self.commands[command].help}")

        for group, commands in groups.items():
            if group:
                console.print()
                if not group_available(group):
                    plats = ", ".join(group_platforms[group])
                    console.print(f"[yellow]Only available for {plats}[/yellow]")
                for command in commands:
                    if group_available(group):
                        console.print(f"[cyan]{command}[/cyan][dim] - {self.commands[command].help}")
                    else:
                        console.print(f"[dim yellow]{command} - {self.commands[command].help}")

        divider(console)
        formatter.write(sio.getvalue())

#--------------------------------------------------
# Main group
#--------------------------------------------------

@click.group(cls=RichGroup)
@click.option("--profile", help="Which config profile to use")
def cli(profile):
    global PROFILE
    PROFILE = profile

#--------------------------------------------------
# Init
#--------------------------------------------------

@cli.command(help="Initialize a new project")
def init():
    init_flow()

#--------------------------------------------------
# Init flow
#--------------------------------------------------

def azure_flow(cfg:config.Config):
    # get the client id and secret
    client_id = inquirer.text("Client ID:", default=cfg.get("client_id", "")).execute()
    client_secret = inquirer.secret("Client Secret:", default=cfg.get("client_secret", "")).execute()
    # setup the default config
    cfg.set("platform", "azure")
    cfg.set("host", "azure.relationalai.com")
    cfg.set("port", "443")
    cfg.set("region", "us-east")
    cfg.set("scheme", "https")
    cfg.set("client_id", client_id)
    cfg.set("client_secret", client_secret)

def snowflake_flow(cfg:config.Config):
    # get account info
    username = inquirer.text("SnowSQL user:", default=cfg.get("snowsql_user", "")).execute()
    password = inquirer.secret("SnowSQL password:", default=cfg.get("snowsql_pwd", "")).execute()
    account = inquirer.text("Snowflake account:", default=cfg.get("account", "")).execute()
    role = inquirer.text("Snowflake role:", default=cfg.get("role", "")).execute()
    # setup the default config
    cfg.set("platform", "snowflake")
    cfg.set("snowsql_user", username)
    cfg.set("snowsql_pwd", password)
    cfg.set("account", account)
    cfg.set("role", role)

def spcs_flow(provider:ResourceProvider, cfg:config.Config):
    if cfg.get("platform") != "snowflake" or (cfg.get("warehouse", "") and cfg.get("rai_app_name", "")):
        return
    with Spinner("Fetching warehouses", "Fetched warehouses"):
        warehouses = cast(snowflake.Resources, provider).list_warehouses()
    print("")
    warehouse = fuzzy("Select a warehouse:", [w["name"] for w in warehouses])
    cfg.set("warehouse", warehouse)

    print("")
    with Spinner("Fetching installed apps", "Fetched apps"):
        apps = cast(snowflake.Resources, provider).list_apps()
    print("")
    app_names = [w["name"] for w in apps]
    if "relationalai" in apps:
        cfg.set("rai_app_name", "relationalai")
    else:
        app = fuzzy("Select RelationalAI app name:", app_names)
        cfg.set("rai_app_name", app)
    provider.reset()
    rich.print("")

def engine_flow(provider:ResourceProvider, cfg:config.Config):
    with Spinner("Fetching engines", "Fetched engines"):
        engines = provider.list_engines()

    engine_names = [engine.get("name") for engine in engines]
    engine_names.insert(0, "Create a new engine")
    print("")
    if len(engine_names) > 1:
        default_engine = cfg.get("engine", "")
        if default_engine not in engine_names:
            default_engine = None
        engine = fuzzy("Select an engine:", choices=engine_names)
    else:
        engine = "Create a new engine"
        rich.print("[green]Looks like you need to create your first engine.")
        rich.print("")
    if engine == "Create a new engine":
        engine = inquirer.text("Engine name:").execute()
        engine_size = fuzzy("Engine size:", choices=ENGINE_SIZES)
        engine_pool = ""
        if cfg.get("platform") == "snowflake":
            provider = cast(snowflake.Resources, provider)
            print("")
            with Spinner("Fetching compute pools", "Fetched compute pools"):
                pools = [v["name"] for v in provider.list_compute_pools()]
            print("")
            engine_pool = fuzzy("Compute pool:", pools)
            cfg.set("compute_pool", engine_pool)
        rich.print("")
        with Spinner(f"Creating '{engine}' engine... (this may take several minutes)", f"Engine '{engine}' created"):
            provider.create_engine(engine, engine_size, engine_pool)
        rich.print("")

    cfg.set("engine", engine)

def gitignore_flow():
    current_dir = Path.cwd()
    while current_dir != Path.home():
        gitignore_path = current_dir / '.gitignore'
        if gitignore_path.exists():
            # if there is, check to see if rai.config is in it
            with open(gitignore_path, 'r') as gitignore_file:
                if 'rai.config' in gitignore_file.read():
                    return
                else:
                    # if it's not, ask to add it
                    add_to_gitignore = inquirer.confirm("Add rai.config in .gitignore?").execute()
                    if add_to_gitignore:
                        with open(gitignore_path, 'a') as gitignore_file:
                            gitignore_file.write("\nrai.config")
                    return
        current_dir = current_dir.parent

def save_flow(cfg:config.Config):
    if cfg.profile in cfg.get_profiles():
        if not inquirer.confirm(f"Overwrite existing {cfg.profile} profile").execute():
            cfg.profile = inquirer.text("Profile name:").execute()
    cfg.save()

def init_flow():
    cfg = config.Config()
    cfg.clone_profile()
    rich.print("\n[dim]---------------------------------------------------\n")
    rich.print("[bold]Welcome to [green]RelationalAI!\n")
    platform = fuzzy("Host platform:", choices=["Snowflake", "Azure (Legacy)"])

    if platform == "Snowflake":
        snowflake_flow(cfg)
    elif platform == "Azure (Legacy)":
        azure_flow(cfg)

    provider = get_resource_provider(None, cfg)
    provider.config = cfg

    rich.print()
    spcs_flow(provider, cfg)
    engine_flow(provider, cfg)
    save_flow(cfg)

    gitignore_flow()
    rich.print("")
    rich.print("[green]✓ rai.config saved!")
    rich.print("\n[dim]---------------------------------------------------\n")

#--------------------------------------------------
# Debugger
#--------------------------------------------------

@cli.command(help="Open the RAI debugger")
def debugger():
    deb.main()

#--------------------------------------------------
# Engine list
#--------------------------------------------------

@cli.command(name="engines:list", help="List all engines")
def engines_list():
    divider(flush=True)
    with Spinner("Fetching engines"):
        engines = get_resource_provider().list_engines()

    if len(engines):
        table = Table(show_header=True, border_style="dim", header_style="bold", box=rich_box.SIMPLE_HEAD)
        table.add_column("Name")
        table.add_column("Size")
        table.add_column("State")
        for engine in engines:
            table.add_row(engine.get("name"), engine.get("size"), engine.get("state"))
        rich.print(table)
    else:
        rich.print("[yellow]No engines found")

    divider()

#--------------------------------------------------
# Engine create
#--------------------------------------------------

@cli.command(name="engines:create", help="Create a new engine")
@click.option("--name", help="Name of the engine")
@click.option("--size", type=click.Choice(ENGINE_SIZES, case_sensitive=False), help="Size of the engine")
def engines_create(name, size):
    divider(flush=True)
    name = prompt("Engine name?", name, newline=True)
    if not size:
        size = fuzzy("Engine size:", choices=ENGINE_SIZES)
        rich.print("")
    provider = get_resource_provider()

    pool = provider.config.get("compute_pool", None, strict=False)
    if provider.config.get("platform") == "snowflake" and not pool:
        pool = prompt("Compute pool?", pool, newline=True)

    with Spinner(f"Creating '{name}' engine... (this may take several minutes)", f"Engine '{name}' created!"):
        provider.create_engine(name, size, pool)
    divider()

#--------------------------------------------------
# Engine delete
#--------------------------------------------------

@cli.command(name="engines:delete", help="Delete an engine")
@click.option("--name", help="Name of the engine")
def engines_delete(name):
    divider(flush=True)
    name = prompt("Engine name?", name, newline=True)
    with Spinner(f"Deleting '{name}' engine", f"Engine '{name}' deleted!"):
        get_resource_provider().delete_engine(name)
    divider()

#--------------------------------------------------
# Object flow
#--------------------------------------------------

def object_flow(provider):
    with Spinner("Fetching databases", "Databases fetched"):
        dbs = provider.list_databases()
    rich.print()
    db = fuzzy("Select a database:", [db["name"] for db in dbs])
    rich.print()

    with Spinner("Fetching schemas", "Schemas fetched"):
        schemas = provider.list_sf_schemas(db)
    rich.print()
    schema = fuzzy("Select a schema:", [s["name"] for s in schemas])
    rich.print()

    with Spinner("Fetching tables", "Tables fetched"):
        tables = provider.list_tables(db, schema)
    rich.print()
    table = fuzzy("Select tables (tab for multiple):", [t["name"] for t in tables], multiselect=True)
    rich.print()
    return db, schema, table

#--------------------------------------------------
# Imports list
#--------------------------------------------------

@cli.command(name="imports:list", help="List objects imported into RAI")
@click.option("--model", help="Model")
def imports_list(model):
    divider(flush=True)
    provider = cast(snowflake.Resources, get_resource_provider())
    check_group("imports")

    if not model:
        with Spinner("Fetching models", "Models fetched"):
            models = provider.list_graphs()
        rich.print()
        model = fuzzy("Select a model:", models)
        rich.print()

    with Spinner(f"Fetching imports for {model}", "Imports fetched"):
        imports = provider.list_imports(model)

    rich.print()
    if len(imports):
        table = Table(show_header=True, border_style="dim", header_style="bold", box=rich_box.SIMPLE_HEAD)
        table.add_column("Import")
        for imp in imports:
            table.add_row(imp.get("name"))
        rich.print(table)
    else:
        rich.print("[yellow]No imports found")

    divider()

#--------------------------------------------------
# Imports stream
#--------------------------------------------------

@cli.command(name="imports:stream", help="Stream an object into RAI")
@click.option("--object", help="Object")
@click.option("--model", help="Model")
@click.option("--rate", help="Rate")
def imports_stream(object, model, rate):
    divider(flush=True)
    provider = cast(snowflake.Resources, get_resource_provider())
    check_group("imports")

    if not model:
        with Spinner("Fetching models", "Models fetched"):
            models = provider.list_graphs()
        rich.print()
        model = fuzzy("Select a model:", models)
        rich.print()

    if not object:
        db, schema, table = object_flow(provider)
        for t in table:
            obj = f"{db}.{schema}.{t}"
            with Spinner(f"Creating stream for {obj}", f"Stream for {obj} created"):
                provider.create_import_stream(obj, model, rate)
    else:
        with Spinner(f"Creating stream for {object}", f"Stream for {object} created"):
            provider.create_import_stream(object, model, rate)

    divider()

#--------------------------------------------------
# Imports delete
#--------------------------------------------------

@cli.command(name="imports:delete", help="Delete an import from RAI")
@click.option("--object", help="Object")
@click.option("--model", help="Model")
def imports_delete(object, model):
    divider(flush=True)
    provider = cast(snowflake.Resources, get_resource_provider())
    check_group("imports")

    if not model:
        with Spinner("Fetching models", "Models fetched"):
            models = provider.list_graphs()
        rich.print()
        model = fuzzy("Select a model:", models)
        rich.print()

    with Spinner(f"Fetching imports for {model}", "Imports fetched"):
        imports = provider.list_imports(model)

    if not imports:
        rich.print()
        rich.print("[yellow]No imports to delete")
    elif not object:
        rich.print()
        objects = fuzzy("Select objects (tab for multiple):", [t["name"] for t in imports], multiselect=True)
        rich.print()
        for object in objects:
            with Spinner(f"Removing {object}", f"{object} removed"):
                provider.delete_import(object, model)
    else:
        with Spinner(f"Removing {object}", f"{object} removed"):
            provider.delete_import(object, model)

    divider()

#--------------------------------------------------
# Exports list
#--------------------------------------------------

@cli.command(name="exports:list", help="List objects exported out of RAI")
@click.option("--model", help="Model")
def exports_list(model):
    divider(flush=True)
    provider = cast(snowflake.Resources, get_resource_provider())
    coming_soon()
    check_group("exports")

    if not model:
        with Spinner("Fetching models", "Models fetched"):
            models = provider.list_graphs()
        rich.print()
        model = fuzzy("Select a model:", models)
        rich.print()

    with Spinner(f"Fetching exports for {model}", "Exports fetched"):
        exports = provider.list_exports(model, "")

    rich.print()
    if len(exports):
        table = Table(show_header=True, border_style="dim", header_style="bold", box=rich_box.SIMPLE_HEAD)
        table.add_column("Object")
        for imp in exports:
            table.add_row(imp.get("name"))
        rich.print(table)
    else:
        rich.print("[yellow]No exports found")

    divider()

#--------------------------------------------------
# Exports delete
#--------------------------------------------------

@cli.command(name="exports:delete", help="Delete an export from RAI")
@click.option("--export", help="export")
@click.option("--model", help="Model")
def exports_delete(export, model):
    divider(flush=True)
    provider = cast(snowflake.Resources, get_resource_provider())
    coming_soon()
    check_group("exports")

    if not model:
        with Spinner("Fetching models", "Models fetched"):
            models = provider.list_graphs()
        rich.print()
        model = fuzzy("Select a model:", models)
        rich.print()

    if not export:
        db, schema, table = object_flow(provider)
        for t in table:
            export = f"{db}.{schema}.{t}"
            with Spinner(f"Removing {export}", f"{export} removed"):
                provider.delete_export(model, "", export)
    else:
        with Spinner(f"Removing {export}", f"{export} removed"):
            provider.delete_export(model, "", export)

    divider()

#--------------------------------------------------
# Main
#--------------------------------------------------

if __name__ == "__main__":
    # app = EventApp()
    # app.run()
    cli()
