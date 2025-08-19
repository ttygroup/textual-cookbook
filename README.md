# Textual-Cookbook

This repo contains a collection of examples and recipes for using the Textual framework to build terminal applications. Every example in this repository is runnable, and you can use them as a starting point for your own projects, or just learn how to do nifty things with Textual.

The examples are currently organized into the following categories:

- **Animation Effects**: Examples that demonstrate how to create various animation effects in Textual applications.
- **Architecture Patterns**: Examples that showcase different architectural patterns for building Textual applications.
- **Modifying Widgets**: Examples that show how to modify existing widgets or create new ones.
- **Styling and Colors**: Examples that demonstrate how to style Textual applications and use colors effectively.
- **Textual API Usage**: Examples that illustrate how to use the Textual API for various tasks.
- **Tips and Tricks**: A collection of miscellaneous examples that don't fit into the other categories.

All examples are tested with Nox against multiple verions of Textual (back to 1.0.0) in order to see how far back the examples work. Nearly all of them work all the way back to 1.0.0 with a few exceptions. To view the results of the tests, click the link below:

## [Textual Cookbook Test Results](https://ttygroup.github.io/textual-cookbook/reports/)

## Contributing / Submission Guide

Recipes can be submitted as pull requests. If you have a recipe that you would like to contribute, please follow these steps:

1. Fork the repository and clone it to your local machine.
2. Create your new recipe in the appropriate directory. It must be inside one of the category directories. If you think a new category is needed please open an issue.
3. Follow the recipe guidelines below when writing your recipe.
4. Test your recipe inside of the cookbook runner to ensure that it displays properly in the runner and the recipe works as expected.
5. Run Pytest (or Nox) to ensure your recipe passes the test on at least the latest version of Textual.
6. Submit a pull request.

You may also want to download the [`Just` command runner](https://just.systems/) to use the justfile.

## Recipe Guidelines

When writing a recipe, please follow these guidelines:

### **Docstring at the top** must follow this format

```python
"""This is the description of the recipe. Please write a description
that clearly explains what the recipe demonstrates. This description
can be as long or as short as you think is necessary. If it is very
long then the description screen will be scrollable. Some recipes
have short descriptions, some have descriptions that are several
paragraphs. This may be necessary if your recipe solves a complex
problem that requires explanation. The most important thing is
that it's obvious what this recipe does and what its purpose is.

This could be a second paragraph if you like, etc.

Recipe by Your Name Here"""
```

Note the `Recipe by Your Name Here` must not have anything else on the line, except for the triple quotes (""") at the end. The cookbook runner uses Regex to find this line and extract the author's name. If you do not follow this format, the cookbook runner will not be able to display your name correctly.

Optionally you can add extra info on the next line below your name and move the ending triple quotes to the next line, like this:

```python
"""This is the description of the recipe.

Recipe by Your Name Here
2025, https://your.website.here"""
```

### **Main guard** must be present and follow this format

It should look like this:

```python
if __name__ == "__main__":
    app = YourRecipeApp()
    app.run()
    sys.exit(app.return_code)
```

Note this requires importing `sys` at the top of your recipe file. The cookbook runner uses the exit code to know if a recipe failed or not, and provide an error message if one does. However, Textual does not return an exit code by default so we need to return it explicitly in the main guard using `sys.exit`.

Without this, if a recipe fails then the runner has no way of knowing. The recipe simply closes leaving the user wondering what happened. This isn't a huge deal for experienced Textual developers adding new recipes. However, the cookbook's intended audience is beginners and intermediate users who may be modifying existing recipes, or attempting to create their own. Without this error message, it may not be immediately obvious that their recipe has failed and that they can close the runner to view the traceback. If every recipe has this in the main guard, it means any recipe can be modified or copied as a starting point for a new recipe, and the user will always get an error message if something goes wrong.

### Type hints

Type hints are not required, but they are encouraged. I'm not going to be enforcing type strictness at all. But please do include them if you can.

MyPy and BasedPyright are included as dev dependencies and there's a shortcut to use them in the justfile. You can use it like this:

```bash
just typecheck category/my_recipe.py
```

And that's everything. Pytest will run in CI to ensure your recipe passes before it is merged. If you have any questions, feel free to open an issue or ask in the Textual Discord server.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
