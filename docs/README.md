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
||||
|:---:|:---:|:---:|
|**aliens**<br><a href='https://knowyourmeme.com/memes/ancient-aliens' target='_blank'>more info</a>|**alive**<br>alt: no_brain<br><a href='https://knowyourmeme.com/memes/oh-fuck-i-forgot-to-give-you-a-brain' target='_blank'>more info</a>|**argument**<br>alt: wrestlers<br><a href='https://knowyourmeme.com/memes/american-chopper-argument' target='_blank'>more info</a>|
|<a href='./templates/aliens.jpg' target='_blank'><img alt='enlarge' src='./preview/aliens.jpg'/></a>|<a href='./templates/alive.jpg' target='_blank'><img alt='enlarge' src='./preview/alive.jpg'/></a>|<a href='./templates/argument.jpg' target='_blank'><img alt='enlarge' src='./preview/argument.jpg'/></a>|
|**bender**<br>alt: hookers, blackjack<br><a href='https://knowyourmeme.com/memes/im-going-to-build-my-own-theme-park-with-blackjack-and-hookers' target='_blank'>more info</a>|**born_cool**<br><a href='https://knowyourmeme.com/memes/nobody-is-born-cool' target='_blank'>more info</a>|**brain3**|
|<a href='./templates/bender.jpg' target='_blank'><img alt='enlarge' src='./preview/bender.jpg'/></a>|<a href='./templates/born_cool.jpg' target='_blank'><img alt='enlarge' src='./preview/born_cool.jpg'/></a>|<a href='./templates/brain3.jpg' target='_blank'><img alt='enlarge' src='./preview/brain3.jpg'/></a>|
|**brain4**<br>alt: brains<br><a href='https://knowyourmeme.com/memes/galaxy-brain' target='_blank'>more info</a>|**brain5**|**buff**<br>alt: tom, jerry<br><a href='https://knowyourmeme.com/memes/buff-tom' target='_blank'>more info</a>|
|<a href='./templates/brain4.jpg' target='_blank'><img alt='enlarge' src='./preview/brain4.jpg'/></a>|<a href='./templates/brain5.jpg' target='_blank'><img alt='enlarge' src='./preview/brain5.jpg'/></a>|<a href='./templates/buff.jpg' target='_blank'><img alt='enlarge' src='./preview/buff.jpg'/></a>|
|**burn**<br>alt: paper<br><a href='https://knowyourmeme.com/photos/1379947-spongebob-squarepants' target='_blank'>more info</a>|**button**<br>alt: nut<br><a href='https://knowyourmeme.com/memes/nut-button' target='_blank'>more info</a>|**bye_mom**<br>alt: google<br><a href='https://knowyourmeme.com/memes/ok-bye-mom' target='_blank'>more info</a>|
|<a href='./templates/burn.jpg' target='_blank'><img alt='enlarge' src='./preview/burn.jpg'/></a>|<a href='./templates/button.jpg' target='_blank'><img alt='enlarge' src='./preview/button.jpg'/></a>|<a href='./templates/bye_mom.jpg' target='_blank'><img alt='enlarge' src='./preview/bye_mom.jpg'/></a>|
|**clock**<br><a href='https://knowyourmeme.com/memes/squidwards-clock-closet' target='_blank'>more info</a>|**culture**<br>alt: anime<br><a href='https://knowyourmeme.com/memes/ah-i-see-youre-a-man-of-culture-as-well' target='_blank'>more info</a>|**disappointed**<br><a href='https://knowyourmeme.com/memes/disappointed-black-guy' target='_blank'>more info</a>|
|<a href='./templates/clock.jpg' target='_blank'><img alt='enlarge' src='./preview/clock.jpg'/></a>|<a href='./templates/culture.jpg' target='_blank'><img alt='enlarge' src='./preview/culture.jpg'/></a>|<a href='./templates/disappointed.jpg' target='_blank'><img alt='enlarge' src='./preview/disappointed.jpg'/></a>|
|**distracted**<br>alt: boyfried, cheating, girlfriend<br><a href='https://knowyourmeme.com/memes/distracted-boyfriend' target='_blank'>more info</a>|**dont_look**<br>alt: ricky, mom, influenced<br><a href='https://knowyourmeme.com/memes/dont-look-at-them-ricky' target='_blank'>more info</a>|**drake**<br><a href='https://knowyourmeme.com/memes/drakeposting' target='_blank'>more info</a>|
|<a href='./templates/distracted.jpg' target='_blank'><img alt='enlarge' src='./preview/distracted.jpg'/></a>|<a href='./templates/dont_look.jpg' target='_blank'><img alt='enlarge' src='./preview/dont_look.jpg'/></a>|<a href='./templates/drake.jpg' target='_blank'><img alt='enlarge' src='./preview/drake.jpg'/></a>|
|**drift**<br>alt: exit<br><a href='https://knowyourmeme.com/memes/left-exit-12-off-ramp' target='_blank'>more info</a>|**everywhere**<br>alt: buzz, woody<br><a href='https://knowyourmeme.com/memes/x-x-everywhere' target='_blank'>more info</a>|**everywhere2**<br>alt: angry, diapers<br><a href='https://knowyourmeme.com/memes/how-many-diapers-could-he-possibly-use' target='_blank'>more info</a>|
|<a href='./templates/drift.jpg' target='_blank'><img alt='enlarge' src='./preview/drift.jpg'/></a>|<a href='./templates/everywhere.jpg' target='_blank'><img alt='enlarge' src='./preview/everywhere.jpg'/></a>|<a href='./templates/everywhere2.jpg' target='_blank'><img alt='enlarge' src='./preview/everywhere2.jpg'/></a>|
|**fight**<br>alt: vaping<br><a href='https://knowyourmeme.com/memes/dabbing-dude' target='_blank'>more info</a>|**fine**<br>alt: fire, dog<br><a href='https://knowyourmeme.com/memes/this-is-fine' target='_blank'>more info</a>|**flex_tape**<br>alt: flex, tape<br><a href='https://knowyourmeme.com/memes/flex-tape' target='_blank'>more info</a>|
|<a href='./templates/fight.jpg' target='_blank'><img alt='enlarge' src='./preview/fight.jpg'/></a>|<a href='./templates/fine.jpg' target='_blank'><img alt='enlarge' src='./preview/fine.jpg'/></a>|<a href='./templates/flex_tape.jpg' target='_blank'><img alt='enlarge' src='./preview/flex_tape.jpg'/></a>|
|**gate**<br><a href='https://knowyourmeme.com/memes/open-the-gate' target='_blank'>more info</a>|**girl_cat**<br><a href='https://knowyourmeme.com/memes/woman-yelling-at-a-cat' target='_blank'>more info</a>|**grandma**<br><a href='https://knowyourmeme.com/memes/grandma-finds-the-internet' target='_blank'>more info</a>|
|<a href='./templates/gate.jpg' target='_blank'><img alt='enlarge' src='./preview/gate.jpg'/></a>|<a href='./templates/girl_cat.jpg' target='_blank'><img alt='enlarge' src='./preview/girl_cat.jpg'/></a>|<a href='./templates/grandma.jpg' target='_blank'><img alt='enlarge' src='./preview/grandma.jpg'/></a>|
|**gru**<br>alt: plan<br><a href='https://knowyourmeme.com/memes/grus-plan' target='_blank'>more info</a>|**guys**<br>alt: explain, paid<br><a href='https://knowyourmeme.com/memes/you-guys-are-getting-paid' target='_blank'>more info</a>|**handshake**<br><a href='https://knowyourmeme.com/memes/epic-handshake' target='_blank'>more info</a>|
|<a href='./templates/gru.jpg' target='_blank'><img alt='enlarge' src='./preview/gru.jpg'/></a>|<a href='./templates/guys.jpg' target='_blank'><img alt='enlarge' src='./preview/guys.jpg'/></a>|<a href='./templates/handshake.jpg' target='_blank'><img alt='enlarge' src='./preview/handshake.jpg'/></a>|
|**handshake2**<br>alt: scott<br><a href='https://knowyourmeme.com/memes/young-michael-scott-shaking-ed-trucks-hand' target='_blank'>more info</a>|**idea**<br>alt: gentlemen<br><a href='https://knowyourmeme.com/memes/all-right-gentlemen' target='_blank'>more info</a>|**lion**<br>alt: shadowy, king, light<br><a href='https://knowyourmeme.com/memes/simba-everything-the-light-touches-is' target='_blank'>more info</a>|
|<a href='./templates/handshake2.jpg' target='_blank'><img alt='enlarge' src='./preview/handshake2.jpg'/></a>|<a href='./templates/idea.jpg' target='_blank'><img alt='enlarge' src='./preview/idea.jpg'/></a>|<a href='./templates/lion.jpg' target='_blank'><img alt='enlarge' src='./preview/lion.jpg'/></a>|
|**meeting**<br>alt: boardroom, suggestion<br><a href='https://knowyourmeme.com/memes/boardroom-suggestion' target='_blank'>more info</a>|**mini**<br>alt: joker<br><a href='https://knowyourmeme.com/memes/mini-joker' target='_blank'>more info</a>|**nobody_cares**<br>alt: nobody, jurassic, park, jurassic_park<br><a href='https://knowyourmeme.com/memes/see-nobody-cares' target='_blank'>more info</a>|
|<a href='./templates/meeting.jpg' target='_blank'><img alt='enlarge' src='./preview/meeting.jpg'/></a>|<a href='./templates/mini.jpg' target='_blank'><img alt='enlarge' src='./preview/mini.jpg'/></a>|<a href='./templates/nobody_cares.jpg' target='_blank'><img alt='enlarge' src='./preview/nobody_cares.jpg'/></a>|
|**nope**<br><a href='https://knowyourmeme.com/memes/disappointed-black-guy' target='_blank'>more info</a>|**overconfident**<br>alt: alcohol, depressed<br><a href='https://knowyourmeme.com/memes/overconfident-alcoholic' target='_blank'>more info</a>|**patrick**<br>alt: wallet, id<br><a href='https://knowyourmeme.com/memes/patrick-stars-wallet' target='_blank'>more info</a>|
|<a href='./templates/nope.jpg' target='_blank'><img alt='enlarge' src='./preview/nope.jpg'/></a>|<a href='./templates/overconfident.jpg' target='_blank'><img alt='enlarge' src='./preview/overconfident.jpg'/></a>|<a href='./templates/patrick.jpg' target='_blank'><img alt='enlarge' src='./preview/patrick.jpg'/></a>|
|**pigeon**<br>alt: butterfly<br><a href='https://knowyourmeme.com/memes/is-this-a-pigeon' target='_blank'>more info</a>|**pills**<br>alt: swallow<br><a href='https://knowyourmeme.com/memes/hard-to-swallow-pills' target='_blank'>more info</a>|**pleasure3**<br>alt: satisfied3|
|<a href='./templates/pigeon.jpg' target='_blank'><img alt='enlarge' src='./preview/pigeon.jpg'/></a>|<a href='./templates/pills.jpg' target='_blank'><img alt='enlarge' src='./preview/pills.jpg'/></a>|<a href='./templates/pleasure3.jpg' target='_blank'><img alt='enlarge' src='./preview/pleasure3.jpg'/></a>|
|**pleasure4**<br>alt: pleasure, satisfied, satisfied4<br><a href='https://knowyourmeme.com/memes/vince-mcmahon-reaction' target='_blank'>more info</a>|**salt_bae**<br>alt: salt<br><a href='https://knowyourmeme.com/memes/salt-bae' target='_blank'>more info</a>|**scary**<br>alt: spongebob, fearless<br><a href='https://knowyourmeme.com/memes/spongebob-sees-flying-dutchman' target='_blank'>more info</a>|
|<a href='./templates/pleasure4.jpg' target='_blank'><img alt='enlarge' src='./preview/pleasure4.jpg'/></a>|<a href='./templates/salt_bae.jpg' target='_blank'><img alt='enlarge' src='./preview/salt_bae.jpg'/></a>|<a href='./templates/scary.jpg' target='_blank'><img alt='enlarge' src='./preview/scary.jpg'/></a>|
|**seagull2**<br>alt: seagull, screaming<br><a href='https://knowyourmeme.com/memes/inhaling-seagull' target='_blank'>more info</a>|**seagull4**|**see_that_guy**<br><a href='https://knowyourmeme.com/memes/hey-man-you-see-that-guy-over-there' target='_blank'>more info</a>|
|<a href='./templates/seagull2.jpg' target='_blank'><img alt='enlarge' src='./preview/seagull2.jpg'/></a>|<a href='./templates/seagull4.jpg' target='_blank'><img alt='enlarge' src='./preview/seagull4.jpg'/></a>|<a href='./templates/see_that_guy.jpg' target='_blank'><img alt='enlarge' src='./preview/see_that_guy.jpg'/></a>|
|**sleeping**<br>alt: brain<br><a href='https://knowyourmeme.com/memes/are-you-going-to-sleep' target='_blank'>more info</a>|**spiderman**<br>alt: same<br><a href='https://knowyourmeme.com/memes/spider-man-pointing-at-spider-man' target='_blank'>more info</a>|**struggle**<br>alt: choice, hero<br><a href='https://knowyourmeme.com/memes/daily-struggle' target='_blank'>more info</a>|
|<a href='./templates/sleeping.jpg' target='_blank'><img alt='enlarge' src='./preview/sleeping.jpg'/></a>|<a href='./templates/spiderman.jpg' target='_blank'><img alt='enlarge' src='./preview/spiderman.jpg'/></a>|<a href='./templates/struggle.jpg' target='_blank'><img alt='enlarge' src='./preview/struggle.jpg'/></a>|
|**t_pose**<br>alt: dominance, monika<br><a href='https://knowyourmeme.com/memes/monika-t-posing-over-sans' target='_blank'>more info</a>|**tom_cousins**<br>alt: cousins, backup, goons<br><a href='https://knowyourmeme.com/memes/tom-and-jerry-hired-goons' target='_blank'>more info</a>|**tough2**<br>alt: tough, fight<br><a href='https://knowyourmeme.com/memes/increasingly-buff-spongebob' target='_blank'>more info</a>|
|<a href='./templates/t_pose.jpg' target='_blank'><img alt='enlarge' src='./preview/t_pose.jpg'/></a>|<a href='./templates/tom_cousins.jpg' target='_blank'><img alt='enlarge' src='./preview/tom_cousins.jpg'/></a>|<a href='./templates/tough2.jpg' target='_blank'><img alt='enlarge' src='./preview/tough2.jpg'/></a>|
|**tough2bis**<br>alt: soft|**tough3**|**trump**<br>alt: law<br><a href='https://knowyourmeme.com/memes/trumps-first-order-of-business' target='_blank'>more info</a>|
|<a href='./templates/tough2bis.jpg' target='_blank'><img alt='enlarge' src='./preview/tough2bis.jpg'/></a>|<a href='./templates/tough3.jpg' target='_blank'><img alt='enlarge' src='./preview/tough3.jpg'/></a>|<a href='./templates/trump.jpg' target='_blank'><img alt='enlarge' src='./preview/trump.jpg'/></a>|
|**trust_nobody**<br>alt: yourself, gun<br><a href='https://knowyourmeme.com/memes/trust-nobody-not-even-yourself' target='_blank'>more info</a>|**truth**<br>alt: scroll<br><a href='https://knowyourmeme.com/memes/the-scroll-of-truth' target='_blank'>more info</a>|**winnie2**<br>alt: winnie<br><a href='https://knowyourmeme.com/memes/tuxedo-winnie-the-pooh' target='_blank'>more info</a>|
|<a href='./templates/trust_nobody.jpg' target='_blank'><img alt='enlarge' src='./preview/trust_nobody.jpg'/></a>|<a href='./templates/truth.jpg' target='_blank'><img alt='enlarge' src='./preview/truth.jpg'/></a>|<a href='./templates/winnie2.jpg' target='_blank'><img alt='enlarge' src='./preview/winnie2.jpg'/></a>|||
<!--LIST1-END-->

