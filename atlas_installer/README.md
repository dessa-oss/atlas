# atlas-installer

During installation, Atlas installer 

1. Downloads the installation package, which is commonly built and packaged by the [`atlas-ce-build`](https://github.com/DeepLearni/atlas-ce-build) build pipeline
2. Unpacks the package (the file to unpack can be supplied using a command line argument), which should contain
  * an images directory with docker images and a single manifest.yaml file,
  * a wheels directory with the SDK and Atlas server python packages.
3. Loads the following docker images from the package: scheduler, worker, tracker, rest, GUI, tensorboard rest, tensorboard server
4. Places configuration files in the right locations. if in advanced mode, prompts users for details of the configurations
5. Installs the wheels in the wheels directory with the current python executable, except for the server
6. Installs the Atlas server via wheel

The installer installs its own python dependencies in the current python environment when needed.

All the above steps can be toggled on and off via flags when running the installer. Use `python atlas_installer.py --help` to see more.

The user should run the installer using the python environment they intend to use Atlas CE.

The installer should be build using the build script in order for it to contain its git version via `setuptools_scm`
