# Custom Bone Property for Blender

Easily add or remove custom properties on bones in the active armature with this Blender add-on. Designed for riggers and technical artists, it provides a flexible interface for batch property management, supporting a wide range of property types and naming conventions.

**Selection behavior:**

- If the armature object is selected in Object mode, all bones will receive the custom property.
- In Pose mode, only the selected bones will receive the custom property.

## Features

- Add or remove custom properties on all (or selected) pose bones in the selected armature
- Supports Integer, Float, Boolean, String, and array property types
- Set min, max, and default values for numeric and array properties
- Customizable property name format, separator, and suffix
- Works in Object, Pose, and Edit modes
- Accessible from the right-click context menu in 3D Viewport (Object, Armature, and Pose modes)
- UI updates automatically after property changes

## Installation

1. Download or clone this repository.
2. In Blender, go to **Edit > Preferences > Add-ons > Install**.
3. Select the `__init__.py` file from this repository.
4. Enable the add-on in the Add-ons list.

## Usage

1. Select an armature object in Object, Pose, or Edit mode.
2. Right-click in the 3D Viewport and choose **Custom Bone Property** from the context menu.
3. In the dialog, choose the property type, method (Add/Remove), and configure values and naming options.
4. Click **OK** to apply the operation to all bones.

### Video Tutorial

For a quick demonstration of the add-on in action, watch the video below:
[![Custom Bone Property](https://img.youtube.com/vi/TUGGjXJURmU/0.jpg)](https://www.youtube.com/watch?v=TUGGjXJURmU)

### Property Options

- **Property Type**: Integer, Float, Boolean, String, Integer Array, Float Array, Boolean Array
- **Method**: Add or Remove properties
- **Min/Max/Default Values**: For numeric and array types
- **Separator & Suffix**: Customize property name formatting
- **Property Name Format**: Use `{armature}`, `{bone}`, `{suffix}` tokens for dynamic names

### Example

To add an integer property named `Armature_Bone_TO` to all bones:

- Set Property Type: `Integer`
- Suffix: `TO`
- Property Name Format: `{armature}_{bone}_{suffix}`

## Uninstallation

1. Go to **Edit > Preferences > Add-ons**.
2. Search for "Add/Remove Custom Bone Properties".
3. Uncheck the box to disable or click **Remove** to uninstall.

## Support

For questions or support, visit [Blastframe Contact](https://blastframe.com/contact/).

## Author

Blastframe

## Acknowledgements

- Special acknowledgement to [**Joel at SketchySquirrel**](https://www.youtube.com/c/SketchySquirrel) for the inspiration and idea behind this add-on, as well as for providing invaluable rigging insights to the Grease Pencil user base.
- For more details and projects, visit Joel's [GitHub](https://github.com/sketchy-squirrel) repository.

## License

This add-on is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
