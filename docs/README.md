* [Commands](#commands)
* [Discord features](#discord-features)
* [CLI features](#cli-features)
* [List of templates](#list-of-templates)
* [List of reactions](#list-of-templates)


## Commands

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

## Discord features

Tag the bot and use the above syntax to get started. In addition, you can use the following commands:

* Use `help` to get a simple help message
* Use `list` to get a list of all meme ids
* Use `delete` to delete the last message sent by the bot (directed to you)

To get the template info, just send the meme id without texts.

> Tip : You can use `\\n` in your texts to add a line break 

Enjoy the full experience of this bot by using direct messages to keep your server free of spam.

## CLI features

In this project directory, you can simply call:
```
python -m meme_otron [meme id] "text1" "text2" ... > output.jpg
```
Without pipe redirection with `-o [output]`:
```
python -m meme_otron -o output.png [meme id] "text1" "text2" ...
```

> Note: with `-o`, you are free to choose the output format

## List of templates

You can find here the full list of templates.
Each one has extra info and an image showing how texts are placed.
Click on an image to enlarge it.


<!--START1-->

<!--END1-->

## List of reactions

You can find here the full list of reactions (templates without texts).
Each one has extra info.
Click on an image to enlarge it.

<!--START2-->

<!--END2-->
