# Releasing

A version is published by pushing a tag `v<version>`. The `Release` workflow then runs the checks, builds the
package, publishes it on TestPyPI, waits for an approval on GitHub, publishes it on PyPI, publishes the
documentation site and creates the GitHub release with the changes of `CHANGELOG.md`.

1. A minor or major version, such as `0.2.0` or `1.0.0`, is first tried as a release candidate: set
   `version = "0.2.0rc1"` in `pyproject.toml`, commit, then push the branch and the tag at once. A release candidate
   only goes to TestPyPI. Check its page and its installation, and fix with `0.2.0rc2` and so on until it is right.
2. Set the final version in `pyproject.toml`, and replace `## [Unreleased]` with `## [0.2.0] - <date>` in
   `CHANGELOG.md`. Commit, then push the branch and the tag at once.
3. Check the version on TestPyPI, then approve the `pypi` environment in the workflow run on GitHub.

A patch version, such as `0.1.1`, skips step 1. When TestPyPI shows a problem, the approval is refused and the patch
is tried again as `0.1.1rc1`.

`git push origin main v0.2.0rc1` sends the branch and this tag only, in one push: the checks run once, and a tag
left on the computer is never sent by mistake.

```
git tag v0.2.0rc1
git push origin main v0.2.0rc1
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ numdaplot==0.2.0rc1
```

