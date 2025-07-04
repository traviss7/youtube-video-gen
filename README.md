# YouTube Shorts Search App

This repository contains a simple Python application for searching short-form YouTube videos by keyword. The GUI is built with `tkinter` and results include the video title, duration, category, and channel.

## Requirements
- Python 3
- [`google-api-python-client`](https://github.com/googleapis/google-api-python-client)

Install dependencies with:

```bash
pip install google-api-python-client
```

## Usage
1. Obtain a YouTube Data API key from the [Google Developer Console](https://console.developers.google.com/).
2. Open `app.py` and replace `YOUR_API_KEY` with your API key.
3. Run the application:

```bash
python app.py
```

Enter a search term and press the **검색** button to list short-form videos that match the query.
