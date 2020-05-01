# Meme-Otron guide

* [Commands](#commands)
  * [Simple use](#simple-use)
  * [Advanced use](#advanced-use)
  * [Discord features](#discord-features)
  * [CLI features](#cli-features)
* [List of templates](#list-of-templates)
  * [Standard Templates](#standard-templates)
  * [Reactions (no text)](#reactions-no-text)
* [Examples](#examples)
  * [Example 1: Simple template](#example-1-simple-template)
  * [Example 2: Use of empty texts](#example-2-use-of-empty-texts)
  * [Example 3: Text + Template](#example-3-text--template)
  * [Example 4: Complex composition](#example-4-complex-composition)


## Commands

### Simple use
<sub><sup>[↑ back to top](#meme-otron-guide)</sup></sub>

You can generate memes by using the following arguments:

```
[meme id] "text1" "text2" ...
```

Depending of the number of `"text"` arguments, several behavior occurs:
* **None**: you get the template that gives you the locations of texts. (see below)
* **Less than the template's**: the remaining texts are blank on the output
* **More than the template's**: the extra arguments are ignored

> Notes
> * You don't have to use all texts shown on the templates
> * You can use an empty text argument ( `""` ) to skip a text and keep it blank

See [Examples](#examples) to get an idea of how to use it.

### Advanced use
<sub><sup>[↑ back to top](#meme-otron-guide)</sup></sub>

Since version 1.3, Meme-Otron allows you to "pipe" parts in order to compose more advanced memes. The syntax is as follows:

```
[part1] - [part2] - ...
```

Each part can be one of the following:

* A template: as described in [Simple use](#simple-use)
* Texts: ```text "text 1" "text 2" ...```
  * Black Arial texts on white background
  * Each text is it's own paragraph
* Images: ```image <URL>```
  * Takes an image from input or an URL (optional)
  * Input depends on the system:
    * the Discord bot takes the attachment
    * the CLI takes stdin or `--input` argument.

> Notes
> * Input of `image` is always the same, don't expect multiple instances of `image` to get different results if you don't indicate an URL

See [Examples](#examples) to get an idea of how to use it.

### Discord features
<sub><sup>[↑ back to top](#meme-otron-guide)</sup></sub>

Tag the bot and use the above syntax to get started. In addition, you can use the following commands:

* Use `help` to get a simple help message
* Use `list` to get a list of all meme ids
* Use `delete` to delete the last message sent by the bot (directed to you)

To get the template info, just send the meme id without texts.

> Tip : You can use `\\n` in your texts to add a line break 

Enjoy the full experience of this bot by using direct messages to keep your server free of spam.

### CLI features
<sub><sup>[↑ back to top](#meme-otron-guide)</sup></sub>

In this project directory, you can simply call:
```
python -m meme_otron [meme id] "text1" "text2" ... > output.jpg
```
Without pipe redirection with `-o [output]`:
```
python -m meme_otron -o output.png [meme id] "text1" "text2" ...
```

You can even pipe input images like this:
```
python -m meme_otron [arguments] < input.jpg > output.jpg
```

Available arguments:
* `--help` / `-h`
  * Show a simple guide
* `--output [file]` / `-o [file]`
  * Output file, you are free to choose the format
* `--input [file]` / `-i [file]`
  * Input file used for `image`
* `-nw` / `--no-watermark`
  * Removes the watermark
* `-d` / `--debug`
  * Add more info to output like a box show the texts boundaries
* `-v` / `--verbose`
  * Add more logging


## List of templates
<sub><sup>[↑ back to top](#meme-otron-guide)</sup></sub>

You can find here the full list of templates.
Each one has extra info and an image showing how texts are placed.
Click on an image to enlarge it.

### Standard Templates
<sub><sup>[↑ back to top](#meme-otron-guide)</sup></sub>

<!--LIST1-START-->

<!--LIST1-END-->

### Reactions (no text)
<sub><sup>[↑ back to top](#meme-otron-guide)</sup></sub>

<!--LIST2-START-->

<!--LIST2-END-->


## Examples

### Example 1: Simple template
<sub><sup>[↑ back to top](#meme-otron-guide)</sup></sub>

<!--EXAMPLE1-START-->

<!--EXAMPLE1-END-->

### Example 2: Use of empty texts
<sub><sup>[↑ back to top](#meme-otron-guide)</sup></sub>

<!--EXAMPLE2-START-->

<!--EXAMPLE2-END-->

### Example 3: Text + Template
<sub><sup>[↑ back to top](#meme-otron-guide)</sup></sub>

<!--EXAMPLE3-START-->

<!--EXAMPLE3-END-->


### Example 4: Complex composition
<sub><sup>[↑ back to top](#meme-otron-guide)</sup></sub>

<!--EXAMPLE4-START-->

<!--EXAMPLE4-END-->