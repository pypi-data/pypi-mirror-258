"""
See top level package docstring for documentation: help(sibilate)
"""

import argparse
import collections
import logging
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import time
import warnings

import humanize
import monist
import tabulate
# import whisper  # See whisper_install()
import yaml

########################################################################

myself = pathlib.Path(__file__).stem

format = '%(name)s: %(levelname)s: %(funcName)s: %(message)s'
# format = '%(name)s: %(levelname)s: %(message)s'
logging.basicConfig(format=format)
logger = logging.getLogger(myself)
logger.setLevel(logging.WARNING)

defaults = {
    'verbose': False,
    'debug': False,
    'quiet': False,
    'Log': False,
    'logfile': f"{myself}_log.txt",
    'model': 'base',
    'language': 'en',
    'ffmpeg': shutil.which('ffmpeg'),
    'root': os.path.expanduser('~/.whisper_models'),
    'srtfile': f"{myself}.srt",
    'txtfile': f"{myself}.txt",
}


def main():
    try:
        monist.config = configure()
        configure_logging()
        logger.debug(monist.config)
        ffmpeg_capability(monist.config['ffmpeg'])
        result = transcribe(
            inputfile=monist.config['inputfile'],
            language=monist.config['language'],
            model=monist.config['model'],
            root=monist.config['root'],
            verbose=monist.config['verbose'],
        )
        save_txtfile(result) if monist.config['txt'] else None
        save_srtfile(result) if monist.config['srt'] else None
        if monist.config['subtitles']:
            add_subtitles(result, inputfile=monist.config['inputfile'])
        if monist.config['burn']:
            burn_subtitles(result, inputfile=monist.config['inputfile'])
    except Exception as e:
        logger.error(f"Fatal: {e}")
        if monist.config['debug']:
            raise
        else:
            logger.warning('Run with -h for usage instructions')
            exit()
    logger.info('Completed without error')


def transcribe(
    inputfile,
    language='en',
    model='base',
    root=os.path.expanduser('~/.whisper_models'),
    verbose=False,
):
    import whisper

    logger.info(f"Target language is: {language}")
    logger.info(f"Model cache directory is: '{root}'")
    logger.info(f"Loading model '{model}' ...")
    m = whisper.load_model(model, download_root=root)
    logger.info(f"Transcribing audio using model '{model}' ...")
    start_time = time.time()
    result = m.transcribe(
        inputfile,
        verbose=verbose,
        language=language,
    )
    end_time = time.time()
    elapsed_time = end_time - start_time
    formatted_time = humanize.naturaldelta(elapsed_time)
    logger.info(f"Transcription done; time elapsed = {formatted_time}")
    return result


def save_txtfile(result):
    logger.info(f"Writing text: '{monist.config['txtfile']}' ...")
    with open(monist.config['txtfile'], 'w') as f:
        f.write(result['text'])

    
def save_srtfile(result):
    logger.info(f"Writing subtitles: '{monist.config['srtfile']}' ...")
    generate_srt(result, output=monist.config['srtfile'])


def add_subtitles(result, inputfile, mark='_subtitled'):
    srt = tempfile.NamedTemporaryFile(
        prefix=f"{myself}_", suffix='.srt', delete=False,
    )
    logger.debug(f"Subtitles temporary file: {srt.name}")
    generate_srt(result, output=srt.name)

    stem = pathlib.Path(inputfile).stem
    suffix = pathlib.Path(inputfile).suffix
    output = f"{stem}{mark}{suffix}"

    command = [
        monist.config['ffmpeg'],
        '-i', inputfile,
        '-i', srt.name,
        *'-c copy -c:s mov_text'.split(),
        output,
    ]

    try:
        logger.info(f"Running command: {command}")

        proc = subprocess.run(
            command,
            capture_output=True,
            check=True,
            text=True,
        )
        logger.debug(proc.stdout)
    except Exception as e:
        logger.debug(f"Exception: {type(e).__name__}: {e}")
        logger.error(f"Command failed")
        sys.exit(1)

    srt.delete = True
    srt.close()


