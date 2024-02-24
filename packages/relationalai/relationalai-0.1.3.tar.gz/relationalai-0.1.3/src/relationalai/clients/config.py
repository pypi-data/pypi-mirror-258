import os
from typing import Dict, Any
from railib import config
import configparser

#--------------------------------------------------
# helpers
#--------------------------------------------------

def _find_config_file():
    if os.path.exists("rai.config"):
        return "rai.config"
    elif os.path.exists(os.path.expanduser("~/.rai.config")):
        return os.path.expanduser("~/.rai.config")

def _get_config(file:str|None=None):
    if not file:
        file = _find_config_file()
    if not file:
        return {}
    config = configparser.ConfigParser()
    config.read(file)
    cfg = {}
    for key, value in config.items():
        cfg[key] = {k: v for k,v in value.items()}
    return cfg

def to_rai_config(data:Dict[str, Any]) -> Dict[str, Any]:
    creds = config._read_client_credentials(data)
    _keys = ["host", "port", "region", "scheme", "audience"]
    result = {k: v for k, v in data.items() if k in _keys}
    result["credentials"] = creds
    return result

#--------------------------------------------------
# Config
#--------------------------------------------------

class Config():
    def __init__(self, profile:str|None=None):
        self.profile:str = profile or os.environ.get("RAI_PROFILE", "default")
        self.fetch()

    def get_profiles(self):
        return self.profiles.keys()

    def fetch(self):
        self.profiles = _get_config(_find_config_file())
        self.props = self.profiles.get(self.profile, {})

    def clone_profile(self):
        self.props = {k: v for k,v in self.props.items()}

    def get(self, name:str, default:Any|None=None, strict:bool=True):
        val = self.props.get(name, os.environ.get(name, default))
        if val is None and strict:
            raise Exception(f"Missing config value for '{name}'")
        return val

    def set(self, name:str, value:str|int):
        self.props[name] = value

    def unset(self, name:str):
        del self.props[name]

    def to_rai_config(self) -> Dict[str, Any]:
        return to_rai_config(self.props)

    def save(self):
        self.profiles[self.profile] = self.props
        # save the config in ini format in rai.config
        with open("rai.config", "w") as f:
            for profile, props in self.profiles.items():
                if len(props):
                    f.write(f"[{profile}]\n")
                    for key, value in props.items():
                        f.write(f"{key} = {value.replace('%', '%%')}\n")
                    f.write("\n")