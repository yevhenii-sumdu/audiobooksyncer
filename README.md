# audiobooksyncer

An application to synchronize an audiobook with text and its translation.

The purpose of this app is to simplify the experience of listening to audiobooks in a foreign language, so you can quickly look up what's being said and check the translation if needed.

Under the hood, the following packages are used:
- [aeneas](https://github.com/readbeyond/aeneas) - to sync text with audio
- [bertalign](https://github.com/bfsujason/bertalign) - to sync text with translation
- [whisper](https://github.com/openai/whisper) - to find where the audio files begin in text.

# Getting Started

First clone the repo using:

```bash
git clone https://github.com/yevhenii-sumdu/audiobooksyncer
```

This app can only be used on Linux and you need a GPU with CUDA support (though you can run it on CPU, but it will be slower). Tested with Python 3.10.

You need the following packages installed:
- gcc/clang
- libespeak-dev
- ffmpeg

On Debian-based systems this can be done using:

```bash
apt install gcc libespeak-dev ffmpeg
```

These are mostly needed by aeneas, for troubleshooting check it's [dependencies](https://github.com/readbeyond/aeneas/blob/master/install_dependencies.sh).

Then create a python virtual environment:

```bash
python3 -m venv .venv
. .venv/bin/activate
```

Then install python dependencies using pinned versions:

```bash
pip install -r requirements.txt
```

You can also install the project itself:

```bash
pip install .
# or
pip install -e .
```

This will add `audiobooksyncer` script to your environment.

# Usage

If you install the app, you can use `audiobooksyncer` script. Otherwise, you can run the package directly with `python -m audiobooksyncer`.

As an input provide book's text, translation (plain text files) and a directory which contains audiobook's files.

```bash
python -m audiobooksyncer book_de.txt book_en.txt audiobook/
```

The shorter the audio files, the better the result, around an hour is fine. You can set `--aeneas_dtw_margin` for longer files (default is 120 seconds).

Text to audio sync requires quite a bit of RAM. The audio files are processed in parallel, with the number of processes equal to CPU count by default (can be set with `--aeneas_processes`). RAM is mostly used up in the second part of processing of each file, so if you have several big files with the same duration, this peak might add up.

## Results

Results will be stored in a directory created in CWD, the directory's name is unique for different inputs, each step's result will be stored in a json file and reused on consecutive runs.

The sync map file contains json array with each element containing part of the text, part of the translation and time interval in ms.

```json
[
  {
    "src": "Der Hobbit",
    "tgt": "The Hobbit",
    "begin": 0,
    "end": 1880
  },
  ...
]
```

This can be turned into subtitles files with [srt](https://pypi.org/project/srt/).

Or you can use [AudiobookSyncerReader](https://github.com/atlantis-11/AudiobookSyncerReader) app for Android.

# Documentation Style Guide  

This project follows the **reStructuredText (reST) format** for documentation to ensure consistency and readability across all modules. When writing docstrings, please adhere to the **PEP 257** guidelines and structure them clearly.  

## Example

**Function & Method Docstrings**  
- Include a brief description, parameters, return values, and any raised exceptions.  
- Use the following format:  

```python
def example_function(param1: int, param2: str) -> bool:
    """
    Brief summary of the function.

    :param param1: Description of the first parameter.
    :type param1: int
    :param param2: Description of the second parameter.
    :type param2: str
    :return: Description of what the function returns.
    :rtype: bool
    :raises ValueError: Explanation of when this exception is raised.
    """
```
