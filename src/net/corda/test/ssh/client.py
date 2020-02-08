import codecs, paramiko

class SSHClient():
    """Abstraction over making an SSH connection to a client, and executing commands on it. """

    def __init__(self, user, password, port, stdout, stderr):
        """Construct an instance of the ssh client and connect to the server.

        :param user: The username to use in the ssh connection
        :param password: The password to use in the ssh connection
        :param port: The port the ssh server is running on
        :param stdout: A file to store stdout of the connection
        :param stderr: A file to store stderr of the connection
        """
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect('localhost', port=port, username=user, password=password)
        self.stdout = stdout
        self.stderr = stderr


    def execute(self, command, timeout):
        """Execute a command on the ssh server and write to stdout.

        :param command: The command to execute
        :param timeout: The timeout period to wait for the command to complete.
        :return: 
        """
        _stdin, _stdout, _stderr = self.executeCommand(command, timeout)
        with codecs.open(self.stdout, 'w', encoding='utf-8') as fp:
            for line in _stdout.readlines():
                fp.write('%s\n'%line.strip())
            fp.close()
        map(lambda x: x.close(), [_stdin, _stdout, _stderr])
        return self


    def executeCommand(self, command, timeout):
        """Execute a command and return a tuple of the stdin, stdout and stderr

        :param command: The command to execute
        :param timeout: The timeout period to wait for the command to complete.
        :return: Tuple of (stdin, stdout, stderr)
        """
        return self.ssh.exec_command(command, get_pty=True, timeout=timeout)


    def close(self):
        """Close down the SSH connection to the server."""
        self.ssh.close()


