# Extension Project Template

This project is a template for developing own extensions for *Omniverse Kit* based apps.

# Getting Started: Add new extension to your *Omniverse App*

1. Install *Omniverse Launcher*: https://www.nvidia.com/en-us/omniverse/download/
2. Install and launch one of *Omniverse* apps in the Launcher. We recommend to start with *Code*.
3. Fork and clone this repo, for example in `C:\projects\kit-extension-template`
4. In the *Omniverse App* open extension manager: *Window* &rarr; *Extensions*.
5. In the *Extension Manager Window* open settings page, with a small gear button in the top left bar.

![Extension Manager Window](/images/add-ext-search-path.png)

6. In the settings you can see where the *App* searches for extensions. Add this cloned repo `exts` folder there as another search path: `C:\projects\kit-extension-template\exts`
7. Now you should be able to find `omni.hello.world` extension in the top left search bar. Select and enable it.
8. *My Window* will pop up. Extension manager watches for any file changes. You can try changing some code in this extension and see them applied immediately with a hotreload.

## Few tips

* Now that `exts` folder was added to the search you can add new extensions to this folder and they will be automatically found by the *App*.
* Look at the *Console* window for warnings and errors. It also has a small button to open current log file.
* All the same commands work on linux. Replace `.bat` with `.sh` and `\` with `/`.

# Next Steps: Alternative way to add a new extension

To get a better understanding and learn few other things, we recommend to remove search path added in previous section and try the following steps.

1. Open it using Visual Studio Code. It will suggest installing a few extensions to improve python experience.
2. In the terminal (CTRL + \`) run `link_app.bat` (more in [Linking with an *Omniverse* app](#linking-with-an-omniverse-app) section).
3. Run this app with `exts` folder added as an extensions earch path and new extension enabled:

```bash
> app\omni.code.bat --ext-folder exts --enable omni.hello.world
```

`--ext-folder` adds new folder to the search path

`--enable` enables an extension.

For more flags run help:

```bash
> app\omni.code.bat -h
```

4. You should see the new *My Window* popup, extension search paths in *Extensions* window, extension enabled in the list of extensions.
5. If you look inside `omni.code.bat` or any other *Omniverse App* they all run *Omniverse Kit* (`kit.exe`). *Omniverse Kit* is an extension runner. Think of it as `python.exe`. It is a small runtime, that enables all the basics, like settings, python, logging and searches for extensions. *Everything else is an extension.* You can run only this new extension without running any big *App* like *Code*:


```bash
> app\kit\kit.exe --ext-folder exts --enable omni.hello.world
```

It starts much faster and will only have extensions enabled required for this new extension: `[dependencies]` of it (Look at `extension.toml`). You can enable more extensions try adding `--enable omni.kit.window.extensions` to have extensions window enabled. Yes, extension window is an extension too:


```bash
> app\kit\kit.exe --ext-folder exts --enable omni.hello.world --enable omni.kit.window.extensions
```

You should see a menu in the top left. From here you can enable more extensions in UI. 

## Few tips

* In the *Extensions* window, press *Bread* button near the search bar and select *Show Extension Graph*. It will show how current *App* come to be. All extensions and their dependencies.
* Extensions system documentation: http://omniverse-docs.s3-website-us-east-1.amazonaws.com/kit-sdk/104.0/docs/guide/extensions.html

# Running Tests

To run tests we run a new process where only the tested extension (and it's dependencies) is enabled. Like in example above + testing system (`omni.kit.test` extension). There are 2 ways to run extension tests:

1. Run: `app\kit\test_ext.bat omni.hello.world  --ext-folder exts`

That will run test process with all tests and exit. For development mode pass `--dev`: that will open test selection window. As everywhere, hotreload also works in this mode, give it a try by changing some code!

2. In *Extension Manager* (*Window &rarr; Extensions*) find your extension, click on *TESTS* tab, click *Run Test*

For more information on testing refer to: http://omniverse-docs.s3-website-us-east-1.amazonaws.com/kit-sdk/104.0/docs/guide/ext_testing.html


# Linking with an *Omniverse* app

For a better developer experience, it is recommended to create a folder link named `app` to the *Omniverse Kit* app installed from *Omniverse Launcher*. A convenience script to use is included.

Run:

```bash
> link_app.bat
```

If successful you should see `app` folder link in the root of this repo.

If multiple Omniverse apps is installed script will select recommended one. Or you can explicitly pass an app:

```bash
> link_app.bat --app create
```

You can also just pass a path to create link to:

```bash
> link_app.bat --path "C:/Users/bob/AppData/Local/ov/pkg/create-2021.3.4"
```

# Sharing Your Extensions

TBD;

Direct link to a git repository can be added to *Omniverse Kit* extension search paths. 

Link might look like this: `git://github.com/[user]/[your_repo].git?branch=main&dir=exts`

Notice `exts` is repo subfolder with extensions. More information can be found in "Git URL as Extension Search Paths" section of developers manual.
