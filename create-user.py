#!/usr/bin/python3
import os
import re
import sys

def main():
    for line in sys.stdin:
        # Check if the line starts with a #, skip it if it does.
        match = re.match('^#', line)

        # Split the line into fields separated by ':'.
        fields = line.strip().split(':')

        # Skip lines starting with # or those without five fields.
        if match or len(fields) != 5:
            continue

        username = fields[0]
        password = fields[1]
        gecos = "%s %s,,," % (fields[3], fields[2])

        # Split the groups field into individual groups.
        groups = fields[4].split(',')

        # Create a user account using the given information.
        print("==> Creating account for %s..." % username)
        cmd = "/usr/sbin/adduser --disabled-password --gecos '%s' %s" % (gecos, username)
        os.system(cmd)

        # Set the password for the user.
        print("==> Setting the password for %s..." % username)
        cmd = "/bin/echo -ne '%s\n%s' | /usr/bin/sudo /usr/bin/passwd %s" % (password, password, username)
        os.system(cmd)

        # Assign the user to each group provided.
        for group in groups:
            if group != '-':
                print("==> Assigning %s to the %s group..." % (username, group))
                cmd = "/usr/sbin/adduser %s %s" % (username, group)
                os.system(cmd)


if __name__ == '__main__':
    main()
