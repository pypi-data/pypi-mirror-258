# simple-redis-helper
Little command-line library to send/receive data to/from a Redis backend.

## Installation

*simple-redis-helper* is a Python 3 library, which you can install in virtual
environments as follows:

```commandline
pip install simple-redis-helper
```

## Redis and Docker

You can start Redis through docker on a host as follows:

```commandline
docker run --name=redis-devel --publish=6379:6379 --hostname=redis --restart=on-failure --detach redis:latest
```

For connecting other docker images to this instance, add the following to your `docker run` command:

```
--net=host
```

## Utilities

### Load

Uploads a file into the Redis backend.

```
usage: srh-load [-h] [-H HOST] [-p PORT] [--password PASSWORD]
                                [--password_env PASSWORD] [-d DB] -k KEY -f
                                FILE

Loads a file into Redis under the specified key.

optional arguments:
  -h, --help            show this help message and exit
  -H HOST, --host HOST  The redis server to connect to (default: localhost)
  -p PORT, --port PORT  The port the redis server is listening on (default:
                        6379)
  --password PASSWORD   The password to use for the redis server (takes
                        precedence over --password_env) (default: None)
  --password_env PASSWORD
                        The environment variable to obtain the password from
                        to use for connecting (default: None)
  -d DB, --database DB  The redis database to use (default: 0)
  -k KEY, --key KEY     The key to store the file content under (default:
                        None)
  -f FILE, --file FILE  The file to load into Redis (default: None)
```

### Save

Saves the content of a key in the Redis backend to a file.

```
usage: srh-save [-h] [-H HOST] [-p PORT] [--password PASSWORD]
                                [--password_env PASSWORD] [-d DB] -k KEY
                                [-f FILE] [-s]

Saves the content from a Redis key in the specified file.

optional arguments:
  -h, --help            show this help message and exit
  -H HOST, --host HOST  The redis server to connect to (default: localhost)
  -p PORT, --port PORT  The port the redis server is listening on (default:
                        6379)
  --password PASSWORD   The password to use for the redis server (takes
                        precedence over --password_env) (default: None)
  --password_env PASSWORD
                        The environment variable to obtain the password from
                        to use for connecting (default: None)
  -d DB, --database DB  The redis database to use (default: 0)
  -k KEY, --key KEY     The key to retrieve (default: None)
  -f FILE, --file FILE  The file to save the content in. Outputs the content
                        to stdout if not provided. (default: None)
  -s, --convert_to_string
                        Whether to convert the retrieved bytes to string
                        (default: False)
```

### Broadcast

For broadcasts data on a Redis channel.

```
usage: srh-broadcast [-h] [-H HOST] [-p PORT]
                                     [--password PASSWORD]
                                     [--password_env PASSWORD] [-d DB] -c
                                     CHANNEL [-f FILE] [-b] [-s STR]

Loads a file and broadcasts its content to the specified Redis channel.

optional arguments:
  -h, --help            show this help message and exit
  -H HOST, --host HOST  The redis server to connect to (default: localhost)
  -p PORT, --port PORT  The port the redis server is listening on (default:
                        6379)
  --password PASSWORD   The password to use for the redis server (takes
                        precedence over --password_env) (default: None)
  --password_env PASSWORD
                        The environment variable to obtain the password from
                        to use for connecting (default: None)
  -d DB, --database DB  The redis database to use (default: 0)
  -c CHANNEL, --channel CHANNEL
                        The channel to broadcast the content on (default:
                        None)
  -f FILE, --file FILE  The file to load into Redis (if not using a string)
                        (default: None)
  -b, --binary          Whether to treat the file as binary (default: False)
  -s STR, --string STR  The string to load into Redis (if not reading a file)
                        (default: None)
```

### Listen

Listens to messages being broadcast on a Redis channel.

```
usage: srh-listen [-h] [-H HOST] [-p PORT]
                                  [--password PASSWORD]
                                  [--password_env PASSWORD] [-d DB] -c CHANNEL
                                  [-D] [-s] [-o DIR] [-f FORMAT]

Listens to the specified channel for messages to come through and outputs them
on stdout if no output directory provided.

optional arguments:
  -h, --help            show this help message and exit
  -H HOST, --host HOST  The redis server to connect to (default: localhost)
  -p PORT, --port PORT  The port the redis server is listening on (default:
                        6379)
  --password PASSWORD   The password to use for the redis server (takes
                        precedence over --password_env) (default: None)
  --password_env PASSWORD
                        The environment variable to obtain the password from
                        to use for connecting (default: None)
  -d DB, --database DB  The redis database to use (default: 0)
  -c CHANNEL, --channel CHANNEL
                        The channel to broadcast the content on (default:
                        None)
  -D, --data_only       Whether to output only the message data (default:
                        False)
  -s, --convert_to_string
                        Whether to convert the message data to string
                        (requires --data_only) (default: False)
  -o DIR, --output_dir DIR
                        The directory to store the received messages/data in
                        (default: None)
  -f FORMAT, --file_format FORMAT
                        the format to use for the output files (when using '--
                        output_dir'), see: https://docs.python.org/3/library/d
                        atetime.html#strftime-and-strptime-format-codes
                        (default: %Y%m%d_%H%M%S.%f.dat)
```

### Ping

```
usage: srh-ping [-h] [-H HOST] [-p PORT] [--password PASSWORD]
                [--password_env PASSWORD] [-d DB]

Pings the redis host.

optional arguments:
  -h, --help            show this help message and exit
  -H HOST, --host HOST  The redis server to connect to (default: localhost)
  -p PORT, --port PORT  The port the redis server is listening on (default:
                        6379)
  --password PASSWORD   The password to use for the redis server (takes
                        precedence over --password_env) (default: None)
  --password_env PASSWORD
                        The environment variable to obtain the password from
                        to use for connecting (default: None)
  -d DB, --database DB  The redis database to use (default: 0)
```

