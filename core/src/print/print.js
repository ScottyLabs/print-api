/**
 * @file print.js
 * @brief Print node. Sends jobs to the Linux print driver.
 * @author Justin Gallagher, justin@scottylabs.org
 * @since 2015-08-07
 */

'use strict';

var exec = require('child_process').exec;

/**
 * @function printFile
 * @brief Copies a file to the printed directory. In the future, calls lp to add
 *        the file to the print queue.
 * @param path String: Path to file to print.
 * @param andrewid String: Andrew ID to use for printing.
 * @param jobid Number: ID for this job.
 * @param options: Object: Parameters to the lp command to pass.
 */
function printFile(path, andrewid, jobid, options) {
  exec('mkdir -p printed/' + andrewid + '& cp ' + path + ' printed/' +
       andrewid + '/' + jobid + '.pdf');
}

var print = {
  printFile: printFile,
};

module.exports = print;
