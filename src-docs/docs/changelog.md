# Changelog

[TOC]

This is the list of what has changed since the first version of *Duik for Blender*.

## 0.0.16

#### New

- [Pie menu with animation tools](animation-tools.md).
- Added a [Pie menu for the armature display options](tools.md).
- Added a [Pie menu for the auto-rig](tools.md) tools.
- Automatically [swap IK and FK](animation-tools.md).

#### Bugfixes

- Lots of bugfixes

## 0.0.6

#### New

- Added the [Texture Animation](texanim.md) tool.

#### Bugfixes

- Lots of bugfixes

## 0.0.5

#### New

- Added a [ui for bone layers](ui-layers.md) in the 3D View

## 0.0.4

#### Source code Improvement and cleaning

As the addon becomes bigger, there was a need to clean the source code to improve the groundwork of future features.

- Split the addon in modules and submodules for easier development and maintenance
- Added GPLv3 notices

## 0.0.3

#### Improvements

- [*FK Controller*](fk.md): the property for the "follow" option has been moved to the bone instead of the controller. Use a Duik [*UI Control*](ui-controls.md) to expose it on the controller if needed. Also, the way to rig the FK controller has been simplified a lot.

## 0.0.2

#### New

- [*UI Controls*](ui-controls.md)

#### Improvements

- [*BBone Controllers*](bbone.md) now control the bbone rotations more accurately, and the scale controls the curvature.

#### Fixes

- The *Assign* button for the [*Selection sets*](selection-sets.md) now work correctly even if the set has been created empty at first.
- The custom properties used by Duik no longer have wrong limits.

## 0.0.1

Initial release with:

- Rigging tools:
    - [*IK/FK rig*](ikfk.md)
    - [*FK Controller*](fk.md)
    - [*FK Controller (No Follow)*](fk.md)
    - [*BBone Controllers*](bbone.md)
- UI Controls:
    - [*Selection sets*](selection-sets.md)


<sub>*Last Modified on <script type="text/javascript"> document.write(document.lastModified) </script>*</sub>