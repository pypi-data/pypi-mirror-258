# Auto documentation <!-- omit in toc -->

Generate the markdown documentation (like Sphinx) to be used for vitepress, using GPT4.
It uses the OpenAI API to generate the documentation based on the docstrings of the code.

- [Usage](#usage)
- [Example](#example)
- [Distribution on pypi](#distribution-on-pypi)

## Usage

Install the package using pypi
```bash
pip install autopress
```

Configure the package. The OpenAI API key will be asked if not already set.

```bash
autodoc configure
```

The configure command will ask for the OpenAI API key and let you change the default prompt for the OpenAI API.

The commands can be listed using

```bash
autopress --help
```
```
Commands:
  Autopress.from_class      Use this method to generate a docstring from...
  Autopress.from_docstring  Use this method to generate a docstring from...
  Autopress.from_file       Open a markdown file and replace the tags...
  Autopress.from_method     Use this method to generate a docstring from...
  configure                 Set your configuration settings
```

The main command is `Autopress.from_file` which will replace the tags in the markdown file with the actual documentation. Go in the root of the package and run the following command:

```bash
cd demo
autopress Autopress.from_file --file README.md --output README_out.md
```

The above command will generate the documentation for the README.md file and save it in the README_out.md file.

## Example

The below tag will be replaced with the actual documentation of the method `convert_tag` from the module `autopress.utils`.

Before:
```markdown
<MethodAutopress module="autopress.utils" method="convert_tag" />
```

After:
```markdown 
<!--<MethodAutopress module="autopress.utils" method="convert_tag"  id="9d66f8"/>-->
<!--<AutoDoc.Content id="9d66f8">-->

### `autopress.utils.convert_tag`
Converts a tag to a docstring and replaces it in the content. This operation is useful when modifying file contents dynamically by substituting placeholders or tags with actual docstrings.

### Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `content` | `str` | | The content of the file. |
| `tag` | `str` | | The tag to convert. |
| `docstring` | `str` | | The docstring to replace the tag with. |
| `existing_id` | `re.Match` | | The existing ID of the tag. |

### Returns

| Type | Description |
|------|-------------|
| `str` | The content with the tag replaced by the docstring. |

<!--</AutoDoc.Content id="9d66f8">-->
```

You can excute again the command and the autpress will update the content.



## Distribution on pypi

> Make sure the version number is updated in the [__init__.py](autopress/__init__.py) file and in the [setup.py](setup.py) file.

The distribution on done with continuous integration using github actions. The secret `PYPI_API_TOKEN` is set in the repository settings.

Then, to trigger the release, we need to create a tag with the version number. The release will be automatically created and the package will be uploaded to pypi.

For example, to release version 1.0.0, we need to do the following:

```bash
git tag v1.0.0
git push origin v1.0.0
``` 

You can also create a release with a new tag in the github interface.