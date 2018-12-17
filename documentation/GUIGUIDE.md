# GUI Guide

## Installation

### Dependencies

The preferred way to run the GUI is via Docker.  As a result, `Docker >= 18.09` is required.  In all likelihood, older versions of Docker will work but these have not been tested.

As with Foundations itself, there must be an accessible `redis:5` instance / installation.  See the [start guide](STARTGUIDE.md) for more information.

If you wish to build the GUI from source, we also require `Python >= 3.5` - older versions may work but have not been tested.

### Build Process

These steps are not necessary if you already have the images or can download them.  Feel free to skip if that's the case.  Otherwise:

0. If you haven't done so already, clone the Foundations repo and checkout the desired branch (probably `master`).
1. Make sure you're in the root of the Foundations repo.
2. Run the `build_gui.sh` script - this will also tag the images.

### Installation Process

0. Either build (see above for how to do that) the images or otherwise acquire them via `docker pull` or `docker load -i`.
1. Ensure that you have the `foundations-rest-api` and `foundations-gui` images installed on your system, and both have the same tag.  If not, please tag them accordingly - any syntactically valid tag will work, so long as they're the same.
2. Ensure that you have the `foundations_gui.sh` script whose version matches the image versions, e.g. if you built the images from the `master` branch, grab the `foundations_gui.sh` script from the `master` branch.
3. Edit two variables in the `foundations_gui.sh` script as follows:
    * `node_ip` is the ip of the node on which the REST API container will be hosted.  If you're going to have a GUI installation for development or otherwise on your own machine, and it will be accessed by only you, then you may put `localhost`.  If you want anyone else to access it, put the ip of the machine instead.
    * `redis_url` is the url for the `redis:5` instance / installation that Foundations has been / will have been using.  It is of the form `redis://<redis_ip>:<redis_port>` - you can't use `localhost` in place of the redis ip, even if redis is running on the same node as the REST API.  Please do put the ip of the node hosting redis.

## Starting / Stopping the GUI

Make sure you have edited the `foundations_gui.sh` script as described in step 3 of the installation process!

### Starting the GUI

`./foundations_gui.sh start ui [image_tag]`
* `image_tag` is optional - omit to use `latest` as a default

### Stopping the GUI

`./foundations_gui.sh stop ui`

## Known Issues Running On OSX
There are some known issues related to networking with Docker on OSX, which could appear as we use Docker as the backend to run the GUI. Please see [the networking features documentation](https://docs.docker.com/docker-for-mac/networking/) for details and limitations.