<div id="top"></div>

<!-- PROJECT LOGO -->

<br />
<div align="center">
  <a href="https://github.com/kiwicampus/kiwi-booster">
    <img src="https://user-images.githubusercontent.com/26184787/227988899-7192c613-c651-4f45-ae9a-8dea254ccaca.png" alt="Logo" width="200" height="200">
  </a>
<h3 align="center"><font size="8">Kiwi Booster</font></h3>

<p align="center">
    Python utils and classes for KiwiBot AI&Robotics team<br>
    <a href="https://github.com/kiwicampus/kiwi-booster/pulls">Make a Pull Request</a>
    ·
    <a href="https://github.com/kiwicampus/kiwi-booster/issues">Report Bug</a>
    ·
    <a href="https://github.com/kiwicampus/kiwi-booster/issues">Request Feature</a>
</p>

</div>

---

<!-- TABLE OF CONTENTS -->

### Table of contents

- [About The Project](#about-the-project)
- [Getting started](#getting-started)
  - [Installation](#installation)
  - [Usage](#usage)
- [Contributing](#contributing)
  - [License](#license)
  - [Contact](#contact)

---

<!-- ABOUT THE PROJECT -->

## About The Project

This library contains utility functions and classes from Python that are commonly used in the AI&Robotics team. It is divided into 5 main sections:

- **common_utils**: Some common utils that are normally used in most of the projects.
  
  - kiwi_booster.loggers
    This module contains GCP and local loggers with a predefined format.
  
  - kiwi_booster.mixed
    This module contains miscellaneous utils from multiple objectives.
  
  - kiwi_booster.requests
    This module contains utils for working with HTTP requests.

- **gcp_utils**: Utils that are related to the Google Cloud Platform.
  
  - kiwi_booster.gcp_utils.bigquery
    This module contains utils for working with BigQuery.
  
  - kiwi_booster.gcp_utils.kfp
    This module contains utils for working with Vertex (Kubeflow) Pipelines.
  
  - kiwi_booster.gcp_utils.secrets
    This module contains utils for working with Google Cloud Secrets Manager.
  
  - kiwi_booster.gcp_utils.storage
    This module contains utils for working with Google Cloud Storage.

- **ml_utils**: Utils that are related to Machine Learning.
  
  - kiwi_booster.ml_utils.benchmarks
    This module contains utils for benchmarking machine learning models.
  
  - kiwi_booster.ml_utils.prediction
    This module contains utils to handle the prediction of the semantic segmentation model.

- **decorators**: Decorators that are used to improve the codebase.

- **slack_utils**: Utils that are related to Slack.

<p align="right">(<a href="#top">back to top</a>)</p>

---

<!-- GETTING STARTED -->

## Getting started

### Installation

To install the package, simply run the following command:

```sh
pip install kiwi-booster
```

### Usage

To use the package, we recommend using relative imports for each function or class you want to import to improve readability. For example, if you want to use the `SlackBot` class, you can import it as follows:

```python
from kiwi_booster.slack_utils import SlackBot

slack_bot = SlackBot(
        SLACK_TOKEN,
        SLACK_CHANNEL_ID,
        SLACK_BOT_IMAGE_URL,
        image_alt_text="Bot description",
)
```

Or any decorator as follows:

```python
from kiwi_booster.decorators import try_catch_log

@try_catch_log
def my_function():
    # Do something
```

As well, we recommend importing them in a separate section from the rest of the imports.

<p align="right">(<a href="#top">back to top</a>)</p>

---

<!-- CONTRIBUTING -->

## Contributing

If you'd like to contribute to Kiwi Booster, please feel free to submit a pull request! We're always looking for ways to improve our codebase and make it more useful to a wider range of use cases. You can also request a new feature by submitting an issue.

### License

Kiwi Booster is licensed under the GNU license. See the LICENSE file for more information.

### Contact

Sebastian Hernández Reyes - Machine Learning Engineer - [Mail contact](mailto:juan.hernandez@kiwibot.com)

Carlos Alvarez - Machine Learning Engineer Lead - [Mail contact](mailto:carlos.alvarez@kiwibot.com)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- Template developed by the ML Team :D-->
