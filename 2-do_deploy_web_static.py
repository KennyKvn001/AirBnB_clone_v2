#!/usr/bin/python3
from fabric.api import env, put, run
import os


env.user = "ubuntu"
env.hosts = ["204.236.196.88", "34.224.218.238"]
env.key_filename = "~/.ssh/school"


def do_deploy(archive_path):
    """Distributes an archive to your web servers"""
    if not os.path.exists(archive_path):
        print("Archive does not exist:", archive_path)
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        print("Uploading archive...")
        put(archive_path, "/tmp/")
        print("Archive uploaded successfully")

        # Extract archive filename
        archive_name = os.path.basename(archive_path)
        archive_name_no_ext = os.path.splitext(archive_name)[0]

        # Uncompress the archive to /data/web_static/releases/<archive filename without extension>
        print("Extracting archive...")
        run("mkdir -p /data/web_static/releases/{}/".format(archive_name_no_ext))
        run(
            "tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(
                archive_name, archive_name_no_ext
            )
        )
        print("Archive extracted successfully")

        # Delete the archive from the web server
        print("Deleting archive...")
        run("rm /tmp/{}".format(archive_name))
        print("Archive deleted successfully")

        # Move contents to proper location
        print("Moving contents to proper location...")
        run(
            "mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(
                archive_name_no_ext, archive_name_no_ext
            )
        )

        # Remove the now empty directory
        print("Removing empty directory...")
        run(
            "rm -rf /data/web_static/releases/{}/web_static".format(archive_name_no_ext)
        )

        # Check if my_index.html exists in the expected location
        index_path = "/data/web_static/releases/{}/my_index.html".format(
            archive_name_no_ext
        )
        index_exists = run("test -f {}".format(index_path), warn=True).succeeded

        if index_exists:
            print("my_index.html found at:", index_path)
        else:
            print("ERROR: my_index.html not found at:", index_path)
            return False

        # Delete the symbolic link /data/web_static/current from the web server
        print("Deleting current symlink...")
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        print("Creating new symlink...")
        run(
            "ln -s /data/web_static/releases/{}/ /data/web_static/current".format(
                archive_name_no_ext
            )
        )

        print("New version deployed!")
        return True
    except Exception as e:
        print("Deployment failed:", e)
        return False
