# Introduction

This package builds JavaScript projects with [`yarn`](https://yarnpkg.com).
It contains a [`zest.releaser`](http://pypi.org/project/zest.releaser)
entry point and a stand-alone command line tool.

## Goal

You want to release a package that has a `packages.json` on it
and a `release` script defined on it.

Usually one does not want to keep the generated files on VCS,
but you want them when releasing with `zest.releaser`.

## Credits

This package is a direct inspiration from
[`zest.pocompile`](https://pypi.org/project/zest.pocompile) from Maurits van Rees.

Thanks!

## To Do

Add tests

