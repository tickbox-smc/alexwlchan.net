#!/usr/bin/env bash
# Based on https://gist.github.com/hc2p/9e284cee3d585eefbc59454e44cc247a

set -o errexit
set -o nounset

sudo service docker stop
sudo chown -R travis ~/docker
