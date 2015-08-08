# Overview
- Endpoint node(s)

    - The interfaces that interact with clients, such as email, native apps, web
      app, etc.

- Delivery node

    - A single node that acts as the sole endpoint to the conversion and
      printing pipeline.

    - Classifies and distributes file blobs to different converters.

- Conversion node(s)

    - Convert the blobs to PDF.

- Print node

    - Sends PDFs to the Linux print driver.

- Job node

    - Maintains master job list, allows the endpoint nodes to interface with it.

- Telemetry node

    - Sink for any sort of telemetry in the system.

## Endpoint Node(s)

- Email `P0`

    - Node.js IMAP cleint parses an email inbox provided by Gmail. `P0`

    - Prints the attachments of a given email from an `@andrew.cmu.edu` email.
      `P0`

    - Maintains a list of additional emails that can print to an account. `P1`

- Web app `P0`

    - File upload `P0`

    - Google Drive `P1`

    - Dropbox `P1`

- Android app `P2`

    - File picker `P2`

    - Share endpoint `P2`

- iOS `P2`

- Windows Universal Appp `P2`

- Chrome Extension `P2`

- Public API with API keys `P2`

## Delivery Node

- Expose REST endpoint. `P0`

- Secured with SSL. `P1`

- Maintains private API keys for the endpoint nodes to use. `P1`

## Conversion Nodes

- Accept PDF. `P0`

- Accept plain text (.txt, source code files). `P0`

- Accept Microsoft Word, PowerPoint. `P1`

- Accept various image formats. `P1`

- Update job node with success or failure of conversion. `P1`

- Accept a link and print a static website (like a course website). `P2`

## Print Node

- Accept a PDF and send it to Linux print driver. `P0`

- Maintain blacklist of users who have opted out of using Print. `P0`

- Update master job list with error information in case of failed print. `P1`

## Job Node

- Maintain master job list. `P1`

- Allow queries of job status. `P1`

- Clear database at defined intervals. `P1`

- Backup and restore the job list from a backup. `P1`

- Asynchronously report job statuss to registered endpoints. `P2`

## Telemetry Node

- Maintain a master log of all notable events, correlated with job IDs. `P0`

- Create an event logging API for other nodes to log events. `P0`

- Create a small text file weekly with aggregate statistics. `P1`

    - Back it up in a cloud drive service `P1`

- Simple admin panel to check master status and number of errors. `P2`

- Add usage statistics to admin panel. `P2`

