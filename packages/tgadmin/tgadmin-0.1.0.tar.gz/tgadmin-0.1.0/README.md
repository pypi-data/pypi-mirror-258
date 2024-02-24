<!--
SPDX-FileCopyrightText: 2024 Georg-August-Universität Göttingen

SPDX-License-Identifier: CC0-1.0
-->

# tgadmin

a command line tool for managing your projects without TextGridLab. 

## Install

You may use this with venv or with pipx. with pipx you have the benefit of 
just having the command available without further manual venv creation and activation

### Possibility 1) install and use with pipx

Install [pipx](https://pypa.github.io/pipx/), e.g. on debian/ubuntu `apt install pipx`

and then this tool (from this dir, where this README is located)

        pipx install .

### Possibility 2) venv

        python3 -m venv venv
        . venv/bin/activate
        pip install --editable .

afterwards you have tgadmin in this venv available, but need to activate this venv for using the tool

## Usage

### export sid

get from https://dev.textgridlab.org/1.0/Shibboleth.sso/Login?target=/1.0/secure/TextGrid-WebAuth.php?authZinstance=textgrid-esx1.gwdg.de

and set as env var:

        export TEXTGRID_SID=your_secret_sid_here

or set with `--sid` for every command

### get help

        tgpadmin

### list projects

list your projects:

        tgadmin list

### create project

if there is no suitable project, create one:

        tgadmin create lab-import-test-20230605

## Development


