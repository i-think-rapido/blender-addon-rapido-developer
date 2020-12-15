
import re
import os
import aiohttp
from aiohttp import ClientConnectionError
import asyncio
import shutil
from watchgod import awatch, Change, DefaultWatcher
from pathlib import Path
from cement import Controller, ex, FrameworkError

class Watcher(Controller):
    class Meta:
        label = 'watch'
        stacked_type = 'embedded'
        stacked_on = 'base'

    @ex(
        help='start watching',
        arguments=[
            (
                ['addon'],
                dict(
                    help='the addon to be watched',
                )
            ),
            (
                ['-p', '--path'],
                dict(
                    help='addon development folder to be watched',
                    default='.',
                    required=False,
                    dest='watched_folder'
                )
            ),
        ],
    )
    def watch(self):

        if self.app.pargs.addon == 'rapido_developer':
            raise FrameworkError('Addon can\'t be rapido_developer')

        if self.app.pargs.addon:
            print('Addon to sync %s' % self.app.pargs.addon)

        if self.app.pargs.watched_folder == '.':
            print('This folder to watch')
        else:
            print('Folder %s to watch' % self.app.pargs.watched_folder)

        if re.match(r'^[a-zA-Z0-9_]+$', self.app.pargs.addon):
            self.addon = self.app.pargs.addon
        else:
            raise FrameworkError('Addon has no proper identifier')

        path = Path(self.app.pargs.watched_folder).resolve()
        
        if path.exists() and path.is_dir():
            self.watched_folder = path
        else:
            raise FrameworkError('%s is not a directory' % path)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.sync())

    async def send(self, uri):

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(uri) as resp:

                    if resp.status == 200:
                        return await resp.json()
                    elif resp.status == 400:
                        return await resp.json()
                    else:
                        raise FrameworkError('Rapido Developer Server part seems not to be running')
            except ClientConnectionError as e:
                raise e

    async def sync(self):

        self.blender_script_path = Path((await self.send('http://localhost:11111/script-path'))['script_path'])
        self.destination_path = self.blender_script_path / 'addons' / self.addon
        self.destination_path.mkdir(parents=True, exist_ok=True)
        print('Blender script folder: %s' % self.blender_script_path)

        await self.start_sync()

    def get_dest_source_path(self, source_path):
        return (Path('%s/%s' % (str(self.destination_path), str(source_path).replace(str(self.watched_folder), ''))), Path(str(source_path)))

    async def handle_file_changes(self, changes):

        for change in changes:
            pair = self.get_dest_source_path(change[1])
            if change[0] == Change.deleted:
                pair[0].unlink()
                parent = pair[0].parent
                while not os.listdir(str(parent)):
                    parent.rmdir()
                    parent = parent.parent

            elif change[0] == Change.added or change[0] == Change.modified:
                shutil.copy(pair[1], pair[0])

        print(await self.send('http://localhost:11111/reload-addon/%s' % self.addon))

    async def start_sync(self):
        
        watched = self.stat(self.watched_folder)
        dest = self.stat(self.destination_path)

        dest_only = self.difference(dest, watched)

        for p in dest_only:
            if p['path'].is_dir() and not os.listdir(str(p['path'])):
                p['path'].rmdir()                
            else:
                p['path'].unlink()
        shutil.copytree(self.watched_folder, self.destination_path, dirs_exist_ok=True)

        async for changes in awatch(self.watched_folder, debounce=500, normal_sleep=200):
            await self.handle_file_changes(changes)

    def stat(self, baseDir):
        out = baseDir.glob('**/*')
        out = filter(lambda x: x.is_file() or x.is_dir(), out)
        out = filter(lambda x: str(x).find('__pycache__') == -1, out)
        out = map(lambda x: dict(path=x, stat=x.stat()), out)
        out = map(lambda x: dict(path=x['path'], is_file=x['path'].is_file(), is_dir=x['path'].is_dir(), size=x['stat'].st_size, mtime=x['stat'].st_mtime), out)
        return out

    def difference(self, collection, ref):
        return [c for c in collection if len([*filter(lambda x: x['path'] == c['path'], ref)]) == 0]
    