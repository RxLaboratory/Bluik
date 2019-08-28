Select one bone and launch the tool.

This will create a single FK controller for the bone, which will control the rotation and the scale of the bone. If the bone was not connected to its parent, it will also control its location.

There's a *Follow* property on the bone used to make it inherit the parent rotation or not. This is very useful for necks, heads or arms. This control is available in the sidebar [N] of the *3D View* with the bone selected.

!!! tip
    Use a Duik [*UI Control*](ui-controls.md) to expose the follow property on the controller if needed by the animator.


<sub>*Last Modified on <script type="text/javascript"> document.write(document.lastModified) </script>*</sub>