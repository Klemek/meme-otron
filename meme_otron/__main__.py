import sys
import os

from . import img_factory
from . import meme_db
from . import meme_otron
from . import utils
from . import VERSION

if __name__ == "__main__":
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
        output_file = utils.read_argument(sys.argv, "-o", "--output", valued=True, delete=True)
        img, errors = meme_otron.compute(*sys.argv[1:])
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
