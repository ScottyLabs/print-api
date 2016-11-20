# Print-Scottylabs
Unified printing for CMU on multiple devices.

## API format

### POST request

|Input type|Name           |
|----------|---------------|
|text      |andrew_id      |
|file      |file           |


### JSON response

#### Success example:
```
{
  "message": "Successfully printed hello_world.pdf",
  "status_code": 200
}
```

#### Failure example:
The status code will default to 400, Bad Request.
```
{
  "message": "Please submit a valid Andrew ID.",
  "status_code": 400
}
```

