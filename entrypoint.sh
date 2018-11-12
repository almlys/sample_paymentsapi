#!/usr/bin/env bash

if [ "x$1" == "xtests" ]; then
    py.test --cov=app tests
else
    exec "$@"
fi
