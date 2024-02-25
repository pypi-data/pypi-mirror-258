========
sibilate
========


.. image:: https://img.shields.io/pypi/v/sibilate.svg
        :target: https://pypi.python.org/pypi/sibilate

.. image:: https://img.shields.io/travis/datagazing/sibilate.svg
        :target: https://travis-ci.com/datagazing/sibilate

.. image:: https://readthedocs.org/projects/sibilate/badge/?version=latest
        :target: https://sibilate.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

Subtitle generator using whisper LLM

.. code-block:: console

  usage: sibilate [-h] [-v] [-d] [-q] [-L] [--logfile F] [-m M] [-l L]
                  [--ffmpeg FFMPEG] [-R DIR] [-s] [-b] [-S] [--srtfile F] [-T]
                  [--txtfile F] [-W]
                  inputfile
  
  Subtitle generator using whisper LLM
  
  positional arguments:
    inputfile           Input file with audio
  
  options:
    -h, --help          show this help message and exit
    -v, --verbose       set loglevel to INFO
    -d, --debug         set loglevel to DEBUG
    -q, --quiet         set loglevel to CRITICAL
    -L, --Log           log to file also
    --logfile F         log file name (sibilate_log.txt)
    -m M, --model M     tiny, base, small, medium, large (default: base)
    -l L, --language L  language (default: en)
    --ffmpeg FFMPEG     path to ffmpeg A/V encoder
    -R DIR, --root DIR  download root (default: ~/.whisper_models)
    -s, --subtitles     add subtitles to input file
    -b, --burn          burn subtitles into input file
    -S, --srt           save transcription to srt file
    --srtfile F         srt file (default: sibilate.srt)
    -T, --txt           save transcription to txt file
    --txtfile F         txt file (default: sibilate.txt)
    -W, --whisper       install whisper package using git and pip
  
  +--------+--------------+----------------+--------+
  | Name   | Parameters   | English-only   | VRAM   |
  +========+==============+================+========+
  | tiny   | 39M          | tiny.en        | ~1GB   |
  +--------+--------------+----------------+--------+
  | base   | 74M          | base.en        | ~1GB   |
  +--------+--------------+----------------+--------+
  | small  | 244M         | small.en       | ~2GB   |
  +--------+--------------+----------------+--------+
  | medium | 769M         | medium.en      | ~5GB   |
  +--------+--------------+----------------+--------+
  | large  | 1550M        | N/A            | ~10GB  |
  +--------+--------------+----------------+--------+



Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
