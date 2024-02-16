#!/usr/bin/python3
""" alu-Airbnb_clone_v2 - Deploy static, task 4. Keep it clean!
"""
from fabric.api import env, run, cd, sudo

env.hosts = ["204.236.196.88", "34.224.218.238"]
env.user = "ubuntu"


# Replace with the number of archives to keep
num_kp = 2


def do_clean(number=num_kp):
    """
    Deletes out-of-date archives locally and on web servers.

    Args:
        number: Number of archives (including the most recent) to keep.
    """

    with cd("versions"):
        # Get a list of archive filenames sorted by reverse creation time
        archives = sorted(run("ls -rt").split(), reverse=True)

        # Delete all but the first `number` archives
        for archive in archives[number:]:
            run("rm %s" % archive)

    # Run cleanup on both web servers
    for host in env.hosts:
        with cd("%s/releases" % host):
            # Connect to the server and run do_clean with the same number
            sudo("fab -H %s do_clean:%s" % (host, number))


if __name__ == "__main__":
    do_clean()
