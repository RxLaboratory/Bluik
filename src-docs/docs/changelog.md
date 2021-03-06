# Changelog

[TOC]

This is the list of what has changed since the first version of *Duik for Blender*.

## 0.5.5

#### New

- Added a "Create scene" operator, in the `3D view > Add` menu

## 0.5.4

- Fixed an error showing in the console when linking collections

## 0.5.3

- Fixed an error happening when (re)moving an image in the TexAnim module.

## 0.5.2

#### New

- Added an operator to reset [Custom UI Controls](ui-controls.md) to their default values.

## 0.5.0

#### New

- [Dope Sheet and Graph Editor filters](dopesheet-filters.md)

#### Bugfixes

- Improved [TexAnim](texanim.md) and fixed a few bugs.

## 0.4.0

#### New

- Added the [OCA Importer](oca.md)

## 0.2.0

#### New

- [Camera Linker](objects.md)

## 0.0.20

#### Bugfixes

- The [TexAnim](texanim.md) now updates correctly the textures when are nested inside node groups.
- Fixed textures which could not be moved or removed from [TexAnim](texanim.md) when it's nested inside node groups.

## 0.0.18

#### Bugfixes

- The [TexAnim](texanim.md) now works correctly when the textures are nested inside node groups.

## 0.0.17

#### Bugfixes

- The [TexAnim](texanim.md) keyframes are now correctly updated when modifying the list of images if the list already has keyframes.
- The [TexAnim](texanim.md) is now correctly updated when navigating the timeline with the keyboard shortcuts ( [->] and [<-] )

#### New

- [Pie menu with animation tools](animation-tools.md).
- Added a [Pie menu for the armature display options](armatures.md).
- Added a [Pie menu for the auto-rig](armatures.md) tools.
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