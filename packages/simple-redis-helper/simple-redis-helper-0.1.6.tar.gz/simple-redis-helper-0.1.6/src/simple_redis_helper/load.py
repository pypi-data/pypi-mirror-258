import argparse
import redis
import traceback
from simple_redis_helper.utils import get_password


def main(args=None):
    """
    The main method for parsing command-line arguments and running the application.

    :param args: the commandline arguments, uses sys.argv if not supplied
    :type args: list
    """
    parser = argparse.ArgumentParser(
        prog="srh-load",
        description="Loads a file into Redis under the specified key.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-H', '--host', metavar='HOST', required=False, default="localhost", help='The redis server to connect to')
    parser.add_argument('-p', '--port', metavar='PORT', required=False, default=6379, type=int, help='The port the redis server is listening on')
    parser.add_argument('--password', metavar='PASSWORD', required=False, default=None, type=str, help='The password to use for the redis server (takes precedence over --password_env)')
    parser.add_argument('--password_env', metavar='PASSWORD', required=False, default=None, type=str, help='The environment variable to obtain the password from to use for connecting')
    parser.add_argument('-d', '--database', metavar='DB', required=False, default=0, type=int, help='The redis database to use')
    parser.add_argument('-k', '--key', metavar='KEY', required=True, default=None, help='The key to store the file content under')
    parser.add_argument('-f', '--file', metavar='FILE', required=True, default=None, help='The file to load into Redis')
    parsed = parser.parse_args(args=args)

    # connect
    r = redis.Redis(host=parsed.host, port=parsed.port, db=parsed.database, password=get_password(parsed))

    with open(parsed.file, "r") as f:
        content = f.read()
        r.set(parsed.key, content)


def sys_main():
    """
    Runs the main function using the system cli arguments, and
    returns a system error code.
    :return: 0 for success, 1 for failure.
    :rtype: int
    """
    try:
        main()
        return 0
    except Exception:
        print(traceback.format_exc())
        return 1


if __name__ == '__main__':
    main()

