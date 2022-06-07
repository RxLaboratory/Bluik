#====================== BEGIN GPL LICENSE BLOCK ======================
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#======================= END GPL LICENSE BLOCK ========================

# <pep8 compliant>

# OCO Import

import time
import numpy as np
import bpy # pylint: disable=import-error
import bmesh
import mathutils as mu
from mathutils.geometry import tessellate_polygon
from bpy_extras.image_utils import load_image # pylint: disable=import-error
from bpy_extras.object_utils import ( # pylint: disable=import-error
    AddObjectHelper,
)
from .ocopy import oco # pylint: disable=import-error
from . import dublf
from .dublf import image as ilib # pylint: disable=import-error
from .dublf import geo # pylint: disable=import-error
from . import layers

class IMPORT_OCO_OT_import(bpy.types.Operator, AddObjectHelper):
    """Imports Open Cut-Out Assets"""
    bl_idname = "import_oco.import"
    bl_label = "Import OCO assets"
    bl_options = {'REGISTER', 'PRESET', 'UNDO'}

    # File Dialog properties
    filepath: bpy.props.StringProperty(maxlen=1024, subtype='FILE_PATH', options={'HIDDEN', 'SKIP_SAVE'})
    filename: bpy.props.StringProperty(maxlen=1024, subtype='FILE_PATH', options={'HIDDEN', 'SKIP_SAVE'})
    directory: bpy.props.StringProperty(maxlen=1024, subtype='FILE_PATH', options={'HIDDEN', 'SKIP_SAVE'})

    # Options
    shader: bpy.props.EnumProperty(
        name="Shader",
        items= (
            ('PRINCIPLED',"Principled","Principled Shader"),
            ('SHADELESS', "Shadeless", "Only visible to camera and reflections"),
            ('EMISSION', "Emit", "Emission Shader"),
        ),
        default='SHADELESS', 
        description="Node shader to use"
        )

    smooth: bpy.props.IntProperty(
        name="Smoothing",
        min=0,
        max=100,
        default=0,
        description="Smooth source pixels"
    )

    cutoff: bpy.props.FloatProperty(
        name="Cutoff",
        min=0.0001,
        max=0.9999,
        default=0.5,
        description="Threshold in the alpha channel in which the selected pixel is considered visible",
    )

    def draw(self, context):
        def spacer(inpl):
            row = inpl.row()
            row.ui_units_y = 0.5
            row.label(text="")
            return row

        # pixel
        col = self.layout.box()
        col = col.column(align=True)

        row = col.row()
        row.label(text="Pixels", icon="NODE_TEXTURE")

        spacer(col)

        row = col.row(align=True)
        row.prop(self, "smooth")

        row = col.row(align=True)
        row.prop(self, "cutoff")

        # shader
        col = self.layout.box()
        col = col.column(align=True)
        row = col.row()
        row.label(text="Material", icon="MATERIAL")

        spacer(col)

        row = col.row(align=True)
        row.prop(self, 'shader', expand=True)

    def invoke(self, context, event):
        engine = context.scene.render.engine
        if engine not in {'CYCLES', 'BLENDER_EEVEE'}:
            if engine != 'BLENDER_WORKBENCH':
                self.report({'ERROR'}, "Cannot generate materials for unknown %s render engine" % engine)
                return {'CANCELLED'}
            else:
                self.report({'WARNING'},
                            "Generating Cycles/EEVEE compatible material, but won't be visible with %s engine" % engine)

        # Open file browser
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        if not bpy.data.is_saved:
            self.relative = False

        # this won't work in edit mode
        editmode = context.preferences.edit.use_enter_edit_mode
        context.preferences.edit.use_enter_edit_mode = False
        if context.active_object and context.active_object.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        self.import_oco(context)

        context.preferences.edit.use_enter_edit_mode = editmode

        return {'FINISHED'}

    def import_oco(self, context):
        ocoDocument = oco.load(self.filepath)

        print("Importing OCO: " + ocoDocument['name'])

        # Get/Create Duik Scene
        scene = layers.get_create_scene(context)

        # Layers
        for layer in ocoDocument['layers']:
            self.import_layer(context, layer, scene)

        # Let's redraw
        dublf.ui.redraw()

        print("OCO correctly imported")

    def import_layer(self, context, ocoLayer, containing_group, depth=0):
        layer_type = ocoLayer['type']

        if layer_type == 'grouplayer':
            print('Importing OCO Group: ' + ocoLayer['name'])
            group = layers.create_group(context, ocoLayer['name'], containing_group)
            for layer in ocoLayer['childLayers']:
                depth = self.import_layer(context, layer, group, depth)
            group.hide_viewport = not ocoLayer['visible']
            group.hide_render = ocoLayer['reference']
        else:
            print('Importing OCO Layer: ' + ocoLayer['name'])
            depth = depth - .01
            # Animated: create a group for it
            if ocoLayer['animated']:
                containing_group = layers.create_group(context, ocoLayer['name'], containing_group)
            # Create images to leafig them
            for frame in ocoLayer['frames']:
                r = self.import_image(context, frame['fileName'], ocoLayer['name'], frame['opacity'])
                if r is None:
                    continue
                layer = r[0]
                shader = r[0]
                layers.set_as_layer(layer, containing_group)
                layers.set_layer_position( layer, ocoLayer['position'] )
                layer.duik_layer.depth = depth
                if ocoLayer['label'] != 0:
                    shader.diffuse_color = oco.OCOLabels[ ocoLayer['label'] % 8 +1 ]

        return depth

    def import_image(self, context, image_path, name, opacity=1.0):
        print("Importing image: " + image_path)
        image = load_image(image_path, check_existing=True, force_reload=True)
        if not image:
            print("Import failed")
            return None

        # We need an image editor
        #bpy.ops.render.view_show("INVOKE_DEFAULT")

        wm = context.window_manager

        tot = 1000
        wm.progress_begin(0, tot)
        wm.progress_update(100)

        t0 = time.time()
        pixels = np.float32(np.array(image.pixels[:]).reshape(image.size[1], image.size[0], 4))

        print("load pixels from Blender: {:.2f} sec".format(time.time() - t0))
        t0 = time.time()

        xdim = pixels.shape[0]
        ydim = pixels.shape[1]
        mindim = min(xdim, ydim)
        st = 1
        # st = int(self.prg.downsample)

        wm.progress_update(200)

        # convert from linear to srgb
        bcol = np.array([ilib.linear2srgb(i) for i in (0.0, 0.0, 0.0)], dtype=np.float32)

        pixels[:, :, :3] = np.abs(pixels[:, :, :3] - bcol)
        res = pixels[:, :, 3]

        print("image conversion: {:.2f} sec".format(time.time() - t0))
        t0 = time.time()

        wm.progress_update(300)

        if self.smooth > 0:
            sval = 1 + self.smooth * 2
            krn = np.ones(sval) / sval
            f_krn = lambda m: np.convolve(m, krn, mode="same")
            res = np.apply_along_axis(f_krn, axis=1, arr=res)
            res = np.apply_along_axis(f_krn, axis=0, arr=res)

            print("smoothing: {:.2f} sec".format(time.time() - t0))
            t0 = time.time()

        wm.progress_update(400)

        nm = res > self.cutoff
        l_verts = geo.lines_marching(res, self.cutoff, nm)

        print("pixel logic: {:.2f} sec".format(time.time() - t0))
        t0 = time.time()

        wm.progress_update(500)

        chains = geo.parse_segments(self, l_verts)

        print("parse: {:.2f} sec".format(time.time() - t0))
        t0 = time.time()

        wm.progress_update(600)

        if not chains or len(chains) == 0:
            print("Duik: No polygons found at this cutoff/smoothing values")
            return None

        # biggest chain first
        chains = sorted(chains, key=lambda x: -len(x))

        # move verts to right location (to match image/pixel/edge)
        for c in chains:
            for i, v in enumerate(c.verts):
                c.verts[i] = (c.verts[i][0] + 1.0, c.verts[i][1] + 1.0)

        # build polys
        for chain in chains:
            # if not self.prg.sharp_pixels:
            # chain.smooth(0.5, 2)
            chain.simplify(1.0)

        print("num chains:", len(chains))

        print("simplify: {:.2f} sec".format(time.time() - t0))
        t0 = time.time()

        wm.progress_update(700)

        # go through chain, is it inside any other chain?
        print(len(chains), end=" -> ")
        chains = [c for c in chains if not c.invalid]
        print(len(chains), end=" filtered\n")

        if len(chains) == 0:
            print("Leafig: No polygons found at this cutoff/pixel error values")
            return None

        # find outer loops
        roots = []
        lch = len(chains)
        for ci, c in enumerate(chains):
            wm.progress_update(800 + 100 * ci // lch)
            inside = False
            for i in chains:
                if c == i:
                    continue
                if c.inside(i):
                    inside = True
                    break

            # if chain is not inside any other, mark it as root
            if not inside:
                roots.append(c)

        groups = [[c] for i, c in enumerate(roots)]

        print("groups: {:.2f} sec".format(time.time() - t0))
        t0 = time.time()

        def wrap(n_func, root):
            # create mesh
            mesh = bpy.data.meshes.new(name + ".duik_mesh")
            obj = bpy.data.objects.new(name + ".Cutout", mesh)
            context.collection.objects.link(obj)
            mesh = obj.data
            bm = bmesh.new()

            n_func(bm, root)

            bmesh.ops.beautify_fill(bm, faces=bm.faces[:], edges=bm.edges[:])

            # TODO: only build partial spine at the tips
            # geo.build_spine(bm)

            # write UV
            uv_layer = bm.loops.layers.uv.verify()
            for f in bm.faces:
                for vert, loop in zip(f.verts, f.loops):
                    loop[uv_layer].uv = (
                        (vert.co[0] * mindim - 0.5) / ydim,
                        (vert.co[2] * mindim - 0.5) / xdim,
                    )

            # move object origin
            ploc = root[0].get_end_location('CENTER')
            offset = mu.Vector([-ploc[1], 0.0, -ploc[0]]) * st / mindim
            for v in bm.verts:
                v.co += offset

            # make the bmesh the object's mesh
            bm.to_mesh(mesh)
            bm.free()
            obj.location = -offset

            # selecting the object might disrupt trying to determine correct border values
            # obj.select_set(True)
            # context.view_layer.objects.active = obj

            # if self.prg.create_material:
            mat, texture_node = dublf.materials.create_im_material(image, "cutout_" + image.name, self.shader)
            mat.node_tree.nodes['Opacity'].inputs[1].default_value = opacity
            obj.data.materials.append(mat)

            return obj, mat

        def create(bm, g):
            inp = [[mu.Vector(v) for v in c.verts] for c in g]
            polys = tessellate_polygon(inp)

            # write to bmesh
            sverts = []
            for l in inp:
                for v in l:
                    loc = (v[1] * st / mindim, 0.0, v[0] * st / mindim)
                    sverts.append(bm.verts.new(loc))

            bm.verts.ensure_lookup_table()
            # ff = set([])
            for p in polys:
                # ensure no dupe faces
                # ids = frozenset(tuple(sverts[i].index for i in p))
                # if ids not in ff:
                #     ff.add(ids)
                bm.faces.new([sverts[i] for i in p])
                # else:
                #     print("Leafig: Dupe face.")

        def loop_wrap(bm, x):
            for g in groups:
                create(bm, g)

        obj, mat = wrap(loop_wrap, groups[0])

        print("tessellate: {:.2f} sec".format(time.time() - t0))
        t0 = time.time()

        wm.progress_end()

        return obj, mat

def import_oco_button(self, context):
    self.layout.operator(IMPORT_OCO_OT_import.bl_idname, text="Open Cut-Out (OCO)", icon='ARMATURE_DATA')

classes = (
    IMPORT_OCO_OT_import,
)

def register():
    # register
    for cls in classes:
        bpy.utils.register_class(cls)

    # Menu item
    bpy.types.TOPBAR_MT_file_import.append(import_oco_button)

def unregister():
    # unregister
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    # Menu item
    bpy.types.TOPBAR_MT_file_import.remove(import_oco_button)
