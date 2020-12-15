# Tool for Easy Blender Addon Development

**My Motivation to Create This Tool**

I'm a coder, new to Bender and wanted to write an addon for it.

I like to use my own editor and not Blender itself.

It was annoyed how rediculously cumbersome reloading of the addon is when I just made a change.

That's why I've been looking for solutions of the community but found nothing.

*Hey, I'm a coder, so why not creating one myself while lerning Blender bottom-up.*

This repo is the result.


## How to Use Rapido Developer Addon

**WARNING:** The current state of this addon works, but is not production ready.

### Preparation

Get a copy of the newest version of this addon.

[https://github.com/i-think-rapido/blender-addon-rapido-developer](https://github.com/i-think-rapido/blender-addon-rapido-developer)

Create virtual an environment environment.

```
$ make virtualenv
```

### 1. Part - Installing the Rapdio Developer Addon in Blender

Use the command ```rapidodeveloper build-addon``` to create an import zip file to be used for import in Blender.

You can find this installer file in folder: ```<project-root>/dist```.

Then open the ```Edit > Preferences > Addons``` dialog of the preferences in Blender and import the zip file.

Activate the Community tab and search for ```rapido```.

Activate ```Development: Rapido Developer``` *(This may take some seconds)*

You may set the Scripts Path of Blender to a folder that suits you.

You can configure this setting in ```Edit > Preferences > File Paths > Scripts```

If you change this setting while having Rapido Developer Addon acitivated, you have to deactivate and reactivate this addon again to refresh the inner path settings of this addon.

When activated, blender starts listening on port 11111 on your local machine for commands provided by the watcher (see 2. Part)

### 2. Part - Usage of the command line tool

Create a project folder for your addon, if you don't already have one.

The best preparation would be to have a working ```__init__.py``` file in this folder with an appropriate ```bl_info``` dictionary.

Use the command

```
$ rapidodeveloper watch <addon-name> <addon-folder to be watched (default: current folder)>
```

to start watching your changes.

Remember, you need to have the Rapido Developer Addon activated when watching a folder. Otherwise the command line tool will abort with an error.

### Further Notes

It is recommended to open the console window where blender is running during the development of your addon. 
This way you can notice errors or debug output messages of you addon.

On linux or macOS, you should start blender from the command line.

On Windows, you have a menu entry at ```Window > Toggle System Console``` to open the console window.

## Installation

```
$ pip install -r requirements.txt

$ pip install setup.py
```

## Development

This project includes a number of helpers in the `Makefile` to streamline common development tasks.

### Environment Setup

The following demonstrates setting up and working with a development environment:

```
### create a virtualenv for development

$ make virtualenv

$ source env/bin/activate


### run rapidodeveloper cli application

$ rapidodeveloper --help


### run pytest / coverage

$ make test
```


### Releasing to PyPi

Before releasing to PyPi, you must configure your login credentials:

**~/.pypirc**:

```
[pypi]
username = YOUR_USERNAME
password = YOUR_PASSWORD
```

Then use the included helper function via the `Makefile`:

```
$ make dist

$ make dist-upload
```

## Deployments

### Docker

Included is a basic `Dockerfile` for building and distributing `Rapido Developer`,
and can be built with the included `make` helper:

```
$ make docker

$ docker run -it rapidodeveloper --help
```