def burn_subtitles(result, inputfile, mark='_burned'):
    srt = tempfile.NamedTemporaryFile(
        prefix=f"{myself}_", suffix='.srt', delete=False,
    )
    logger.debug(f"Subtitles temporary file: {srt.name}")
    generate_srt(result, output=srt.name)

    stem = pathlib.Path(inputfile).stem
    suffix = pathlib.Path(inputfile).suffix
    output = f"{stem}{mark}{suffix}"

    command = [
        monist.config['ffmpeg'],
        '-i', inputfile,
        '-vf', f"subtitles={srt.name}",
        '-codec:a',
        'copy',
        output,
    ]

    try:
        logger.info(f"Running command: {command}")

        proc = subprocess.run(
            command,
            capture_output=True,
            check=True,
            text=True,
        )
        logger.debug(proc.stdout)
    except Exception as e:
        logger.debug(f"Exception: {type(e).__name__}: {e}")
        logger.error(f"Command failed")
        sys.exit(1)

    srt.delete = True
    srt.close()


def configure():
    """Create a ChainMap: command line options, config file, defaults."""
    maps = list()
    maps.append({k: v for k, v in vars(cmdline()).items() if v is not None})
    maps.append(yaml_conf())
    maps.append(defaults)
    cm = collections.ChainMap(*maps)
    return cm


def cmdline():
    description = __doc__
    overview = list()
    overview.append('Name Parameters English-only VRAM'.split())
    overview.append('tiny 39M tiny.en ~1GB'.split())
    overview.append('base 74M base.en ~1GB'.split())
    overview.append('small 244M small.en ~2GB'.split())
    overview.append('medium 769M medium.en ~5GB'.split())
    overview.append('large 1550M N/A ~10GB'.split())
    epilog = tabulate.tabulate(overview, headers='firstrow', tablefmt='grid')
    # Support nice indenting for epilog specification:
    epilog = '\n'.join([i.strip() for i in epilog.split('\n') if i != ''])
    parser = argparse.ArgumentParser(
        description=description,
        epilog=epilog,
        # Uncomment the following line to preserve newlines in epilog
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        '-v', '--verbose',
        help='set loglevel to INFO',
        action='store_const',
        const=True,
        default=None,
    )

    parser.add_argument(
        '-d', '--debug',
        help='set loglevel to DEBUG',
        action='store_const',
        const=True,
        default=None,
    )

    parser.add_argument(
        '-q', '--quiet',
        help='set loglevel to CRITICAL',
        action='store_const',
        const=True,
        default=None,
    )

    parser.add_argument(
        '-L', '--Log',
        help=f"log to file also",
        action='store_const',
        const=True,
        default=None,
    )

    parser.add_argument(
        '--logfile',
        help=f"log file name ({defaults['logfile']})",
        metavar='F',
    )

    # yyy support this, find the function from that other script
    # parser.add_argument(
    #     '-C', '--configuration',
    #     help='report configuration values and exit',
    #     action='store_const',
    #     const=False,
    # )

    default = defaults['model']
    parser.add_argument(
        '-m', '--model',
        help=f"tiny, base, small, medium, large (default: {default})",
        metavar='M',
    )

    parser.add_argument(
        '-l', '--language',
        help=f"(default: {defaults['language']})",
        metavar='L',
    )

    parser.add_argument(
        '--ffmpeg',
        help=f"path to ffmpeg A/V encoder (default: {defaults['ffmpeg']})",
    )

    default = defaults['root']
    parser.add_argument(
        '-R', '--root',
        help=f"download root (default: {default})",
        metavar='DIR',
    )

    parser.add_argument(
        '-s', '--subtitles',
        help='add subtitles to input file',
        action='store_true',
    )

    parser.add_argument(
        '-b', '--burn',
        help='burn subtitles into input file',
        action='store_true',
    )

    parser.add_argument(
        '-S', '--srt',
        help='save transcription to srt file',
        action='store_true',
    )

    parser.add_argument(
        '--srtfile',
        help=f"srt file (default: {defaults['srtfile']})",
        metavar='F',
    )

    parser.add_argument(
        '-T', '--txt',
        help='save transcription to txt file',
        action='store_true',
    )

    parser.add_argument(
        '--txtfile',
        help=f"txt file (default: {defaults['txtfile']})",
        metavar='F',
    )

    # yyy test this
    parser.add_argument(
        '-W', '--whisper',
        help=f"install whisper package using git and pip",
        action='store_true',
    )

    parser.add_argument('inputfile', help='Input file with audio')

    args = parser.parse_args()

    # --srtfile implies --srt
    args.srt = True if args.srtfile is not None else args.srt
    # --txtfile implies --txt
    args.txt = True if args.txtfile is not None else args.txt

    return args

    
