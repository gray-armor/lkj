# lkj

CLI tool to report working time to Google Calendar

## Install

```sh
pip install git+https://github.com/gray-armor/lkj
```

## Build and install from source

```
make install
# "make clean" to uninstall
```

## Setup

Summary
- Create GCP Project
- Enable Google Calendar API
- Create OAuth2.0 Client ID
- Download credential JSON file
- Place the file to `~/.lkj/credentials.json`
- run
```sh
lkj init
```

### Create GCP Project and Enable Google Calendar API

see: https://developers.google.com/workspace/guides/create-project

### Install OAuth2.0 Client ID from GCP

see:
- https://developers.google.com/workspace/guides/create-credentials#configure_the_oauth_consent_screen
- https://developers.google.com/workspace/guides/create-credentials#create_a_oauth_client_id_credential
- https://developers.google.com/workspace/guides/create-credentials#desktop

Place your credential JSON file to `~/.lkj/credentials.json`

### Bind your Google calendar

```sh
lkj init
```

## Uninstall

```sh
pip uninstall lkj
```

## Start Working

```sh
lkj n
# or
lkj n work title
```

## Submit your work to Google calendar

```sh
lkj c
# if you don't like vim,
EDITOR=nano lkj c
```

Edit as you like
- Created At
- Done At
- Title
- Description

## Show current work

```sh
lkj
```

## Delete current working data

```sh
lkj d
```
