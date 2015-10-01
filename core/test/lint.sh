# !/usr/bin/env bash
# @file lint.sh
# @brief Runs the linters.
# @since 8 August 2015
# @author Oscar Bezi, bezi@scottylabs.org

# JSHint
jshint --config config/jshintrc ./src

# JSCS
jscs -c config/jscsrc ./src
