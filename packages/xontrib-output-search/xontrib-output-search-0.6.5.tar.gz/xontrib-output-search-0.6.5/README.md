<p align="center">
Get identifiers, names, paths, URLs and words from the previous command output and use them for the next command in <a href="https://xon.sh">xonsh</a>.
<br><br>
<img src="https://repository-images.githubusercontent.com/257978984/a0eaac80-0424-11eb-85ad-29809d2f792d">
</p>



## Features

💡 **Universal**. Forget about searching autocomplete plugins for every app you use. Just get the identifiers from the previous output.

⏳ **Save time**. Forget about using mouse, touchpad or trackball to get any words from screen to the next command.

🔒 **Secure**. It works the same way as xonsh shell and the security level is the same.


## Install

```shell script
xpip install -U xontrib-output-search
```

## Before usage

There are three ways to use output search:
* Recommended. Use [tmux](https://en.wikipedia.org/wiki/Tmux) to run xonsh and use output search. See instructions below.
* Not recommended. Set [`$XONSH_CAPTURE_ALWAYS=True`](https://xon.sh/envvars.html#xonsh-capture-always) and be ready some tools will freeze because of capturing e.g. `git config --help`. Details: after [xonsh release 0.10.0](https://github.com/xonsh/xonsh/releases/tag/0.10.0) ([4283](https://github.com/xonsh/xonsh/pull/4283)) you should set [`$XONSH_CAPTURE_ALWAYS=True`](https://xon.sh/envvars.html#xonsh-capture-always) in your `~/.xonshrc` to make output capturable. This approach has issues and we decided that the best solution for output search is to use the terminal window managers and we support [tmux](https://en.wikipedia.org/wiki/Tmux). In this case the output will be captured from the screen.
* Alternative. You can [add support](https://github.com/anki-code/xontrib-output-search/blob/85a5eea39bb33377e236e0ba8e22b5e055f6bce5/xontrib/output_search.py#L81) any terminal emulator or terminal window manager like tmux that can capture the content of the terminal. PR is welcome!

## Usage

The recommended way as described above:

```xsh
zsh
alias tx="tmux new-session xonsh ';' set -g status off"  # add alias to run xonsh in tmux without bottom status bar
tx  # run xonsh in tmux
xontrib load output_search  # add this to ~/.xonshrc
```

After loading you can select tokens from latest not empty output:
* Windows/Linux: Press <kbd>Alt</kbd> + <kbd>f</kbd> hotkeys after getting the output of the previous command.
* Mac: Press <kbd>Control</kbd> + <kbd>f</kbd> hotkeys after getting the output of the previous command.
* Any OS: Type `f__` or `f__<beginning of the word you want>` and press <kbd>Tab</kbd>.

If you use this key combination for another function and your muscle memory is strong just change 
the [key combination](https://python-prompt-toolkit.readthedocs.io/en/master/pages/advanced_topics/key_bindings.html) before 
loading the xontrib:
```python
# Alt+i combination. Meaning for prompt-toolkit: @bindings.add('escape', 'i')
$XONTRIB_OUTPUT_SEARCH_KEY='i'
xontrib load output_search
```
```python
# This approach is recommended for Mac users because `c-<key>` is represented 
# the Control key that has less intersections with other Mac hotkeys. 
#
# Control+g combination. Meaning for prompt-toolkit: @bindings.add('c-g')
$XONTRIB_OUTPUT_SEARCH_KEY_BINDING='c-g'
xontrib load output_search
```
```python
# Right+Left combination. Meaning for prompt-toolkit: @bindings.add('right', 'left')
$XONTRIB_OUTPUT_SEARCH_KEY_META='right'
$XONTRIB_OUTPUT_SEARCH_KEY='left'  # the text placeholder will be `left__`
xontrib load output_search
```

In [tmux](https://en.wikipedia.org/wiki/Tmux) there is [the tmux fallback](https://github.com/anki-code/xontrib-output-search/pull/4) in case the output of last cmd is not available.

## Use cases
#### Get URL from output
```shell script
echo "Try https://github.com/xxh/xxh"
# Try https://github.com/xxh/xxh
git clone xx<Alt+F>
git clone https://github.com/xxh/xxh
```

#### Get key or value from JSON, Python dict and JavaScript object
```shell script
echo '{"Try": "xontrib-output-search"}'
# {"Try": "xontrib-output-search"}
echo I should try se<Alt+F>
echo I should try xontrib-output-search
```    

#### Get the path from environment
```shell script
env | grep ^PATH=
# PATH=/one/two:/three/four
ls fo<Alt+F>
ls /three/four  
```    

#### Complete the complex prefix

Get the URL from previous output after typing `git+`:
```shell script
echo "Try https://github.com/anki-code/xontrib-output-search"
# Try https://github.com/anki-code/xontrib-output-search

pip install git+xo<Alt+F>
pip install git+https://github.com/anki-code/xontrib-output-search
```
Get the port number from previous output while typing the URL:
```shell script
echo "The port number is 4242"
# The port number is 4242

curl http://127.0.0.1:4<Alt+F>
curl http://127.0.0.1:4242
```

#### Get arguments from command help
```shell script
lolcat -h
# ...
lolcat --s<Alt+F>
lolcat --seed=SEED
```

#### Use [tokenize-output](https://github.com/anki-code/tokenize-output) as a tool

```xsh
$(echo 'Hello "world"!' | tokenize-output -p).split()
# ['Hello', 'world']
```

## Environement variables

* `$XONTRIB_OUTPUT_SEARCH_WARNING` - show warnings from xontrib. Default `True`.

## Development

The xontrib-output-search is using [tokenize-output](https://github.com/anki-code/tokenize-output) for tokenizing.

Checking that `output_search` xontrib has been loaded:
```shell script
xontrib list output_search
# output_search  installed  loaded

completer list | grep output_search
# xontrib_output_search
```

## Known issues

#### `Alt+F` may not working in PyCharm terminal
Workaround: `f__` + <kbd>Tab</kbd>.

#### `Alt+F` in the readline is to move forward
Workaround: set `$XONTRIB_OUTPUT_SEARCH_KEY='i'` before `xontrib load output_search`.

#### Not working after [xonsh 0.10.0](https://github.com/xonsh/xonsh/releases/tag/0.10.0) ([4283](https://github.com/xonsh/xonsh/pull/4283))

Workaround: Check [`XONSH_CAPTURE_ALWAYS`](https://xon.sh/envvars.html#xonsh-capture-always) environment variable to bring the capturing of the output back i.e. `$XONSH_CAPTURE_ALWAYS=True`.

#### `cat file` is not captured ([xonsh/issues/3744](https://github.com/xonsh/xonsh/issues/3744))
Workaround: `cat file | head` or `cat file | grep text`.

#### The readline shell type was not tested

We're using the xonsh recommended prompt-toolkit shell type to test the output search xontrib. There could be the issues in the readline shell type. PRs are welcome!

## Links 
* This package is the part of [ergopack](https://github.com/anki-code/xontrib-ergopack) - the pack of ergonomic xontribs.
* This package was created with [xontrib cookiecutter template](https://github.com/xonsh/xontrib-cookiecutter).
* I was inspired by [xontrib-histcpy](https://github.com/con-f-use/xontrib-histcpy). Thanks @con-f-use!
