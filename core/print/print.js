/**
 * @file print.js
 * @brief Print node. Sends jobs to the Linux print driver.
 * @author Justin Gallagher, justin@scottylabs.org
 * @since 2015-08-07
 */

var spawn = require('child_process').spawn

/**
 * @function printFile
 * @brief Adds a file to the print queue.
 * @param path String: Path to file to print.
 * @param andrewid String: Andrew ID to use for printing.
 * @param jobid Number: ID for this job.
 * @param options: Object: Parameters to the lp command to pass.
 */
function printFile(path, andrewid, jobid, options) {
  spawn('lp', ['-U ' + andrewid, '-t ' + jobid, path]);
}

var print = {
  printFile: printFile
}

module.exports = print;
