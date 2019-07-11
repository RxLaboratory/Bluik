# Changelog

This is the list of what has changed since the first version of *Duik for Blender*.

## 0.0.3 (in development)

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