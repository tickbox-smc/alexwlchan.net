#!/usr/bin/env sh

set -o errexit
set -o nounset

# Some links that were useful in getting 'gem install' to work:
#
#   - https://jekyllrb.com/docs/installation/
#   - https://github.com/ffi/ffi/issues/485
#
apk update
apk add g++ libffi-dev make musl-dev ruby ruby-dev

# Required for the static file generator
apk add rsync

# Required for the publish-drafts gem
apk add git

# Required for the pygments gem.  This has to be Python 2, not Python 3:
# https://github.com/tmm1/pygments.rb/issues/45
apk add python py2-pip
pip install pygments

bundle install

# These packages are only required for installation, not for running Jekyll
apk del --purge g++ make musl-dev py2-pip ruby-dev
rm -rf /var/cache/apk/*
