######################################################################
#  This file is part of gmpxxyy.
#
#        Copyright (C) 2020-2025 Julian Rüth
#
#  gmpxxyy is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or (at your
#  option) any later version.
#
#  gmpxxyy is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with gmpxxyy. If not, see <https://www.gnu.org/licenses/>.
#####################################################################

import sys

try:
  input("Are you sure you are on the master branch which is identical to origin/master? [ENTER]")
except KeyboardInterrupt:
  sys.exit(1)

from rever.activities.command import command

command('build', 'python -m build')
command('twine', 'twine upload dist/*')

$PROJECT = 'gmpxxyy'

$ACTIVITIES = [
    'version_bump',
    'changelog',
    'build',
    'tag',
    'twine'
    'push_tag',
    'ghrelease',
]

$VERSION_BUMP_PATTERNS = [
    ('pyproject.toml', r"version =", 'version = "$VERSION"'),
]

$CHANGELOG_FILENAME = 'ChangeLog'
$CHANGELOG_TEMPLATE = 'TEMPLATE.rst'
$CHANGELOG_NEWS = 'doc/news'
$CHANGELOG_CATEGORIES = ('Added', 'Changed', 'Deprecated', 'Removed', 'Fixed', 'Performance')
$PUSH_TAG_REMOTE = 'git@github.com:flatsurf/gmpxxyy.git'

$GITHUB_ORG = 'flatsurf'
$GITHUB_REPO = 'gmpxxyy'

$GHRELEASE_ASSETS = ['gmpxxyy-' + $VERSION + '.tar.gz']
