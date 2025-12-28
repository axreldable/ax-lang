# Automatic Version Bumping

This project uses an automated version bumping system that runs on every merge to the `master` branch.

## How It Works

When code is merged to `master`, the GitHub Actions workflow automatically:

1. Determines the type of version bump (patch, minor, or major)
2. Updates the version in `python/pyproject.toml`
3. Creates a git commit with the version change
4. Creates a git tag for the new version (e.g., `v0.14.4`)
5. Pushes the commit and tag to the repository
6. Creates a GitHub Release with auto-generated release notes

## Version Bump Types

The workflow follows [Semantic Versioning](https://semver.org/):

- **Patch** (`X.Y.Z` → `X.Y.Z+1`): Bug fixes and minor changes (default)
- **Minor** (`X.Y.Z` → `X.Y+1.0`): New features, backwards compatible
- **Major** (`X.Y.Z` → `X+1.0.0`): Breaking changes

### Examples

- Patch: `0.14.1` → `0.14.2`
- Minor: `0.14.1` → `0.15.0`
- Major: `0.14.1` → `1.0.0`

## Triggering Different Bump Types

### Default: Patch Bump

By default, every merge to `master` will increment the patch version.

### Minor Version Bump

Use **either** of these methods:

1. **PR Labels**: Add the `release:minor` label to your pull request
2. **Commit Message**: Include `[minor]` in your commit message

Example commit message:
```
Add new feature for user authentication [minor]
```

### Major Version Bump

Use **either** of these methods:

1. **PR Labels**: Add the `release:major` label to your pull request
2. **Commit Message**: Include `[major]` in your commit message

Example commit message:
```
Refactor API with breaking changes [major]
```

### Manual Trigger

You can also manually trigger a version bump:

1. Go to the [Actions tab](https://github.com/axreldable/ax-lang/actions/workflows/version-bump.yml)
2. Click "Run workflow"
3. Select the branch (usually `master`)
4. Choose the bump type (patch, minor, or major)
5. Click "Run workflow"

## Idempotency

The workflow is designed to be idempotent:

- It checks if the last commit was already a version bump
- If so, it skips the bump to avoid duplicate version increments
- This prevents issues when the workflow is re-run or triggered multiple times

## Priority Order

When multiple bump type indicators are present, the workflow uses this priority:

1. **Manual workflow dispatch** (highest priority)
2. **PR labels** (`release:major` or `release:minor`)
3. **Commit message keywords** (`[major]` or `[minor]`)
4. **Default** (patch bump - lowest priority)

## Release Process

After the version is bumped:

1. The release workflow (`.github/workflows/release.yml`) is automatically triggered by the new tag
2. Tests and coverage checks are run
3. If all checks pass, the package is published to PyPI

## Troubleshooting

### Version wasn't bumped

- Check that your commit was merged to `master` branch
- Verify the workflow ran in the Actions tab
- Check if the last commit was already a version bump (workflow will skip)

### Wrong version bump type

- Check your PR labels in the Pull Request page
- Check your commit message for keywords (`[minor]` or `[major]`)
- If needed, manually trigger the workflow with the correct bump type

## Script Usage

The version bumping script can also be used locally:

```bash
# Dry run to see what would change
python .github/scripts/bump_version.py patch --dry-run

# Actually bump the version
python .github/scripts/bump_version.py minor

# Specify custom pyproject.toml path
python .github/scripts/bump_version.py major --pyproject /path/to/pyproject.toml
```