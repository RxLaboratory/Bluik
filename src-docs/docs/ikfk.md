`3D View ‣ Menu ‣ Pose ‣ Duik Auto-Rig`  
`3D View ‣ [SHIFT + R]`  
Available in *pose mode* only

Select a chain of two bones parented together, and launch the tool.

It will create a comprehensive IK/FK rig for these two bones, with the ability to switch between IK and FK, curve the limb, and adjust the stretchiness.

**Four controllers are created, two for the IK and two for the FK:**

- __*limb.IK.Ctrl*__ is the main controller for the IK.
- __*limb.Pole.Ctrl*__ is the controller for the pole angle of the IK, which is either controlled by the location of this controller or by the custom property on the *limb.IK.Ctrl* bone.
- __*upperBoneName.FK.Ctrl*__ is the FK controller for the upper part of the limb. See [FK Controller](fk.md) for more information.
- __*lowerBoneName.FK.Ctrl*__ is the FK controller for the lower part of the limb. See [FK Controller](fk.md) for more information.

The controls for the options are added as custom properties on the *limb.IK.Ctrl* bone, used as a controller for the IK.
You can find them in the sidebar [N] of the *3D View* with the controller selected.

![IK/FK Sidebar](img/ikfk-sidebar.png)

!!! hint
    These properties can be exposed on several controllers at once, with a better UI/UX using the [UI Controls](ui-controls.md) tools.



<sub>*Last Modified on <script type="text/javascript"> document.write(document.lastModified) </script>*</sub>