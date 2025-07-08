# Add/Remove Custom Bone Properties (Blender Add-on)

This Blender add-on allows you to easily add or remove custom properties to every bone in the active armature. It supports a variety of property types and provides a flexible interface for customizing property names and values.

## Features

- Add or remove custom properties to all bones in the selected armature
- Supports property types: Integer, Float, Float Array, Integer Array, Boolean, Boolean Array, String
- Customizable property name format, separator, and suffix
- Set min/max/default values for numeric and array properties
- Integrated into the object context menu for easy access

## Installation

1. Download or clone this repository.
2. In Blender, go to **Edit > Preferences > Add-ons > Install**.
3. Select the `__init__.py` file from this repository.
4. Enable the add-on in the list.

## Usage

1. Select an armature object in Object, Pose, or Edit mode.
2. Right-click to open the context menu and choose **Add Custom Bone Property**.
3. Configure the property type, values, and naming options in the dialog.
4. Click **OK** to add or remove the custom property on all bones.

## Property Options

- **Property Type**: Choose the type of property to add (Int, Float, Array, etc.)
- **Min/Max/Default Values**: Set the range and default for numeric/array types
- **Method**: Add or Remove properties
- **Separator & Suffix**: Customize the property name
- **Property Name Format**: Use `{armature}`, `{bone}`, `{suffix}` tokens

## Example

Add an integer property named `Armature_Bone_TO` to all bones:

- Set Property Type: `Integer`
- Suffix: `TO`
- Property Name Format: `{armature}_{bone}_{suffix}`

## Uninstallation

1. Go to **Edit > Preferences > Add-ons**.
2. Search for "Add/Remove Custom Bone Properties".
3. Uncheck the box to disable or click **Remove** to uninstall.

## Author

Blastframe

## License

[MIT](LICENSE)
