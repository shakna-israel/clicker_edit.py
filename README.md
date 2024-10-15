# clicker_edit.py

A CLI tool and library for editing and modifying your Clicker Heroes save files.

---

This works with the newer save file style. (Which should now be supported by all platforms.)

A small hash of the word 'zlib', followed by base64-encoded raw-zlib'd JSON data.

Anyways...

The CLI tool automatically finds and builds all the command-line options from the savefile. This means that if any new options are introduced, you'll automatically be able to modify them.

However, that does mean it *requires* a save file to operate. You can't start from scratch.

---

## Basic CLI Usage

	python3 clicker_edit.py SAVEFILE --help

Replace `SAVEFILE` with the file path to your save file.

* You can obtain a save file by opening Clicker Heroes, going to Settings, and clicking 'Save'.

There are a *lot* of things you can tweak.

e.g.

	python3 clicker_edit.py SAVEFILE --not-hasSeenZone100Tip

This will disable the `hasSeenZone100Tip` flag.

All the `default` values come from the current status in your save file.

---

## Library Usage

### `load(filename)`

Given a filename, loads the save file into a dictionary.

### `loads(source)`

Given a string containing the encoded data, loads the save into a dictionary.

### `compile(data, filename)`

Given a dictionary for data, and an output filename, writes an encoded save file.

### `compiles(data)`

Given a dictionary for data, returns a string representing an encoded save file.

---

# License

Public Domain. Exact terms in [LICENSE.md](LICENSE.md).
