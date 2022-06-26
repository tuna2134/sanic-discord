import subprocess

def _get_version(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
    version = None
    for line in lines:
        if "__version__" in line:
            version = line.split()[2]
            break
    return version.replace('"', '')

version = _get_version("sanic_discord/__init__.py")
if "a" in version:
    result = subprocess.run(["git", "log", "--oneline", "-1"], stdout=subprocess.PIPE)
    version += result.stdout.decode().split()[0]

print(version)