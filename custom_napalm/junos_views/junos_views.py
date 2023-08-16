from yaml import safe_load
from pathlib import Path
from jnpr.junos.factory import FactoryLoader

junos_classes = {}
folder = Path(__file__).with_name('junos_views').glob('**/*.yml')

for file in folder:
    yaml = safe_load(file.read_text().replace('unicode', 'str'))
    junos_classes.update(FactoryLoader().load(yaml))

globals().update(junos_classes)

