
import os
import zipfile
from pathlib import Path
from cement import Controller, ex
from ..core.version import get_version

class MakeAddonZip(Controller):
    class Meta:
        label = 'build-addon'
        stacked_type = 'embedded'
        stacked_on = 'base'

    def zipdir(self, path, ziph):
        for root, _, files in os.walk(str(path)):
            for file in files:
                ziph.write(os.path.join(root, file))

    @ex(
        help='builds the addon import file',
    )
    def build_addon(self):
        addon_dir = Path('rapido_developer')
        zip_file = Path('dist/rapido_developer-%s.zip' % get_version())
        if not zip_file.parent.exists(): zip_file.parent.mkdir(exist_ok=True)
        with zipfile.ZipFile(str(zip_file), 'w', zipfile.ZIP_DEFLATED) as zipf:
            self.zipdir(str(addon_dir), zipf)
        print('%s created' % zip_file)



