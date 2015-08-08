/* @file server.js
 * @brief Starts and runs all of the modules in print-core.
 * @author Oscar Bezi, bezi@scottylabs.org
 * @since 07 Aug 2015
 */
'use strict';

var repl = require('./repl');

repl.start();

repl.register('hello',
              'Prints hello world.',
              function () { console.log('Hello, world!'); });
