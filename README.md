# Extension Project Template

This project is a template for developing own extensions for *Omniverse Kit* based apps.

# Getting Started

1. Install *Omniverse Launcher*: https://www.nvidia.com/en-us/omniverse/download/
2. Install one of *Omniverse* apps in the Launcher, we recommend to start with *Code*.
3. Clone this repo
4. Open it using Visual Studio Code. It will suggest installing a few extensions to improve python experience.
5. In the terminal (CTRL + \`) run `link_app.bat` (more in [Linking with an *Omniverse* app](#linking-with-an-omniverse-app) section).
6. Run this app with `exts` folder added as an extensions earch path and new extension enabled:

```bash
> app\omni.code.bat --ext-folder exts --enable omni.hello.world
```




# Linking with an *Omniverse* app

For a better developer experience, it is recommended to create a folder link named `app` to the *Omniverse Kit* app installed from *Omniverse Launcher*. A convenience script to use is included.

Run:

```
> link_app.bat
```

If successful you should see `app` folder link in the root of this repo.

If multiple Omniverse apps is installed script will select recommended one. Or you can explicitly pass an app:

```
> link_app.bat --app create
```

You can also just pass a path to create link to:

```
> link_app.bat --path "C:/Users/bob/AppData/Local/ov/pkg/create-2021.3.4"
```

# Explore

Open this folder using Visual Studio Code. It will suggest you to install few extensions that will make python experience better.

`exts` - is a folder where you can add new extensions. You need to add it extension search path of *omniverse Kit* based app. (Extension Manager -> Gear Icon -> Extension Search Path).

Alternatively, you can launch your app from console with this folder added to search path and your extension enabled, e.g.:

```
> app\omni.create.bat --ext-folder exts --enable omni.hello.world
```

Look for "omni.hello.world" extension in extension manager and enable it. Try applying changes to any python files, it will hot-reload and you can observe results immediately.

# Running Tests

There are 2 ways to run extension tests:

1. Run: `app\kit\test_ext.bat omni.hello.world  --ext-folder exts`

That will run test process with all tests and exit. For development mode pass `--dev`: that will open test selection window. As everywhere, hotreload also works in this mode, give it a try by changing some code!

2. In *Extension Manager* (*Window -> Extensions*) find your extension, click on *TESTS* tab, click *Run Test*

For more information on testing refer to: http://omniverse-docs.s3-website-us-east-1.amazonaws.com/kit-sdk/104.0/docs/guide/ext_testing.html


# Sharing Your Extensions

Direct link to a git repository can be added to *Omniverse Kit* extension search paths. 

Link might look like this: `git://github.com/[user]/[your_repo].git?branch=main&dir=exts`

Notice `exts` is repo subfolder with extensions. More information can be found in "Git URL as Extension Search Paths" section of developers manual.
