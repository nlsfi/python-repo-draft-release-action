# python-repo-draft-release-action

GitHub action for creating draft releases for python repositories.

The action:

1. Replaces the `## Unreleased` header of the changelog with `## <version> - <date>`
   and sets the version in the version file.
2. Commits and pushes the changes (`chore: release version <version>`).
3. Adds a new `## Unreleased` header to the changelog and sets the next version
   in the version file (`<version>.post0` by default).
4. Commits and pushes the changes (`chore: bump version to <next_version>`).
5. Creates a draft GitHub release for the release commit with the changelog
   section as the body.

## Requirements

- The version file is either a python file containing a line
  `__version__ = "<version>"` or a `pyproject.toml` with a static `[project]`
  `version`. A `pyproject.toml` is updated with `uv version`, which also updates
  the root package version in `uv.lock` if the lock file exists.
- The changelog must start with `# CHANGELOG` and contain a `## Unreleased` header.
- The workflow needs `contents: write` permission.

## Usage

```yaml
name: Create draft release

on:
  workflow_dispatch:
    inputs:
      version:
        required: true
        description: Version number without "v" tag prefix (i.e. "1.0.0")

jobs:
  draft-release:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v7
      - uses: nlsfi/python-repo-draft-release-action@v1
        with:
          version: ${{ inputs.version }}
          version_file: src/my_package/__init__.py
```

### Inputs

| Name             | Required | Default               | Description                                                   |
| ---------------- | -------- | --------------------- | ------------------------------------------------------------- |
| `version`        | yes      |                       | Release version without the tag prefix (e.g. `1.0.0`)         |
| `version_file`   | yes      |                       | Path to the file containing `__version__` or `pyproject.toml` |
| `changelog_file` | no       | `CHANGELOG.md`        | Path to the changelog file                                    |
| `next_version`   | no       | `<version>.post0`     | Version to set after the release                              |
| `tag_prefix`     | no       | `v`                   | Prefix of the release tag                                     |
| `token`          | no       | `${{ github.token }}` | Token used to create the draft release                        |

### Outputs

| Name                 | Description                              |
| -------------------- | ---------------------------------------- |
| `version`            | Normalized release version               |
| `next_version`       | Normalized version set after the release |
| `release_commit_sha` | SHA of the release commit                |

## Scripts

The scripts in `src/draft_release` can also be used directly:

```shell
python -m draft_release.get_version <version_file>
python -m draft_release.parse_version <version> [base]
python -m draft_release.set_version <version_file> <version>
python -m draft_release.update_changelog <version|Unreleased> [changelog_file]
python -m draft_release.extract_changes <version> [changelog_file]
```

## Development

```shell
uv sync
uv run prek install
```
