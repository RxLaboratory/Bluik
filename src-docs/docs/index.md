Welcome to the official *Duik for Blender* documentation.

![cel anim panel](img\logo-blender.png)

*Duik* is originally a comprehensive animation and rigging toolset for __*Adobe After Effects*__.  
It all began as a joke... __When will *Duik* be available for *Blender*?__

*Duik for Blender* aims to reproduce the rigging process developped in After Effects but in blender, with predefined Armatures and bones for limbs or complete characters and a comprehensive yet easy to animate auto-rig, along with some advanced rigging and animation tools for experts.

**It is in an early phase of the development**, but it may already be useful for 3D riggers.  
Rigging is already very nice natively in *Blender*, but there are always some automations that can be done to make your process faster and easier.

# Introduction

The first tools which have been developped are some bits of automations for creating nice controllers for very common techniques in 3D rigging, like animatable IK/FK (with bend and stretch controls), FK controllers, intuitive bendy-bone controllers, and some nice UI components...

The goal is to add more low-level tools first, and then build upon them to have nice auto-rigs and animation tools, both for 3D and 2D cut-out animation.

## 3D

Blender already includes an auto-rig add-on called *Rigify* but it's a tool which only rigs complete characters at once. Sometimes it's better to be able to customize a lot the character and to have some low-level tools too, more modular. Another issue with rigify is that the rigs it creates may be too complex for animators, as there are a lot of unnecessary controls, or at least controls which should be deactivated or hidden by default. This can be a big issue for animators; character rigs have to stay intuitive, easy-to-use and with as few main controls as possible, hiding less useful controls for details.

Duik for Blender tries to address these issues by using a modular system, with low, mid and high-level tools. Low-level tools are more advanced and modular, as high-level tools are pretty standard auto-rigs for limbs or complete characters. The rigs created by Duik have all controls needed for a perfect animation (there are no compromise on usability), but always built with a priority on intuitivity and easiness (controls are sorted out based on their importance, there are no unnecessary control).

For now, Duik for Blender only includes low-level tools for controllers creation, which will be used to build high-level auto-rigs.  
The first goal for the upcoming versions of *Duik for Blender*, is to build robust, useful, and modular tools for advanced and professionnal riggers.  
Another goal for future development of *Duik for Blender* is to make it easy to use for beginners with automatic tools and auto-rigs working the same way as *Duik for After Effects*, with the same process (Armature -> Autorig -> Details).


## 2D (Cut-out)

The other important goal for the development of *Duik for Blender* is to develop a way to quickly and easily rig cut-out characters, with or without deformations, exactly the same way as in *After Effects*. This would make the animation step with this style of animation really easier and quicker than in After Effects, thanks to the performance of *Blender*.

Then, Duik could ease the process of exporting or rendering the character and its animation from *Blender* to import in After Effects for compositing.

One could even imagine that characters could be rigged either in After Effects or in Blender, and animated in both, with Duik developped for both softwares.

## Plans

There's no precise schedule to develop all of this yet, as the only revenue for these development (and the support of the tools, the maintainment of the website, etc) is what [Duduf](http://duduf.com) (the developper) gets on [Patreon](https://patreon.com/duduf), and this is going to be a huge work. But, step by step, we'll see how it goes.

Maybe after building a few more tools it could be time for a crowdfunding campaign. But absolutely nothing's sure yet, these are just assumptions!


<sub>*Last Modified on <script type="text/javascript"> document.write(document.lastModified) </script>*</sub>