# Bluik
2D/Cut-Out Rigging and Animation tools for Blender

We're developing a lot of tools for Blender. We're collecting the ones which can already be tested in this add-on, which will ultimately become Bluik (Duik for Blender), and maybe some other more official add-ons.

## OCA - Open Cel Animation

OCA, Open Cel Animation format, is an open format to ease the exchange of traditionnal/frame-by-frame/cel animation between different applications.  
For now, Bluik is the best way to import [OCA](https://rxlaboratorio.org/rx-tool/oca/) documents in Blender.

Note that we're working on a proper OCA-Importer extension for Blender which will ultimately replace this feature from Bluik.

## Dependencies

Some of the code needed by Duik is shared with other tools, and kept in other specific repos.

- [DuBLF](https://codeberg.org/Duduf-Blender/DuBLF) is a python module with specific Blender tools.
- [DuPYF](https://codeberg.org/Duduf/DuPYF) is a python module with generic python tools. The files from this module must be copied *inside* the `dublf` module. Sorry this is a bit nasty, but it's temporary.
- [OCO](https://codeberg.org/OCO/OCO) is the repo for the Open Cut-Out format we're implementing in Bluik.

These modules must be copied/symlinked in the `bluik` folder, like this:

```sh
> bluik
    > dublf # contains both dublf and dupyf files
    > oco
```

Note that we're also in the process of re-organizing those dependencies and this will change eventually.

## Join the community

Join us if you need any help, if you want to contribute (we're always in need for translations, writing the doc, fixing bugs, making tutorials, developing new features...) or just want to show what you're doing with our tools!

We need your support to release our free tools. You can [donate](http://donate.rxlab.info) or [join the development fund to get an early access to the tools](http://membership.rxlab.info).

- Come and have a [chat on Discord](http://chat.rxlab.info).
- [Donate](http://donate.rxlab.info) or join the [membership](http://membership.rxlab.info).
- Follow us on [Facebook](https://www.facebook.com/rxlaboratory),  [Instagram](https://www.instagram.com/rxlaboratory/), [Youtube](https://www.youtube.com/@rxlab), [LinkedIn](https://www.linkedin.com/company/RxLaboratory/)...
- Read the [Contributor Covenant](CODE_OF_CONDUCT.md)