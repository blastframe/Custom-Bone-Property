bl_info = {
    "name": "Add/Remove Custom Bone Properties",
    "blender": (3, 0, 0),
    "category": "Armature",
    "author": "Blastframe",
    "version": (1, 0, 0),
    "description": "Adds/Removes a custom property to each bone in the active armature",
    "doc_url": "https://blastframe.com/contact/",
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


# Redraw all regions in all areas (for UI update after property changes)
def refresh():
    for area in bpy.context.screen.areas:
        for region in area.regions:
            region.tag_redraw()


class BLASTFRAME_OT_add_custom_bone_prop(Operator):
    """Add/Remove a custom property to each bone in the active armature"""

    bl_idname = "object.add_custom_bone_prop"
    bl_label = "Custom Bone Property"
    bl_options = {"REGISTER", "UNDO"}

    # Property type selection
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

    # Add or remove method
    custom_method: EnumProperty(
        name="Method",
        description="Method to use for adding the custom property",
        items=[
            ("ADD", "Add", "Add a new custom property"),
            ("REMOVE", "Remove", "Remove existing custom properties"),
        ],
        default="ADD",
    )

    # Integer property min/max
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

    # Float property min/max
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

    # Default values for boolean, string, and arrays
    default_boolean_value: BoolProperty(
        name="Default Boolean Value",
        description="Default value for the custom property",
        default=False,
    )
    default_boolean_array_value: BoolVectorProperty(
        name="Default Boolean Array Value",
        description="Default value for the custom property",
        default=(False, False, False),
        size=3,
    )
    default_string_value: StringProperty(
        name="Default String Value",
        description="Default value for the custom property",
        default="Hello World",
    )

    # Default values for int/float arrays
    default_min_int_array_value: IntVectorProperty(
        name="Default Int Array Value",
        description="Default value for the custom property",
        default=(0, 0, 0),
        size=3,
        min=0,
    )
    default_max_int_array_value: IntVectorProperty(
        name="Default Int Array Value",
        description="Default value for the custom property",
        default=(1, 1, 1),
        min=0,
    )
    default_min_float_array_value: FloatVectorProperty(
        name="Default Float Array Value",
        description="Default value for the custom property",
        default=(0.0, 0.0, 0.0),
        size=3,
        min=0.0,
    )
    default_max_float_array_value: FloatVectorProperty(
        name="Default Float Array Value",
        description="Default value for the custom property",
        default=(1.0, 1.0, 1.0),
        min=0.0,
    )

    # Separator and suffix for property name
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
        if context.object is None or armature.type != "ARMATURE":
            self.report({"ERROR"}, "No active armature found")
            return {"CANCELLED"}
        bone_count = 0
        bones = armature.pose.bones
        prev_mode = context.mode

        # Switch to pose mode if needed to access pose bones
        if prev_mode == "OBJECT":
            bpy.ops.object.mode_set(mode="POSE")
            bones = armature.pose.bones
        elif prev_mode == "POSE":
            bones = context.selected_pose_bones
        elif prev_mode == "EDIT_ARMATURE":
            bpy.ops.object.mode_set(mode="POSE")
            bones = armature.pose.bones

        for bone in bones:
            # Build the custom property name using the format string and tokens
            prop_name = self.prop_name_format.format(
                armature=self.clean_string(armature.name),
                bone=self.clean_string(bone.name),
                suffix=self.suffix,
                separator=self.separator,
            )
            if self.custom_method == "ADD":
                if prop_name not in bone:
                    # Add property based on type
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
            elif self.custom_method == "REMOVE":
                # Remove property if it exists
                if prop_name in bone:
                    del bone[prop_name]
                    bone_count += 1

        # Restore previous mode and refresh UI
        bpy.ops.object.mode_set(mode=prev_mode)
        refresh()

        action = "Added" if self.custom_method == "ADD" else "Removed"

        if bone_count == 0:
            self.report({"INFO"}, "No custom properties found to remove")
            return {"CANCELLED"}

        self.report(
            {"INFO"},
            f"{action} custom property to {bone_count} bones in {armature.name}",
        )

        return {"FINISHED"}

    def invoke(self, context, event):
        # Show the operator properties dialog
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "prop_type")
        layout.prop(self, "custom_method")

        # Show relevant property fields based on type
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

        # Name formatting options
        layout.prop(self, "separator")
        layout.prop(self, "suffix")
        layout.prop(self, "prop_name_format")

    @classmethod
    def poll(cls, context):
        """Check if the active object is an armature."""
        return context.object is not None and context.object.type == "ARMATURE"

    @classmethod
    def description(cls, context, properties) -> str:
        # Dynamic description for the operator
        description_text = ""
        if context.object is None or context.object.type != "ARMATURE":
            return "No active armature found"
        if properties.custom_method == "ADD":
            description_text = (
                f"Add custom property to each bone in the active armature: "
                f"{properties.prop_name_format.format(armature=context.object.name, bone='', suffix=properties.suffix)}"
            )
        else:
            description_text = (
                f"Remove custom property from each bone in the active armature: "
                f"{properties.prop_name_format.format(armature=context.object.name, bone='', suffix=properties.suffix)}"
            )

        return description_text


def custom_prop_menu(self, context):
    """Add custom property menu to the object/armature/pose context menus."""
    if context.object is None or context.object.type != "ARMATURE":
        return
    layout = self.layout
    layout.operator_context = "INVOKE_DEFAULT"
    layout.operator(
        BLASTFRAME_OT_add_custom_bone_prop.bl_idname,
        text="Custom Bone Property",
        icon="BONE_DATA",
    )


def register():
    register_class(BLASTFRAME_OT_add_custom_bone_prop)
    bpy.types.VIEW3D_MT_pose_context_menu.append(custom_prop_menu)
    bpy.types.VIEW3D_MT_armature_context_menu.append(custom_prop_menu)
    bpy.types.VIEW3D_MT_object_context_menu.append(custom_prop_menu)


def unregister():
    bpy.types.VIEW3D_MT_object_context_menu.remove(custom_prop_menu)
    bpy.types.VIEW3D_MT_armature_context_menu.remove(custom_prop_menu)
    bpy.types.VIEW3D_MT_pose_context_menu.remove(custom_prop_menu)
    unregister_class(BLASTFRAME_OT_add_custom_bone_prop)


if __name__ == "__main__":
    register()
