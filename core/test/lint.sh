# !/usr/bin/env bash
# @file lint.sh
# @brief Runs the linters.
# @since 8 August 2015
# @author Oscar Bezi, bezi@scottylabs.org

# JSHint
jshint ./src

# JSCS
jscs ./src
