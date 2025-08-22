import subprocess
import sys
import argparse

def get_latest_tag():
    try:
        result = subprocess.run(['git', 'describe', '--tags', '--abbrev=0'], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return "v0.0.0"

def is_commit_tagged():
    try:
        result = subprocess.run(['git', 'tag', '--contains', 'HEAD'], capture_output=True, text=True, check=True)
        return len(result.stdout.strip()) > 0
    except subprocess.CalledProcessError:
        return False

def increment_patch(version):
    parts = version.replace('v', '').split('.')
    if len(parts) != 3:
        raise ValueError(f"Invalid version format: {version}")
    major, minor, patch = map(int, parts)
    new_patch = patch + 1
    return f"v{major}.{minor}.{new_patch}"

def get_version(update_tags=False):
    latest_tag = get_latest_tag()
    if is_commit_tagged():
        tags = subprocess.run(['git', 'tag', '--contains', 'HEAD'], capture_output=True, text=True, check=True).stdout.strip().split('\n')
        version = max(tags, key=lambda x: [int(y) for y in x.replace('v', '').split('.')]) if tags else latest_tag
        print(f"Current tag: {version}")
    else:
        new_version = increment_patch(latest_tag)
        if [int(x) for x in new_version.replace('v', '').split('.')] <= [int(x) for x in latest_tag.replace('v', '').split('.')]:
            raise ValueError(f"Calculated version {new_version} is lower than or equal to latest tag {latest_tag}")
        print(f"Current tag: {latest_tag}, Next tag: {new_version}")
        if update_tags:
            print(f"Creating new tag: {new_version}")
            subprocess.run(['git', 'tag', new_version], check=True)
            subprocess.run(['git', 'push', 'origin', new_version], check=True)
        version = new_version if not is_commit_tagged() else latest_tag
    return version

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage version tags for the project.")
    parser.add_argument('--update-tags', action='store_true', help="Create and push a new tag to the repository")
    args = parser.parse_args()

    if len(sys.argv) == 1:
        try:
            version = get_version()
            print(f"VERSION={version}")
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        except subprocess.CalledProcessError as e:
            print(f"Error: Failed to execute Git command: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.update_tags:
        try:
            version = get_version(args.update_tags)
            print(f"VERSION={version}")
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        except subprocess.CalledProcessError as e:
            print(f"Error: Failed to execute Git command: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(0)
