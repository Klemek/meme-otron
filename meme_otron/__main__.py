import sys
import os
import logging

from . import img_factory
from . import meme_db
from . import meme_otron
from . import utils
from . import VERSION

if __name__ == "__main__":
    wmark = not utils.read_argument(sys.argv, "-nw", "--no-watermark", delete=True)
    debug = utils.read_argument(sys.argv, "-d", "--debug", delete=True)
    verbose = utils.read_argument(sys.argv, "-v", "--verbose", delete=True)
    output_file = utils.read_argument(sys.argv, "-o", "--output", valued=True, delete=True)
    input_file = utils.read_argument(sys.argv, "-i", "--input", valued=True, delete=True)

    if verbose and debug:
        logging.basicConfig(format="[%(asctime)s][%(levelname)s][%(module)s] %(message)s", level=logging.DEBUG)
    elif verbose:
        logging.basicConfig(format="[%(asctime)s][%(levelname)s][%(module)s] %(message)s", level=logging.INFO)
    else:
        logging.basicConfig(format="%(message)s", level=logging.WARNING)

    meme_db.load_memes()
    img_factory.load_fonts()

    if len(sys.argv) <= 1 or utils.read_argument(sys.argv, "help", "--help", "-h"):
        print(f"Meme-Otron v{VERSION}"
              "python -m meme_otron -h\n"
              "python -m meme_otron (meme_id) \"[text 1]\" \"[text 2]\" ... > file.jpg\n"
              "python -m meme_otron -o file.jpg (meme_id) \"[text 1]\" \"[text 2]\" ...",
              file=sys.stderr)
        sys.exit(1)
    else:
        input_data = None
        if input_file is not None:
            try:
                with open(input_file, "rb") as f:
                    input_data = f.read()
            except IOError as e:
                print(f"Cannot read '{input_file}': {e}", file=sys.stderr)
                sys.exit(1)
        elif not sys.stdin.isatty():
            input_data = utils.read_stream(sys.stdin.buffer)

        img, errors = meme_otron.compute(*sys.argv[1:], input_data=input_data, wmark=wmark, debug=debug)
        for err in errors:
            print(err, file=sys.stderr)
        if img is None:
            sys.exit(1)
        if output_file is None:
            with os.fdopen(os.dup(sys.stdout.fileno())) as output:
                img.save(output, format="jpeg")
        else:
            try:
                img.save(output_file)
                print(f"Wrote '{output_file}'")
            except OSError as e:
                print(f"Cannot write '{output_file}': {e}", file=sys.stderr)
                sys.exit(1)
            except ValueError as e:
                print(f"Cannot write '{output_file}': {e}", file=sys.stderr)
                sys.exit(1)
