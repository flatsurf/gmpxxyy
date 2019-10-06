#!/bin/bash
set -ex

source $RECIPE_DIR/environment.sh

$SNIPPETS_DIR/autoconf/run.sh
$SNIPPETS_DIR/make/run.sh
make install

$SNIPPETS_DIR/todo/run.sh
