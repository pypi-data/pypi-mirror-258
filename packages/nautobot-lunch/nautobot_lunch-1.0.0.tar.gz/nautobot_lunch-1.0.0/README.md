# Nautobot Lunch

<p align="center">
  <img src="https://raw.githubusercontent.com/nlgotz/nautobot-app-lunch/develop/docs/images/icon-lunch.png" class="logo" height="200px">
  <br>
  <a href="https://github.com/nlgotz/nautobot-app-lunch/actions"><img src="https://github.com/nlgotz/nautobot-app-lunch/actions/workflows/ci.yml/badge.svg?branch=main"></a>
  <a href="https://nautobot-lunch.readthedocs.io/projects/lunch/en/latest/"><img src="https://readthedocs.org/projects/nautobot-plugin-lunch/badge/"></a>
  <a href="https://pypi.org/project/lunch/"><img src="https://img.shields.io/pypi/v/lunch"></a>
  <a href="https://pypi.org/project/lunch/"><img src="https://img.shields.io/pypi/dm/lunch"></a>
  <br>
  An <a href="https://www.networktocode.com/nautobot/apps/">App</a> for <a href="https://nautobot.com/">Nautobot</a>.
</p>

## Overview

This app queries Yelp to find lunch (or breakfast or dinner, we don't discriminate) near a location. The goal of this is to make it easier for field personel to find food near the site they are at. Or to re-arrange the order you want to visit sites so that you actually end up eating a good lunch.

### Screenshots

More screenshots can be found in the [Using the App](https://nautobot-lunch.readthedocs.io/projects/lunch/en/latest/user/app_use_cases/) page in the documentation. Here's a quick overview of some of the app's added functionality:

![Nautobot Lunch](https://raw.githubusercontent.com/nlgotz/nautobot-app-lunch/develop/docs/images/nautobot-lunch-1.png)

## Documentation

Full documentation for this App can be found over on the [Nautobot Docs](https://nautobot-lunch.readthedocs.io) website:

- [User Guide](https://nautobot-lunch.readthedocs.io/projects/lunch/en/latest/user/app_overview/) - Overview, Using the App, Getting Started.
- [Administrator Guide](https://nautobot-lunch.readthedocs.io/projects/lunch/en/latest/admin/install/) - How to Install, Configure, Upgrade, or Uninstall the App.
- [Developer Guide](https://nautobot-lunch.readthedocs.io/projects/lunch/en/latest/dev/contributing/) - Extending the App, Code Reference, Contribution Guide.
- [Release Notes / Changelog](https://nautobot-lunch.readthedocs.io/projects/lunch/en/latest/admin/release_notes/).
- [Frequently Asked Questions](https://nautobot-lunch.readthedocs.io/projects/lunch/en/latest/user/faq/).

### Contributing to the Documentation

You can find all the Markdown source for the App documentation under the [`docs`](https://github.com/nlgotz/nautobot-app-lunch/tree/develop/docs) folder in this repository. For simple edits, a Markdown capable editor is sufficient: clone the repository and edit away.

If you need to view the fully-generated documentation site, you can build it with [MkDocs](https://www.mkdocs.org/). A container hosting the documentation can be started using the `invoke` commands (details in the [Development Environment Guide](https://nautobot-lunch.readthedocs.io/projects/lunch/en/latest/dev/dev_environment/#docker-development-environment)) on [http://localhost:8001](http://localhost:8001). Using this container, as your changes to the documentation are saved, they will be automatically rebuilt and any pages currently being viewed will be reloaded in your browser.

Any PRs with fixes or improvements are very welcome!

## Questions

For any questions or comments, please check the [FAQ](https://nautobot-lunch.readthedocs.io/projects/lunch/en/latest/user/faq/) first. Feel free to also swing by the [Network to Code Slack](https://networktocode.slack.com/) (channel `#nautobot`), sign up [here](http://slack.networktocode.com/) if you don't have an account.
