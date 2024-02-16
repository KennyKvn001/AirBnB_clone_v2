#!/usr/bin/python3
from fabric.api import env, put, run, cd
import os.path


env.user = "ubuntu"
env.hosts = ["204.236.196.88", "34.224.218.238"]
env.key_filename = "~/.ssh/id_rsa"


def do_deploy(archive_path):
    """
    Deploys the archive to both web servers.

    Args:
        archive_path (str): Path to the archive.

    Returns:
        bool: True if successful, False otherwise.
    """

    success = True
    try:
        for host in env.hosts:
            with cd(host):
                # Upload archive to /tmp/
                put(archive_path, "/tmp/")

                # Uncompress archive to releases/
                archive_filename = os.path.basename(archive_path)
                release_dir = (
                    f"/data/web_static/releases/{archive_filename.split('.')[0]}"
                )
                run(f"tar -xzf /tmp/{archive_filename} -C {release_dir}")

                # Delete archive from /tmp/
                run(f"rm /tmp/{archive_filename}")

                # Delete current symbolic link (if exists)
                try:
                    run("rm /data/web_static/current")
                except Exception as e:
                    # Ignore if link doesn't exist
                    pass

                # Create new symbolic link to the new version
                run(f"ln -sf {release_dir} /data/web_static/current")

    except Exception as e:
        print(f"Error deploying on {host}: {e}")
        success = False

    return success
