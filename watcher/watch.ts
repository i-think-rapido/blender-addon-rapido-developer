
import * as fs from "https://deno.land/std@0.79.0/fs/mod.ts";
import * as path from "https://deno.land/std@0.79.0/path/mod.ts";
import { ld as _ } from 'https://deno.land/x/deno_lodash/mod.ts';
//import * as colors from 'https://deno.land/x/ansi_colors/mod.ts';
import "https://deno.land/x/hackle/init.ts";



const info = (message: string) => {
  console.info(message);
}

type FileInfo = {
  path: string;
  isFile: boolean;
  isDirectory: boolean;
  size: number;
  mtime: Date | null;
};

const DEBOUNCE = 300;
const debounce = <Fn extends (...args: any[]) => any>(
  callback: Fn,
  waitFor: number
) => {
  let timeout = 0;
  return (...args: Parameters<Fn>): ReturnType<Fn> => {
    let result: any;
    clearTimeout(timeout);
    timeout = setTimeout(() => {
      result = callback(...args);
    }, waitFor);
    return result;
  };
}

const normDirSep = (filename: string): string => {
  return filename.replace(/\\/g, '/');
}

const stat = (baseDir: string, prefix: string = ''): FileInfo [] => {

  prefix = normDirSep(prefix);
  const list = [...fs.walkSync(baseDir)]
    .filter(f => f.isFile || f.isDirectory)
    .map(f => ({ path: f.path, stat: Deno.statSync(f.path) }))
    .map(f => ({ path: normDirSep(f.path), isFile: f.stat.isFile, isDirectory: f.stat.isDirectory, size: f.stat.size, mtime: f.stat.mtime }))
    .map(f => ({ ...f, path: f.path.indexOf(prefix) === 0 ? f.path.slice(prefix.length) : f.path }))
    .filter(f => f.path !== '')
    .filter(f => !f.path.indexOf('__pycache__'))
    ;

  return list;
}

const absPath = (path: string) : string => {
  return normDirSep(Deno.realPathSync(normDirSep(path)));
}

const difference = (collection: FileInfo[], ref: FileInfo[]) => {
  return _.differenceWith(collection, ref, (c: FileInfo, r: FileInfo) => {
    return c.path === r.path;
  });
}

const removeEmptyDir = (path: string): boolean => {

  if (Deno.statSync(path).isDirectory) {
    if ([...fs.walkSync(path)].length === 1) {
      Deno.removeSync(path);
      return true;
    }
  }

  return false;
}

const removeFile = (file: string, dest: string) => {
  const d = `${dest}${file}`;
  console.log(d)
  Deno.removeSync(d);
  let dir = path.dirname(d);
  while(removeEmptyDir(dir)) {
    dir = path.dirname(dir);
  }
}

const copyFile = (file: string, dest: string, source: string) => {
  const w = `${source}${file}`;
  const d = `${dest}${file}`;
  Deno.mkdirSync(path.dirname(d), { recursive: true });
  Deno.copyFileSync(w, d);
}

const copyAllFiles = debounce((files: string[], dest: string, source: string) => {
  files.forEach(f => copyFile(f, dest, source));
}, DEBOUNCE);
const removeAllFiles = debounce((files: string[], dest: string) => {
  files.forEach(f => removeFile(f, dest));
}, DEBOUNCE);

const reloadAddon = debounce(async (addonName: string) => {
  try {
    fetch(`http://127.0.0.1:11111/reload-addon/${addonName}`);
  }
  catch (error) {
    console.error(error)
  }
}, DEBOUNCE);

const startSync = async (addonName: string, watchedPath: string, destinationPath: string) => {

  const watched = stat(watchedPath, watchedPath);
  const dest = stat(destinationPath, destinationPath);

  const watchedOnly = difference(watched, dest);
  const destOnly = difference(dest, watched);

  destOnly.forEach((f: FileInfo) => removeFile(f.path, destinationPath));
  watchedOnly.forEach((f: FileInfo) => copyFile(f.path, destinationPath, watchedPath))


  const watcher = Deno.watchFs(watchedPath);
  let copyList: string[] = [];
  let delList: string[] = [];
  for await (const event of watcher) {

    const relPaths = event.paths.map(f => normDirSep(f).replace(watchedPath, ''));

    switch(event.kind) {
      case 'create':
      case 'modify':
        copyList = [...new Set(copyList.concat(relPaths))];
        copyAllFiles(copyList, destinationPath, watchedPath);
        await reloadAddon(addonName);
        break;
      case 'remove':
        delList = [...new Set(copyList.concat(relPaths))];
        removeAllFiles(delList, destinationPath);
        await reloadAddon(addonName);
        break;
    }

  }

}

const main = async () => {

  try {

    const res = await fetch('http://127.0.0.1:11111/script-path');
    const json = await res.json();

    const addonName = Deno.args[0];
    const watchedPath = absPath(Deno.args[1]) || '.';
    const blenderScriptPath = json.script_path;
    const path = `${blenderScriptPath}/addons/${addonName}`;
    Deno.mkdirSync(path, { recursive: true });
    const destinationPath = absPath(path);

    info(`Addon name: ${addonName}`);
    info(`Blender script folder: ${blenderScriptPath}`)
    info(`Path to watch: ${watchedPath}`);

    startSync(addonName, watchedPath, destinationPath);  
  }
  catch (error) {
    console.error(error);   
  }

}

main();


// request startup info: is the destination folder available

// yes:

// stat destination foulder and source foulder
// find newer files on source side

// create list

// copy listed files to destination folder





