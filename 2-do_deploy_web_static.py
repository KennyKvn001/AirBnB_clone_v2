#!/usr/bin/python3
from fabric.api import env, put, run, cd
import os.path


env.user = "ubuntu"
env.hosts = ["204.236.196.88", "34.224.218.238"]
env.key_filename = "~/.ssh/id_rsa"


def do_deploy(archive_path):
    """Distributes an archive to your web servers"""
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")

        # Extract archive filename
        archive_name = os.path.basename(archive_path)
        archive_name_no_ext = os.path.splitext(archive_name)[0]

        # Uncompress the archive to /data/web_static/releases/<archive filename
        # without extension>
        run("mkdir -p /data/web_static/releases/{}".format(archive_name_no_ext))
        run(
            "tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(
                archive_name, archive_name_no_ext
            )
        )

        # Delete the archive from the web server
        run("rm /tmp/{}".format(archive_name))

        # Move contents to proper location
        run(
            "mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(
                archive_name_no_ext, archive_name_no_ext
            )
        )

        # Remove the now empty directory
        run(
            "rm -rf /data/web_static/releases/{}/web_static".format(archive_name_no_ext)
        )

        # Delete the symbolic link /data/web_static/current from the web server
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        run(
            "ln -s /data/web_static/releases/{} /data/web_static/current".format(
                archive_name_no_ext
            )
        )

        print("New version deployed!")
        return True
    except Exception as e:
        print("Deployment failed:", e)
        return False
