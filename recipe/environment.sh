#!/bin/bash

# ##################################################################
# Source this file to setup additional environment variables for the
# conda-build environment.
# ##################################################################

export SNIPPETS_DIR=${SNIPPETS_DIR:-$SRC_DIR/recipe/snippets}
export GITHUB_ORGANIZATION=flatsurf
export GITHUB_REPOSITORY=gmpxxyy
export build_flavour=${build_flavour:-release}

source $SNIPPETS_DIR/make/environment.sh

export SUBDIRS=
