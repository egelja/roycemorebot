<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="https://i0.wp.com/roycemoreschool.org/wp-content/uploads/2019/03/cropped-Screen-Shot-2019-02-15-at-12.46.45-PM.png" alt="Project logo"></a>
</p>

<h3 align="center">Roycemore Bot</h3>

<div align="center">

![Bitbucket open issues](https://img.shields.io/bitbucket/issues-raw/NinoMaruszewski/roycemorebot?style=for-the-badge)
![Bitbucket open pull requests](https://img.shields.io/bitbucket/pr-raw/NinoMaruszewski/roycemorebot?style=for-the-badge)
[![License](https://img.shields.io/badge/License-MIT-brightgreen?style=for-the-badge)](./LICENSE)

</div>

---

<p align="center"> A bot for the Roycemore Discord server.
    <br>
</p>

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Built Using](#built_using)
- [TODO](./TODO.md)
- [Contributing](./CONTRIBUTING.md)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)

## About

This is s a Discord bot for the Roycemore Discord server. It provides moderation tools and is a "serious bot" without many games.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See [deployment](#deployment) for notes on how to deploy the project on a live system.

### Prerequisites

First install pipenv:

```sh
pip install pipenv
```

### Installing

Now install everything you need from the Pipfile. This will also create a virtual environment.

```sh
pipenv sync --dev
```

Now set up `pre-commit`:

```sh
pipenv run precommit
```

## Usage

Starting the bot:

```sh
pipenv run start
```

Linting:

```sh
pipenv run lint
```
## Deployment

You can use [PM2](https://pm2.keymetrics.io/) to deploy it. If you have a better solution, create an issue in the issue tracker.

## Built Using

- [Discord.py](https://discordpy.readthedocs.io/en/latest/) - Discord API interface
- [SQLite3](https://sqlite.org/index.html) - Database

## Authors <a name = "authors"></a>

- [@NinoMaruszewski](https://bitbucket.org/NinoMaruszewski/) - Idea & Initial work
