#!/usr/bin/env python3

# Translates juju actions to the etckeeper CLI and returns any output that
# would normally be returned by etckeeper

# TO-DO:
#  - Return stdout, stderr, etc. using action_set
#  - Create Unit / Mock tests

from traceback import format_exc
from subprocess import run, PIPE
from sys import argv
from os.path import basename

from charmhelpers.core.hookenv import action_fail, action_get, action_set

def main():
    # Base commmand
    cmd = [ "etckeeper" ]

    # Append subcommand
    cmd.append(basename(argv[0]))

    # Based on subcommand append action params
    if cmd == "commit":
        msg = action_get("msg")
        if msg:
            cmd.append('"{}"'.format(msg))

    if cmd == "update-ignore":
        present = action_get("present")
        if present:
            if eval(present.title()):
                cmd.append("-a")

    if cmd == "uninit":
        cmd.append('-f')

    if cmd == "update-ignore":
        present = action_get("present")
        if present:
            if eval(present.title()):
                cmd.append("-a")

    if cmd == "vcs":
        # Append VCS subcommand
        cmd.append(action_get("cmd"))

        # Get any VCS subcommand options and append
        try:
            vcs_opt = action_get("opt").split()
        except:
            vcs_opt = None

        if vcs_opt:
            cmd.extend(vcs_opt)

    action_set("command", " ".join(cmd))

    try:
        completed = run(cmd, stdout=PIPE, stderr=PIPE)
    except subprocess.CalledProcessError as e:
        action_set("error", e)
    except Except as e:
        action_set("traceback", format_exc())
        action_fail("{} resulted in an unexpected error".format(cmd[1]))
    else:
        action_set("rc", completed.returncode)
        action_set("stdout", completed.stdout.decode("UTF-8"))
        action_set("stderr", completed.stderr.decode("UTF-8"))

if __name__ == '__main__':
    main()
