[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![Taipy](https://img.shields.io/badge/taipy-4.1-red.svg)](https://docs.taipy.io/en/latest/)

# Taipy 🛠️ Tools

- [Taipy 🛠️ Tools](#taipy-️-tools)
  - [Why Taipy 🛠️ Tools?](#why-taipy-️-tools)
  - [Available Applications](#available-applications)
    - [UUID Generator](#uuid-generator)
    - [Video to GIF](#video-to-gif)
    - [QR Code Generator](#qr-code-generator)
  - [Running Taipy Tools](#running-taipy-tools)
    - [Run Locally](#run-locally)
    - [Run with Docker](#run-with-docker)

This repo is a multiple-tab app, created with Taipy.

The goal is to show how you can use Taipy in enterprise environments to create small dedicated, single-purpose applications for company.

This is how the tabs look for the three main mini-apps: A UUID generator, a Video to GIF converter, and a QR Code generator:

![GIF Screen recording of Taipy Tools](./img/taipy_tools.gif)

## Why Taipy 🛠️ Tools?

Creating small enterprise apps has several advantages:

- It allows **customization**, such as including company logos, corporate colors or any other distinctive corporate style (image, for your company's QR Codes)
- It keeps data inside the company. Sure, there are plenty of GIF generators online, but do you want your employees uploading internal screenshots to random sites?
- Your company may have some small but specific tasks that users could perform with a small Python function: You can bring it to users with Taipy.
- You can integrate your mini-apps with in-house tools or databases. (I'll be showing more apps built in that style in other projects).

Now, Taipy is mainly a data application builder. Examples of typical data apps include:

- Dashboards
- Optimization apps
- Forcasting (Machine Leanrning) apps
- AI apps...

**The apps I listed here aren't data apps**, so why use Taipy for this?

- Big companies often restrict the number of tools employees can use. Taipy’s main use case isn’t building these utility-style apps... but the fact that you can do it, and deploy them in production, is a real plus.
- Taipy is designed to speed up (and even make possible) the creation of data apps by professionals who use Python. But Python’s not just for "data people" anymore. I made these apps fast, and they can go into production with minimal effort. In corporate environments where dev processes often turn into a bottlenecked, endless black hole: this is a real, practical use case.
Using a simple app generator like Taipy can streamline those processes a lot... It can be the difference between a project that happens, and a project that doesn't.
- And well, I had lots of fun doing this 😃!

## Available Applications

These are the tools included in Taipy 🛠️ Tools, I may add more as it goes (feel free to open an issue if you think of a useful mini app!):

### UUID Generator

Uses the [uuid-utils](https://github.com/aminalaee/uuid-utils), which is faster than the `uuid` native Python library. The reason is because **it provides a unified API for all UUID types**. The app omits UUID type 8 (and type 2, but one isn't in use, and the APIs don't provide it either).

This library is also about 10 times faster than the native `uuid` library, but for an app like this one, where it generates one UUID at a time, the performance gain is unsignificant (I still encourage you to take a look at the prock if you use UUIDs).

![GIF Screen recording of the UUID generator](./img/uuid.gif)

### Video to GIF

This generates GIF images from Videos. It uses [ffmpeg-python](https://pypi.org/project/ffmpeg-python/).

An earlier version of this app used moviepy, but ffmepg is faster and is better choice for this small application. Most of the code for the video to GIF converter comes from a chatbot.

![GIF Screen recording of the video to GIF app](./img/video_to_gif.gif)

### QR Code Generator

The QR code generator uses [Segno](https://segno.readthedocs.io/en/latest/), **a library I love!**

There you have it:

![GIF Screen recording of the QR Code generator](./img/qr_codes.gif)

## Running Taipy Tools

You can run this application either **locally** or inside a **Docker container**.

⚠️ Note: The provided code is **not production-grade**: it runs on Taipy’s default Flask server.  
In the future, I may adapt this to use a more robust WSGI server (e.g. Gunicorn).

---

### Run Locally

To run locally, you can use [`uv`](https://docs.astral.sh/uv/) to create a virtual environment and install dependencies from `pyproject.toml`:

```bash
uv venv
uv pip install -r pyproject.toml
```

Then run the app:

```bash
cd src
python main.py
```

Or, from the project root, directly with uv:

```bash
uv run --directory src main.py
```

### Run with Docker

Build the Docker image:

```bash
docker build -t taipytools .
```

Run the container (mapping port 5000):

```bash
docker run -p 5000:5000 taipytools
```

You can then access the app at: http://localhost:5000

**The Dockerfile:**

- Uses Python 3.12 (Debian 12 slim) as the base.
- Installs uv.
- Copies pyproject.toml and uv.lock and installs dependencies at build time (not at runtime).
- Runs as a non-root user (appuser) for better security.
- Exposes port 5000 (default Taipy/Flask port).
- Defines a healthcheck so Docker can monitor container health.
- Runs the app with:

  ```bash
  taipy run --no-debug --no-reloader main.py -H 0.0.0.0 -P 5000
  ```
