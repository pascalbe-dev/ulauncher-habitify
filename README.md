# Ulauncher Habitify

> [ulauncher](https://ulauncher.io/) Extension to access your [Habitify](https://www.habitify.me/) account.

## Usage

TODO: ADD DEMO GIF

## Features

- display all habits for the current day / time

## Requirements

- [ulauncher 5](https://ulauncher.io/)
- Python > 3

## Install

Open ulauncher preferences window -> extensions -> add extension and paste the following url:

`https://github.com/pascalbe-dev/ulauncher-habitify.git`

## Usage

- Before usage you need to configure your Habitify API Credential in plugin preferences. Find guidance to get your API credential [here](https://docs.habitify.me/authentication).

## Local development

### Requirements

- `less` package installed
- `inotify-tools` package installed

### Steps 

1. Clone the repo `git clone https://github.com/pascalbe-dev/ulauncher-habitify.git`
2. Cd into the folder `cd ulauncher-habitify`
3. Watch and deploy your extension for simple developing and testing in parallel `./watch-and-deploy.sh` (this will restart ulauncher without extensions and deploy this extension at the beginning and each time a file in this directory changes)
4. Check the extension log `less /tmp/ulauncher-extension.log +F`
5. Check ulauncher dev log `less /tmp/ulauncher.log +F`