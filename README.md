# TemplateProject

## Development 🧑‍💻

### Requirements 📝

* [Python 3.6.2+](https://www.python.org/downloads/) (I recommend using [pyenv](https://github.com/pyenv/pyenv) to handle Python versions)
* [Poetry](https://github.com/python-poetry/poetry)
* [Node 14](https://nodejs.org/en/) (I recommend using NVM [Node Version Manager](https://github.com/nvm-sh/nvm))
* [AWS CDK](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html) - There is a `package.json` in the cdk examples, it's recommended to run `npm install` in the examples directories and make use of `npx <command>` rather than globally installing AWS CDK
* [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html)
* [Docker](https://docs.docker.com/get-docker/)

If you're developing on MacOS, the above can be installed using [homebrew](https://brew.sh/)

If you're developing on Windows, I'd recommend using either [Git BASH](https://gitforwindows.org/) or [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10)

_I provide a [`Makefile`](./Makefile) to try and abstract away some of the commonly used commands, so you may want to get `make` also_

### `.env` file

A file named `.env` is expected at the base of the repository with the following values:

```
AWS_DEFAULT_PROFILE="your-named-aws-profile"
AWS_DEFAULT_REGION="your-aws-region"
OWNER="your-name"
IDENTIFIER="a-unique-id-for-the-deployment"
```

A file named `example.env` is provided, copy this and fill it out with your values.

### Getting started 🏃‍♀️

To get setup for overall development, install the above [requirements](#requirements) first.

To remove the filler values from this template, replace the header `Template Project` in
[README.md](./README.md) and then also replace `TemplateProject` in both
[app.py](./cdk/app.py) and [stack.py](./cdk/stack.py) with `YourProjectName`.

You can then install the dependencies for development with:

```console
make install
```

### Makefile goodness 🤌

A `Makefile` is available in the root of the repository to abstract away commonly used commands for development:

**`make install`**

> This will run both `npm` and `poetry` to install the project dependencies

**`make lint`**

> This will perform a dry run of `flake8`, `isort`, and `black` and let you know what issues were found

**`make format`**

> This will perform a run of `isort` and `black`, this **will** modify files if issues were found

**`make unit-tests`**

> This will run `pytest` within the `tests/unit` directory

**`make diff`**

> This will run a `cdk diff` using the contents of your `.env` file

**`make deploy`**

> This will run a `cdk deploy` using the contents of your `.env` file. The deployment is auto-approved, so **make sure** you know what you're changing with your deployment first! (Best to run `make diff` to check!)

**`make destroy`**

> This will run a `cdk destroy` using the contents of your `.env` file. The destroy is auto-approved, so **make sure** you know what you're destroying first!