def yaml_conf(file=os.path.expanduser(f"~/.{myself}.yaml")):
    return yaml.safe_load(open(file)) if os.path.isfile(file) else dict()


def configure_logging():
    if monist.config['debug']:
        monist.config['verbose'] = True

    logger.setLevel(logging.CRITICAL) if monist.config['quiet'] else None
    logger.setLevel(logging.INFO) if monist.config['verbose'] else None
    logger.setLevel(logging.DEBUG) if monist.config['debug'] else None
    # The loudest option wins

    if not monist.config['debug']:
        warnings.filterwarnings('ignore', category=UserWarning)


    if monist.config['Log']:
        logger.addHandler(logging.FileHandler(monist.config['logfile']))


def format_time(seconds):
    """Convert seconds to SRT time format."""
    millisec = int((seconds - int(seconds)) * 1000)
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{millisec:03d}"


def generate_srt(result, output='subtitles.srt'):
    """Generate an SRT file from Whisper segments."""
    segments = result['segments']
    with open(output, 'w', encoding='utf-8') as file:
        for i, segment in enumerate(segments):
            start_time = format_time(segment['start'])
            end_time = format_time(segment['end'])
            text = segment['text'].strip()

            file.write(f"{i+1}\n{start_time} --> {end_time}\n{text}\n\n")


def ffmpeg_capability(ffmpeg):
    """Check basic ffmpeg functionality."""
    try: 
        # yyy check this
        if not ffmpeg:
            logger.info('Skipping ffmpeg capability check')
            return

        command = f"{ffmpeg} -h"
        logger.debug(f"Running: '{command}' ...")
        proc = subprocess.run(
            command.split(),
            capture_output=True,
            check=True,
            text=True,
        )
        if not re.search('codec', proc.stdout):
            raise subprocess.SubprocessError('options check failed')
    except Exception as e:
        logger.debug(f"Exception: {type(e).__name__}: {e}")
        logger.error(f"Failed ffmpeg capability check (see --ffmpeg option)")
        # yyy notes about how to install ffmpeg
        sys.exit(1)


def whisper_install():
    """Install whisper package. Not sure why whisper is not on pypi."""
    try:
        import whisper
        return
    except Exception as e:
        logger.debug(f"Exception: {type(e).__name__}: {e}")
        logger.info('Whisper not installed; installing, as requested...')

    # If we are still here, that means 'import whisper' failed
    try:
        command = 'pip install git+https://github.com/openai/whisper.git'
        logger.info(f"Running command: '{command}' ...")
        proc = subprocess.run(
            command.split(),
            capture_output=True,
            check=True,
            text=True,
        )
        # yyy
        #if not re.search('codec', proc.stdout):
        #    raise subprocess.SubprocessError('options check failed')
    except Exception as e:
        logger.debug(f"pip stdout =\n{proc.stdout}")
        logger.debug(f"pip stderr =\n{proc.stderr}")
        logger.debug(f"Exception: {type(e).__name__}: {e}")
        logger.error(f"Failed to install whisper")
        logger.error(f"Are git and pip available?")
        sys.exit(1)


if __name__ == '__main__':
    main()


# Extract Audio from Video
# $1 = mp4 file
# $2 = wav file
# ffmpeg -i "$1" -ab 160k -ac 2 -ar 44100 -vn "$2"
