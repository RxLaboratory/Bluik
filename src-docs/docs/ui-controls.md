With *Duik*, you can create nice UI controls for any (custom) property on the *Armature* you're working on.
This is a way to expose and group the controls needed by the animator using the rig in the `Item` tab of the *sidebar* of the *3D View* (with the transform properties), while keeping any other custom property hidden on bones not used as controllers. These controls have a better display than the native custom properties too.

[TOC]

# Create and manage controls

In the `Armature data` tab of the `Properties` panel, you'll find the *Duik UI Contrlos* Panel.

![](img\ui-controls-config.png)

Select a bone and click on the `+` button to create a UI Control.

You can also duplicate an existing control using the menu under the down arrow, which will automatically be updated depending on the bone currently selected, to quickly create another control for a property with the same name on another bone.

This control will be automatically added on the selected bone. You can add and remove any UI Control to any other bone using the `Assign` and `Remove` button.

# The UI

These *Duik Controls* are available in the *sidebar* of the *3D View*, in the `Item` tab.

![](img\ui-controls.png)

Duik will try to build a nice layout, depending on the names of the controls, and their order in the list. Each time an *.R* suffix followed by an *.L* suffix is found, the two sets are showed in a row.

!!! tip
    UI controls are a very nice way to expose (or not) the controls which may be useful for the animator, while keeping the other custom properties hidden.  
    Their UI is also nicer than the UI of the native custom properties.

!!! note
    Keep in mind that you can have the same UI Control on several bones at once, which is a nice way to be able to animate the same property from different places

# Configuration of the controls

![](img\ui-controls-config-details.png)

There are three types of UI Controls:

- __*Label*__ is a simple text shown in the UI.
- __*Separator*__ is a blank space.
- __*Single Property*__ is an actual control.

## Single property

When set on *Single Property*, the control has some options:

- *Bone:* is the bone where to find the controlled property.
- *Path:* is the **last part only** of the path copied when [right-click] on the property and choosing *copy data path*.
- *Toggle:* is not yet implemented.
- *Slider:* changes the apperances of the control, to be either a slider or a simple value.

!!! note
    In future versions, the *Path* option will be updated to work the same way as in drivers, using the full data path from any object.