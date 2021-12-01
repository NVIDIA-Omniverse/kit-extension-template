# Extension Project Template

This project is a template for developing own extensions for *Omniverse Kit* based apps.

# Setup

For better developer experience it is recommended to create a folder link named `app` to the *Omniverse Kit* app installed from *Omniverse Launcher*. Convenience script to use is included.

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


# Sharing Your Extensions

Direct link to a git repository can be added to *Omniverse Kit* extension search paths. 

Link might look like this: `git://github.com/[user]/[your_repo].git?branch=main&dir=exts`

Notice `exts` is repo subfolder with extensions. More information can be found in "Git URL as Extension Search Paths" section of developers manual.
