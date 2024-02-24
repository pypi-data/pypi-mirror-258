# Manual deploy process

## Test publish

First set up a section of your ~/.pypirc with a token

```
[testpypi]
  username = __token__
  password = <your token here, like pypi-AaBbCcDdEd...>
```

Then increment the version number in pyproject.yaml and open that PR. Download
the wheels artifact (aprox. 100MB) from the GitHub CI workflow
python-client-build.yml and copy it into the dist directory.

```
# This is only required for distribution
rm -r dist python/_convex/_convex.*.so
poetry run maturin build --out dist
# test publish
MATURIN_REPOSITORY=testpypi maturin upload dist/*
# Now you can download thei convex package from test pypi
python -m pip install --index-url https://test.pypi.org/simple/ convex
```

## Prerelease publish

# TODO before release

- [x] hook up smoke tests
- [x] build for multiple Python versions (requires using more limited ABI)
  - [x] use native Python error class
  - [x] change the interface to not throw ConvexError
- [x] confirm that mypy types are working
- [x] implement set_debug and set_admin_auth
- [x] fix values behavior! We need
  - [x] reference ConvexInt64 from Rust
  - [x] coercion! Keep the same Python behavior (which means we need a Python
        pass first)
  - [x] tests: seems broken right now?
- [x] Copy over the detailed docstrings and doctests
- [x] build scripts for python
- [x] provide new API for legacy HTTP
- [x] set up CI for automated test releases
- [x] manually publish a test release
- [ ] manually publish a prerelease release
- [ ] update mergify for new CI tasks
- [ ] write tests for subscription APIs
- [ ] delete old python-packages/convex directory and squash so that git history
      gets carried over

comming soon

- [ ] document how disconnecting works: WebSocket will continue to attempt to
      reconnect
- [ ] document surprising ctrl-c behaviors: subscription may or may not be lost?
- [ ] remove 3.8 compatibility code
- [ ] Is there a way to query connection status?
- [ ] fix client header (it'll just be the Rust one by default)
- [ ] pring logs as a side effect of the query, not a side effect of the
      internal implementation
- [ ] restore original set_debug() behavior (printing logs is currently on by
      default)
- [ ] confirm that APIs remain backward-compatible (particularly timing,
      retries, timeouts)
  - [ ] does URL validation happen at the same point?
  - [ ] track whether connection has ever occurred? Currently WebSocket
        reconnection just keeps being attempted.
- [ ] test async methods at the lower layer; they don't work in examples
- [ ] fix or remove **aiter** methods used in example.py
- [ ] simplify internal subscription.exists() logic (the async code we're
      removing should eliminate some of it)
- [ ] remove irrelevant examples
- [ ] figure out if an sdist distribution is possible
- [ ] set up new Copybara script
- [ ] set up CI for real relases - we need some GitHub secrets for this
