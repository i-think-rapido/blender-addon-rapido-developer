
import os
import shutil
from pathlib import Path
from cement import Controller, ex
from ..core.version import get_version

class MakeAddonZip(Controller):
    class Meta:
        label = 'build-addon'
        stacked_type = 'embedded'
        stacked_on = 'base'

    @ex(
        help='builds the addon import file',
    )
    def build_addon(self):
        addon_dir = (Path(__file__).parent.parent).resolve()
        zip_file = Path('dist/rapido_developer-%s' % get_version())
        shutil.make_archive(
            str(zip_file), 
            'zip', 
            root_dir=str(addon_dir), 
            base_dir='rapido_developer'
        )
        print('%s.zip created' % zip_file)



