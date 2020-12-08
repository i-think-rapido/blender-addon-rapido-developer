# Tool for Easy Blender Addon Development

**My Motivation to Create This Tool**

I'm a coder, new to Bender and wanted to write an addon for it.

I like to use my own editor and not Blender itself.

It was annoyed how rediculously cumbersome reloading of the addon is when I just made a change.

That's why I've been looking for solutions of the community but found nothing.

*Hey, I'm a coder, so why not creating one myself while lerning Blender bottom-up.*

This repo is the result.


## How to Use Rapido Developer Addon

### 1. Part

Get a copy of the newest version of this addon.

[https://github.com/i-think-rapido/blender-addon-rapido-developer](https://github.com/i-think-rapido/blender-addon-rapido-developer)

Use the build script to create an import zip file to be used for import in Blender.

You can find this file in folder: ```<project-root>/dist```.

Then open the ```Edit > Preferences > Addons``` dialog of the preferences in Blender and import the zip file.

Activate the Community tab and search for ```rapido```.

Activate ```Development: Rapido Developer``` *(This may take some seconds)*

### 2. Part

**Preparation**

You need an execution program for running the client. This is (a) ```deno``` from [https://deno.land](https://deno.land).

You find installation instructions at [https://deno.land/manual/getting_started/installation](https://deno.land/manual/getting_started/installation).

After installation, create a project folder and start implementing your addon.

When you want to sync this folder with Blender, start the client and leave it running until you're done.

This is done by opening your favorite Terminal program of your operating system. (On Windows: [WIN]+R, then type in ```cmd``` + [ENTER].)

The command is:

```bash
# in one line, type:
deno run --allow-read --allow-write --allow-net --watch --unstable <project-root>/watcher/watch.ts <addon-name-without-spaces> <folder-to-watch>
# replace the brackets with approriate values
```

You can see an example in the ```<project-root>/start-watching.sh``` file.

**Nothing more to do.** Rapido Developer Addon takes care of the rest.

**Hint:** You can have several clients runing.

### TODOs

* I need some refactoring in web server and client code to enhence readability.
* The web server port is fixed to ```11111```. This needs to be changeable.
* The addon part of this tool is not tested for Linux and MacOS Blender *but should work*.

### If You Find Bugs

Post them at [https://github.com/i-think-rapido/blender-addon-rapido-developer/issues](https://github.com/i-think-rapido/blender-addon-rapido-developer/issues)

## The Concept Behind It

I want to have a development folder in my project. 

When I save a file, it should simutaniously sync it with the Blender addon folder and reload the addon automatically.

First, I wanted to use the *watchdog* in this addon and install it with pip. But unfortunately installing third party modules for Blender python is very difficult. (At least for me.)

*I shifted to another approach:*

This tool consists of two parts:

- A basic web server encapsulated within my addon
- A client which does the heavy lifting and syncs the folders

Changes to my development folder where synced to the Blender addon folder outside of Blender. Then the client notifies the addon via REST API to reload the addon.

To get the client ready for work, it discovers the actual Blender addon folder by calling the web server on startup. Blender must be running and having **Rapido Developer Addon** activated when doing this.

