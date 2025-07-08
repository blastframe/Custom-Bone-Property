bl_info = {
    "name": "Add/Remove Custom Bone Properties",
    "blender": (3, 0, 0),
    "category": "Armature",
    "author": "Blastframe",
    "version": (1, 0, 0),
    "description": "Adds/Removes a custom property to each bone in the active armature",
}

import bpy
from bpy.types import Operator
from bpy.props import (
    IntProperty,
    EnumProperty,
    BoolProperty,
    FloatProperty,
    StringProperty,
    IntVectorProperty,
    FloatVectorProperty,
    BoolVectorProperty,
)
from bpy.utils import register_class, unregister_class


class BLASTFRAME_OT_add_custom_bone_prop(Operator):
    """Add a custom property to each bone in the active armature"""

    bl_idname = "object.add_custom_bone_prop"
    bl_label = "Add Custom Bone Property"
    bl_options = {"REGISTER", "UNDO"}

    prop_type: EnumProperty(
        name="Property Type",
        description="Type of the custom property",
        items=[
            ("INT", "Integer", "Add an integer custom property"),
            ("FLOAT", "Float", "Add a float custom property"),
            ("FLOAT_ARRAY", "Float Array", "Add a float array custom property"),
            ("INT_ARRAY", "Integer Array", "Add an integer array custom property"),
            ("BOOLEAN", "Boolean", "Add a boolean custom property"),
            ("BOOLEAN_ARRAY", "Boolean Array", "Add a boolean array custom property"),
            ("STRING", "String", "Add a string custom property"),
        ],
        default="INT",
    )

    min_int_value: IntProperty(
        name="Min Value",
        description="Minimum value for the custom property",
        default=0,
        min=0,
    )

    max_int_value: IntProperty(
        name="Max Value",
        description="Maximum value for the custom property",
        default=200,
        min=0,
    )

    min_float_value: FloatProperty(
        name="Min Float Value",
        description="Minimum value for the custom property",
        default=0.0,
        min=0.0,
    )

    max_float_value: FloatProperty(
        name="Max Float Value",
        description="Maximum value for the custom property",
        default=200.0,
        min=0.0,
    )

    default_boolean_value: BoolProperty(
        name="Default Boolean Value",
        description="Default value for the custom property",
        default=False,
    )

    default_boolean_array_value: BoolProperty(
        name="Default Boolean Array Value",
        description="Default value for the custom property",
        default=False,
    )

    default_string_value: StringProperty(
        name="Default String Value",
        description="Default value for the custom property",
        default="Hello World",
    )

    default_min_int_array_value: IntVectorProperty(
        name="Default Int Array Value",
        description="Default value for the custom property",
        default=[0],
        min=0,
    )

    default_max_int_array_value: IntVectorProperty(
        name="Default Int Array Value",
        description="Default value for the custom property",
        default=[1],
        min=0,
    )

    default_min_float_array_value: FloatVectorProperty(
        name="Default Float Array Value",
        description="Default value for the custom property",
        default=[0.0],
        min=0.0,
    )

    default_max_float_array_value: FloatVectorProperty(
        name="Default Float Array Value",
        description="Default value for the custom property",
        default=[1.0],
        min=0.0,
    )

    method: EnumProperty(
        name="Method",
        description="Method to use for adding the custom property",
        items=[
            ("ADD", "Add", "Add a new custom property"),
            ("REMOVE", "Remove", "Remove existing custom properties"),
        ],
        default="ADD",
    )

    separator: EnumProperty(
        name="Separator",
        description="Separator to use for the custom property name",
        items=[
            ("_", "_ Underscore", "Use single underscore as separator"),
            ("__", "__ Double Underscore", "Use double underscore as separator"),
            (".", ". Dot", "Use dot as separator"),
        ],
        default="_",
    )

    suffix: StringProperty(
        name="Suffix",
        description="Suffix to append to the custom property name",
        default="TO",
    )

    prop_name_format: StringProperty(
        name="Property Name Format",
        description="Format for the custom property name. Use {armature} and {bone} as tokens.",
        default="{armature}_{bone}_{suffix}",
    )

    def clean_string(self, s):
        """Clean a string by replacing unwanted characters."""
        s = s.replace(".", self.separator) if s else s
        s = s.replace(" ", self.separator) if s else s
        s = s.replace("-", self.separator) if s else s
        s = s.replace("_", self.separator) if s else s
        return s

    def execute(self, context):
        armature = context.object
        if armature and armature.type == "ARMATURE":
            bone_count = 0
            bones = armature.pose.bones
            prev_mode = context.mode
            if prev_mode == "OBJECT":
                bones = armature.data.bones
            elif prev_mode == "POSE":
                bones = context.selected_pose_bones
            elif prev_mode == "EDIT_ARMATURE":
                # switch to pose mode to access pose bones
                bpy.ops.object.mode_set(mode="POSE")
                bones = armature.pose.bones

            for bone in bones:
                # custom property
                prop_name = self.prop_name_format.format(
                    armature=self.clean_string(armature.name),
                    bone=self.clean_string(bone.name),
                    suffix=self.suffix,
                    separator=self.separator,
                )
                if self.method == "ADD":
                    if prop_name not in bone:
                        if self.prop_type == "INT":
                            bone[prop_name] = self.min_int_value
                            ui = bone.id_properties_ui(prop_name)
                            ui.update(
                                description=f"Custom {self.prop_type} property for {armature.name} bone {bone.name}",
                                min=self.min_int_value,
                                max=self.max_int_value,
                            )
                        elif self.prop_type == "BOOLEAN":
                            bone[prop_name] = self.default_boolean_value
                            ui = bone.id_properties_ui(prop_name)
                            ui.update(
                                description=f"Custom {self.prop_type} property for {armature.name} bone {bone.name}",
                            )
                        elif self.prop_type == "FLOAT":
                            bone[prop_name] = self.default_min_float_value
                            ui = bone.id_properties_ui(prop_name)
                            ui.update(
                                description=f"Custom {self.prop_type} property for {armature.name} bone {bone.name}",
                                min=self.min_float_value,
                                max=self.max_float_value,
                            )
                        elif self.prop_type == "FLOAT_ARRAY":
                            bone[prop_name] = [
                                self.default_min_float_array_value,
                                self.default_max_float_array_value,
                            ]
                            ui = bone.id_properties_ui(prop_name)
                            ui.update(
                                description=f"Custom {self.prop_type} property for {armature.name} bone {bone.name}",
                                min=self.default_min_float_array_value,
                                max=self.default_max_float_array_value,
                            )
                        elif self.prop_type == "INT_ARRAY":
                            bone[prop_name] = [
                                self.default_min_int_array_value,
                                self.default_max_int_array_value,
                            ]
                            ui = bone.id_properties_ui(prop_name)
                            ui.update(
                                description=f"Custom {self.prop_type} property for {armature.name} bone {bone.name}",
                                min=self.default_min_int_array_value,
                                max=self.default_max_int_array_value,
                            )
                        elif self.prop_type == "BOOLEAN_ARRAY":
                            bone[prop_name] = [
                                self.default_boolean_array_value,
                                self.default_boolean_array_value,
                            ]
                            ui = bone.id_properties_ui(prop_name)
                            ui.update(
                                description=f"Custom {self.prop_type} property for {armature.name} bone {bone.name}",
                                min=self.default_boolean_array_value,
                                max=self.default_boolean_array_value,
                            )
                        elif self.prop_type == "STRING":
                            bone[prop_name] = self.default_string_value
                            ui = bone.id_properties_ui(prop_name)
                            ui.update(
                                description=f"Custom {self.prop_type} property for {armature.name} bone {bone.name}",
                            )

                        bone_count += 1
                elif self.method == "REMOVE":
                    if prop_name in bone:
                        del bone[prop_name]
                        bone_count += 1
            bpy.ops.object.mode_set(mode=prev_mode)

        action = "Added" if self.method == "ADD" else "Removed"

        if bone_count == 0:
            self.report({"INFO"}, "No custom properties found to remove")
            return {"CANCELLED"}

        self.report(
            {"INFO"},
            f"{action} custom property from {bone_count} bones in {armature.name}",
        )

        return {"FINISHED"}

    def invoke(self, context, event):
        # props dialog
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "prop_type")
        if self.prop_type == "INT":
            layout.prop(self, "min_int_value")
            layout.prop(self, "max_int_value")
        elif self.prop_type == "FLOAT":
            layout.prop(self, "min_float_value")
            layout.prop(self, "max_float_value")
        elif self.prop_type == "BOOLEAN":
            layout.prop(self, "default_boolean_value")
        elif self.prop_type == "FLOAT_ARRAY":
            layout.prop(self, "default_min_float_array_value")
            layout.prop(self, "default_max_float_array_value")
        elif self.prop_type == "INT_ARRAY":
            layout.prop(self, "default_min_int_array_value")
            layout.prop(self, "default_max_int_array_value")
        elif self.prop_type == "BOOLEAN_ARRAY":
            layout.prop(self, "default_boolean_array_value")
        elif self.prop_type == "STRING":
            layout.prop(self, "default_string_value")

        layout.prop(self, "method")
        layout.prop(self, "separator")
        layout.prop(self, "suffix")
        layout.prop(self, "prop_name_format")


def custom_prop_menu(self, context):
    """Add custom property menu to the object context menu."""
    if context.object is None or context.object.type != "ARMATURE":
        return
    layout = self.layout
    layout.operator_context = "INVOKE_DEFAULT"
    layout.operator(
        BLASTFRAME_OT_add_custom_bone_prop.bl_idname,
        text="Add Custom Bone Property",
        icon="BONE_DATA",
    )


def register():
    register_class(BLASTFRAME_OT_add_custom_bone_prop)
    bpy.types.VIEW3D_MT_object_context_menu.append(custom_prop_menu)


def unregister():
    bpy.types.VIEW3D_MT_object_context_menu.remove(custom_prop_menu)
    unregister_class(BLASTFRAME_OT_add_custom_bone_prop)


if __name__ == "__main__":
    register()
