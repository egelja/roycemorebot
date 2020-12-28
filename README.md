<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="https://i0.wp.com/roycemoreschool.org/wp-content/uploads/2019/03/cropped-Screen-Shot-2019-02-15-at-12.46.45-PM.png" alt="Project logo"></a>
</p>

<h3 align="center">Roycemore Bot</h3>

<div align="center">
  
[![GitHub issues](https://img.shields.io/github/issues/NinoMaruszewski/roycemorebot?style=for-the-badge)](https://github.com/NinoMaruszewski/roycemorebot/issues/)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/NinoMaruszewski/roycemorebot?style=for-the-badge)](https://github.com/NinoMaruszewski/roycemorebot/pulls/)
[![GitHub](https://img.shields.io/github/license/NinoMaruszewski/roycemorebot?style=for-the-badge)](./LICENSE)

</div>

---

<p align="center"> A bot for the Roycemore Discord server.
    <br>
</p>

## Table of Contents

- [About](#about)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Deployment](#deployment)
- [Built Using](#built-using)
- [Authors](#authors)
- [TODO](./TODO.md)
- [Contributing](./CONTRIBUTING.md)

## About <a name = "about"></a>

This is s a Discord bot for the Roycemore Discord server. It provides moderation tools and is a "serious bot" without many games.

## Getting Started <a name = "getting-started"></a>

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

## Usage <a name = "usage"></a>

Starting the bot:

```sh
pipenv run start
```

Linting:

```sh
pipenv run lint
```
## Deployment <a name = "deployment"></a>

You can use [PM2](https://pm2.keymetrics.io/) to deploy it. If you have a better solution, create an issue in the issue tracker.

## Built Using <a name = "built-using"></a>

- [Discord.py](https://discordpy.readthedocs.io/en/latest/) - Discord API interface
- [SQLite3](https://sqlite.org/index.html) - Database

## Authors <a name = "authors"></a>

- [@NinoMaruszewski](https://github.com/NinoMaruszewski/) - Idea & Initial work
