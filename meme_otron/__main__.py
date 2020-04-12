import logging
import sys
import os

from . import img_factory as imgf
from . import meme_db as db
from . import meme_otron

if __name__ == "__main__":
    db.load_memes()
    imgf.load_fonts()
    
    if len(sys.argv) <= 1 or sys.argv[1].lower().strip() == "help" or "-h" in sys.argv :
        print("python -h\r\n",
          "python -m meme_otron (meme_id) \"[text 1]\" \"[text 2]\" ... > file.jpg\r\n",
          "python -m meme_otron -o file.jpg (meme_id) \"[text 1]\" \"[text 2]\" ...",
          file=sys.stderr)
        sys.exit(1)
    else:
        output_f = None
        if "-o" in sys.argv:
            i = sys.argv.index("-o")
            if len(sys.argv) >= i:
                output_f = sys.argv[i+1]
                del sys.argv[i+1]
            del sys.argv[i]
        img = meme_otron.compute(*sys.argv[1:])
        if img is None:
            sys.exit(1)
        if output_f is None:
            with os.fdopen(os.dup(sys.stdout.fileno())) as output:
                img.save(output, format="jpeg")
        else:
            try:
                img.save(output_f)
                print(f"Wrote '{output_f}'")
            except OSError as e:
                print(f"Cannot write '{output_f}': {e}", file=sys.stderr)
                sys.exit(1)
            except ValueError as e:
                print(f"Cannot write '{output_f}': {e}", file=sys.stderr)
                sys.exit(1)
            
            
