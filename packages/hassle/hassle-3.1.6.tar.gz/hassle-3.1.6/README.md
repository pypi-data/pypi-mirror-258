# Hassle

Automate creating, building, testing, and publishing Python packages from the command line.   

## Installation

Install with:

<pre>
pip install hassle
</pre>

You should be able to type `hassle help` in your terminal and see a list of commands:
<pre>
>hassle help

Documented commands (type help {topic}):
========================================
add_script  check_pypi  configure  help     is_published  publish  sys   update
build       config      format     install  new           quit     test
</pre>


### Additional setup:

Install git and add it to your PATH if it isn't already.  
Some parts of this tool may require [communicating with Github]((https://docs.github.com/en/get-started/getting-started-with-git/caching-your-github-credentials-in-git)).  
You will also need to register a [pypi account](https://pypi.org/account/register/) if you want to publish packages to https://pypi.org with this tool.  
Once you've created and validated an account, you will need to follow the directions to generate an [api key](https://pypi.org/help/#apitoken).  
Copy the key and in your home directory, create a '.pypirc' file if it doesn't already exist.  
Edit the file so it contains the following (don't include the brackets around your api key):

<pre>
[distutils]
index-servers =
    pypi

[pypi]
username = __token__
password = pypi-{The api key you copied}
</pre>

## Configuration

After installation and the above additional setup, it is a good idea to run the 'configure' command.
This isn't required and a blank config will be generated whenever it is needed if it doesn't exist.
This info, if provided, is used to populate a new project's 'pyproject.toml' file.
Typing `hassle help configure`:

<pre>
>hassle help configure
Edit or create `hassle_config.toml`.
Parser help for configure:
usage: config [-h] [-n NAME] [-e EMAIL] [-g GITHUB_USERNAME] [-d DOCS_URL] [-t TAG_PREFIX]

Edit or create the `hassle_config.toml` file.

options:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  Your name. This will be used to populate the 'authors' field of a packages 'pyproject.toml'.
  -e EMAIL, --email EMAIL
                        Your email. This will be used to populate the 'authors' field of a packages 'pyproject.toml'.
  -g GITHUB_USERNAME, --github_username GITHUB_USERNAME
                        Your github username name. When creating a new package, say with the name 'mypackage', the pyproject.toml 'Homepage' field will be set to 'https://github.com/{github_username}/mypackage' and the 'Source code' field will be set to
                        'https://github.com/{github_username}/mypackage/tree/main/src/mypackage'.
  -d DOCS_URL, --docs_url DOCS_URL
                        The template url to be used in your pyproject.toml file indicating where your project docs will be hosted. Pass the url with '$name' as a placeholder for where the package name should go, e.g. 'https://somedocswebsite/user/projects/$name'. If
                        'hassle_config.toml' didn't exist prior to running this tool and nothing is given for this arg, it will default to using the package's github url. e.g. for package 'mypackage' the url will be 'https://github.com/{github_username}/mypackage/tree/main/docs'
  -t TAG_PREFIX, --tag_prefix TAG_PREFIX
                        When using Hassle to do `git tag`, this will be prefixed to the front of the version number in the `pyproject.toml` file.
</pre>

You can also view the current contents with the `config` command:
<pre>
>hassle config
[[authors]]
name = "Matt Manes"
email = "mattmanes@pm.me"

[project_urls]
"Homepage" = "https://github.com/matt-manes/$name"
"Documentation" = "https://github.com/matt-manes/$name/tree/main/docs"
"Source code" = "https://github.com/matt-manes/$name/tree/main/src/$name"

[git]
tag_prefix = "v"
</pre>

## Generating New Projects
New projects are generated with the `new` command:  

<pre>
>hassle help new
Create a new project.
Parser help for new:
usage: new [-h] [-s [SOURCE_FILES ...]] [-d [DESCRIPTION ...]] [-dp [DEPENDENCIES ...]] [-k [KEYWORDS ...]] [-as] [-nl] [-np] name

Create a new project in the current directory.

positional arguments:
  name                  Name of the package to create in the current working directory.

options:
  -h, --help            show this help message and exit
  -s [SOURCE_FILES ...], --source_files [SOURCE_FILES ...]
                        List of additional source files to create in addition to the default __init__.py and {name}.py files.
  -d [DESCRIPTION ...], --description [DESCRIPTION ...]
                        The package description to be added to the pyproject.toml file.
  -dp [DEPENDENCIES ...], --dependencies [DEPENDENCIES ...]
                        List of dependencies to add to pyproject.toml. Note: hassle.py will automatically scan your project for 3rd party imports and update pyproject.toml. This switch is largely useful for adding dependencies your project might need, but doesn't directly import
                        in any source files, like an os.system() call that invokes a 3rd party cli.
  -k [KEYWORDS ...], --keywords [KEYWORDS ...]
                        List of keywords to be added to the keywords field in pyproject.toml.
  -as, --add_script     Add section to pyproject.toml declaring the package should be installed with command line scripts added. The default is '{package_name} = "{package_name}.{package_name}:main".
  -nl, --no_license     By default, projects are created with an MIT license. Set this flag to avoid adding a license if you want to configure licensing at another time.
  -np, --not_package    Put source files in top level directory and delete tests folder.
</pre>

Most of these options pertain to prefilling the generated 'pyproject.toml' file.  
As a simple example we'll create a new package called 'nyquil':

<pre>
>hassle new nyquil -d "A package to help you sleep when you're sick." -k sleep sick -as
Initialized empty Git repository in E:/1vsCode/python/nyquil/.git/
</pre>

A new folder in your current working directory called 'nyquil' should now exist.  
It should have the following structure:

<pre>
nyquil
|  |-.git
|  |  |-config
|  |  |-description
|  |  |-HEAD
|  |  |-hooks
|  |  |  |-applypatch-msg.sample
|  |  |  |-commit-msg.sample
|  |  |  |-fsmonitor-watchman.sample
|  |  |  |-post-update.sample
|  |  |  |-pre-applypatch.sample
|  |  |  |-pre-commit.sample
|  |  |  |-pre-merge-commit.sample
|  |  |  |-pre-push.sample
|  |  |  |-pre-rebase.sample
|  |  |  |-pre-receive.sample
|  |  |  |-prepare-commit-msg.sample
|  |  |  |-push-to-checkout.sample
|  |  |  |_update.sample
|  |  |
|  |  |-info
|  |  |  |_exclude
|  |
|  |-.gitignore
|  |-.vscode
|  |  |_settings.json
|  |
|  |-LICENSE.txt
|  |-pyproject.toml
|  |-README.md
|  |-src
|  |  |-nyquil
|  |  |  |-__init__.py
|  |  |  |_nyquil.py
|  |
|  |-tests
|  |  |_test_nyquil.py
</pre>

**Note: By default an MIT License is added to the project. Pass the `-nl/--no_license` flag to prevent this behavior.**  
If you open the 'pyproject.toml' file it should look like the following except
for the 'project.authors' and 'project.urls' sections:

<pre>
[project]
name = "nyquil"
description = "A package to help you sleep when you're sick."
version = "0.0.0"
dependencies = []
readme = "README.md"
keywords = ["sleep", "sick"]
classifiers = ["Programming Language :: Python :: 3", "License :: OSI Approved :: MIT License", "Operating System :: OS Independent"]
requires-python = ">=3.10, <3.12"

[[project.authors]]
name = "Matt Manes"
email = "mattmanes@pm.me"

[project.urls]
Homepage = "https://github.com/matt-manes/nyquil"
Documentation = "https://github.com/matt-manes/nyquil/tree/main/docs"
"Source code" = "https://github.com/matt-manes/nyquil/tree/main/src/nyquil"

[project.scripts]
nyquil = "nyquil.nyquil:main"

[tool]
[tool.pytest.ini_options]
addopts = ["--import-mode=importlib"]
pythonpath = "src"

[tool.hatch.build.targets.sdist]
exclude = [".coverage", ".pytest_cache", ".vscode", "tests", ".gitignore"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
</pre>

The package would do absolutely nothing, but with the generated files we do have the
viable minimum to build an installable python package.


## Running Tests

Hassle uses [Pytest](https://pypi.org/project/pytest/) and [Coverage](https://pypi.org/project/coverage/) to run tests.  
When we invoke the `hassle test` command,
we should see something like this (pretending we have added test functions to `tests/test_nyquil.py`):

<pre>
>hassle test
================================================================================================================================== test session starts ==================================================================================================================================
platform win32 -- Python 3.11.0, pytest-7.2.1, pluggy-1.0.0
rootdir: C:\python\nyquil, configfile: pyproject.toml
plugins: anyio-3.6.2, hypothesis-6.63.0
collected 1 item

tests\test_nyquil.py .

=================================================================================================================================== 1 passed in 0.06s ===================================================================================================================================
Name                     Stmts   Miss  Cover   Missing
------------------------------------------------------
src\nyquil\__init__.py       0      0   100%
src\nyquil\nyquil.py         6      0   100%
tests\test_nyquil.py         4      0   100%
------------------------------------------------------
TOTAL                       10      0   100%
</pre>


## Building

Building the package is as simple as using:

<pre>
>hassle build
</pre>

By default, the build command will:  
1. Run any tests in the `tests` folder (abandoning the build if any fail).  
2. Format source files with isort and black.  
3. Scan project import statements and add any missing packages to the pyproject `dependencies` field.  
4. Use [pdoc](https://pypi.org/project/pdoc/) to generate documentation (located in a created `docs` folder).  
5. Run `python -m build .` to generate the `tar.gz` and `.whl` files (located in a created `dist` folder).  


## Publishing

Assuming you've set up a [PyPi](https://pypi.org/) account, generated the api key, and configured the '.pypirc' 
file as mentioned earlier, then you can publish the current version of your package by running:

<pre>
>hassle publish
</pre>


## Updating

When the time comes to make changes to your package, the `hassle update` command makes it easy.  
This command needs at least one argument according to the type of update: `major`, `minor`, or `patch`.  
This argument tells Hassle how to increment the project version.  
Hassle uses the [semantic versioning standard](https://semver.org/),
so, for example, if your current version is `1.2.3` then 

`>hassle update major` bumps to `2.0.0`,  
`>hassle update minor` bumps to `1.3.0`,  
and  
`>hassle update patch` bumps to `1.2.4`.  

By default, the update command will:  
1. Run any tests in the `tests` folder (abandoning the update if any fail).  
2. Increment the project version.  
3. Run the build process as outlined above (minus step 1.).  
4. Make a commit with the message `chore: build {project_version}`.  
5. Git tag using the tag prefix in your `hassle_config.toml` file and the new project version.  
6. Generate/update the `CHANGELOG.md` file using [auto-changelog](https://pypi.org/project/auto-changelog/).  
(Normally `auto-changelog` overwrites the changelog file, but Hassle does some extra things so that any manual changes you make to the changelog are preserved).  
7. Git commit the changelog.  
8. Pull/push the current branch with the remote origin.  
9. Publish the updated package if the update command was run with the `-p` flag.  
10. Install the updated package if the update command was run with the `-i` flag.  

