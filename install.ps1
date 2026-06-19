# Copyright (c) 2026 JG Systems Consulting Ltd.
# MIT License — see LICENSE.
#
# PowerShell wrapper around install.py. Forwards all arguments.

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
python "$scriptDir\install.py" @args
