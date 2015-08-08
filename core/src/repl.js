/* @file repl.js
 * @brief Makes a simple case-insensitive REPL to run various functions via the
 * command line.
 * @author Oscar Bezi, bezi@scottylabs.org
 * @since 7 August 2015
 */

'use strict';

// Requires
var _ = require('lodash');
var readline = require('readline');

// The list of registered commands.
var commands = {};

// Whether or not the repl has started.  Prevents two repls being started.
var started = false;

/* @function register
 * @brief registers a command to be available for use in the REPL.
 * @param command String that identifies what command should be used to invoke
 * the callback.
 * @param help String that is printed to help identify the command and explain
 * what it does.
 * @param callback Function that is executed when the command is evaluated.
 */
function register(command, help, callback) {
  commands[command.toLowerCase()] = {
    help: help,
    callback: callback,
  };
}

/* @function help
 * @brief Print help text.
 */
function help() {
  console.log('Known commands');
  console.log('==============');
  if (_.isEmpty(commands)) {
    console.log('No commands registered.');
  } else {
    _.forOwn(commands, function (obj, key) {
      console.log(key + ' - ' + obj.help);
    });
  }
}

/* @function start
 * @brief Starts the repl.  Ensures that it is not started twice.
 */
function start() {
  if (!started) {
    var rl;

    commands = {};

    rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout,
    });

    rl.setPrompt('print-core> ');

    rl.on('line', function (line) {
      line = line.trim().toLowerCase();

      if (_.has(commands, line)) {
        commands[line].callback();
      } else {
        console.log('Unknown command: ' + line);
        help();
      }

      rl.prompt();

    }).on('close', function () {
      console.log('Exiting. . .');
      process.exit(0);
    });

    register('help', 'Print this help text.', help);
    register('exit', 'Kill repl and server.', function () { rl.close(); });

    started = true;
    rl.prompt();
  }
}

module.exports = {
  start: start,
  register: register,
};
