from os.path import exists
from pathlib import Path

from consts import ROOT_DIR


def get_environment_type() -> str:
    if exists(ROOT_DIR / '.env'):
        return 'local'
    if exists(ROOT_DIR / '.env.testing'):
        return 'testing'
    if exists(ROOT_DIR / '.env.production'):
        return 'production'
    raise EnvironmentError('Environment not found.')

def get_environment_file_path() -> Path:
    environment_type = get_environment_type()
    environments = {
        'local': ROOT_DIR / '.env',
        'testing': ROOT_DIR / '.env.testing',
        'production': ROOT_DIR / '.env.production',
    }
    return environments[environment_type]