### Reactions (no text)
<sub><sup>[↑ back to top](#meme-otron-guide)</sup></sub>

<!--LIST2-START-->

<!--LIST2-END-->


## Examples

### Example 1: Simple template
<sub><sup>[↑ back to top](#meme-otron-guide)</sup></sub>

<!--EXAMPLE1-START-->
> 

```
brain3 
"Making memes using an image editor" 
"Making memes using a Python script" 
"Making memes using a Discord bot"
```

![](example1.jpg)
<!--EXAMPLE1-END-->

### Example 2: Use of empty texts
<sub><sup>[↑ back to top](#meme-otron-guide)</sup></sub>

<!--EXAMPLE2-START-->
> The 5th text is not set and the 3rd is explicitly set to empty

```
see_that_guy 
"See that guy over there?" 
"He uses an image editor to make memes" 
"" 
"meme-otron dev"
```

![](example2.jpg)
<!--EXAMPLE2-END-->

### Example 3: Text + template
<sub><sup>[↑ back to top](#meme-otron-guide)</sup></sub>

<!--EXAMPLE3-START-->
> Note how texts make paragraphs

```
text 
"*Meme has a 'made with meme-otron' watermark*" 
"reddit: ..." 
"9gag: ..." 
"meme-otron dev:" 
- 
culture 
"meme otron"
```

![](example3.jpg)
<!--EXAMPLE3-END-->


### Example 4: Complex composition
<sub><sup>[↑ back to top](#meme-otron-guide)</sup></sub>

<!--EXAMPLE4-START-->

<!--EXAMPLE4-END-->