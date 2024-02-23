from .clients import config
from . import clients

def Model(name:str, dry_run:bool=False):
    cfg = config.Config()
    platform = cfg.get("platform", "snowflake")
    if platform == "azure":
        return clients.azure.Graph(name, dry_run)
    elif platform == "snowflake":
        return clients.snowflake.Graph(name, dry_run)
    else:
        raise Exception(f"Unknown platform: {platform}")

def Resources(profile:str|None=None, cfg:config.Config|None=None):
    cfg = cfg or config.Config(profile)
    platform = cfg.get("platform", "snowflake")
    if platform == "azure":
        return clients.azure.Resources(config=cfg)
    elif platform == "snowflake":
        return clients.snowflake.Resources(config=cfg)
    else:
        raise Exception(f"Unknown platform: {platform}")

def Graph(name:str, dry_run:bool=False):
    return Model(name, dry_run=dry_run)