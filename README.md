# Using Ruff in Odoo projects
This project shows how to use Ruff as a styling and formater tool specially for Odoo projects.

## What's Ruff?
Ruff is an extremely fast Python linter and code formatter, written in Rust. The official documentation explains it better than me. So, here is the link: [Ruff](https://docs.astral.sh/ruff/)

## Can I use it in my Odoo projects?
Odoo uses Python and Ruff is a **Python linter** so, yes, you can use it in your Odoo projects and I will show you how to do it.

First, lets install Ruff using pip. You can create a `venv` and install it there if you don't want to mess with your global Python packages; but I like it so much that I will install it globally.
```bash
pip3 install ruff
```
If you are a Mac user, you can install it using Homebrew.
```bash
brew install ruff
```
In any case check if Ruff is installed correctly by running the following command.
```bash
ruff --version
```

## Testing in this project

First of all, clone this repo and checkout to `linter-issues` branch. Trust me blindly, I will explain you just below :)
```bash
git clone https://github.com/rejamen/odoo-ruff.git && cd odoo-ruff && git checkout linter-issues
```

Lets talk about the project structure and branches.

There are ywo branches:
- `main`: A branch without any code yet, only documentation.
- `linter-issues`: The branch I hope you are in. This will contain Python code that needs to be styled by Ruff. We have created a `pull request` to merge this branch into `main` because I want to show you a cool feature of Ruff with Github. Just wait for it.

The folder structure is very simple: 
- `README.md`: This file.
- `docs`: A folder with the documentation of this project.
- `addons`: A folder with the Odoo modules, divided in two subfolders:
  - `custom-addons`: the modules we develop.
  - `external-addons`: the modules we donwload from the Odoo Apps Store or from the Odoo Community GitHub, etc. Basically the addons we don't develop.
  
**Note**: Why I have separated the addons? Basically because we want to style only the ones we build, and most of the time we keep the external ones as they are. But you can style them too if you want. I will show you later how you can `exclude` some folders from the styling process. 

**Note:** What all the addons do (specially the ones inside custom-addons) is not relevant. Its just Python code with a lot of styling issues :)

So, lets try Ruff for the first time. I hope you are still in the branch `linter-issues`, in the root folder `odoo-ruff`
```bash
ruff check
```

Your console result should looks something like this image

![Ruff check](/docs/1.png)

This is nice, a little to much information, but nice. You can see:
- failing files, like `addons/custom-addons/custom_partner/__init__.py`
- error code, like `F401`, `F841`, etc.

Lets adjust the command to see a more compact output.
```bash
ruff check --output-format concise
```

And now you have a more concise output easier to read, like in this image:

![Ruff check concise](/docs/2.png)

**Note**: This is the complete list of available `output-format`. You can test now some of them. Later in this documentation we will use `github` to show you a cool feature.
* `concise`, `full`, `json`, `json-lines`, `junit`, `grouped`, `github`, `gitlab`, `pylint`, `rdjson`, `azure`, `sarif`

**Note**: Do you want to see all the issues in a file? Then use the `grouped` option. 

The previous command was executed in the root folder `odoo-ruff`. Therefore it checked all the addons including the external-addons, and we dont want to waste time styling what others did :D. Instead we will share this repo with them so they know how to fix it :D . Its a joke, lets just check our custom-addons. Don't worry, later we will add all this options in a configuration file, lets continue for now playing with the command line. 

```bash
ruff check addons/custom-addons --output-format concise 
```

This show now less issues, and only in the `custom_partner` and `custom_sale` modules, as you can see in this image:
![Ruff check custom addons](/docs/3.png)

Can we fix the issue now? Wait, no yet. Check this details. Run this command please and see the output.
```bash
ruff check addons/custom-addons/custom_partner/models/__init__.py --output-format concise 
```

It shows some issues in the `__init__.py` file. But wait, this is the `Odoo way` to import models. So it could be an issue for Ruff but not for Odoo developers.

![Ruff check init file](/docs/4.png)

Lets work on this point first. I want to say to Ruff that ignores the `__init__.py` files, because I know what I am doing :D. And now that we are excluding things, lets also exclude the `external-addons` folder.

For that, lets create a file called `pyproject.toml` in the root folder `odoo-ruff` and add the following content:
```toml
[tool.ruff]
exclude = [
    "addons/external-addons",
    "**/__init__.py",
]
output-format = "concise"

[tool.ruff.lint]
select = [
    "E",  # pycodestyle errors (PEP 8)
    "F",  # pyflakes errors (unused imports, etc.)
    "I",  # isort errors (import sorting)
    "C",  # Pylint convention violations
    "N",  # PEP 8 naming conventions
]
```
We added here:
- `exclude`: folders and files we want to exclude
- `output-format` to `concise`
- `select`: The list of issues we want to catch.

Now, we just run the following command, from the root folder `odoo-ruff` and just like that we dont have to pass any other option the the ruff check command
```bash
ruff check
```

Ok, now its time to fix our issues. Actually `ruff will do it for us`. Lets run the following command:
```bash
ruff check --fix
```

Which shows us that 10 errors were found, 7 were fixed and 3 are still remaining.

![Ruff check fix](/docs/5.png)

As you can image, Ruff can not fix all of them, but we have now a smaller list of files to check. If we are in the same page, you should manually fix:
- addons/custom-addons/custom_partner/models/res_partner.py:19:9: F841 Local variable `my_value` is assigned to but never used
- addons/custom-addons/custom_partner/models/res_partner.py:22:9: N802 Function name `incorrectNamingConvention` should be lowercase
- addons/custom-addons/custom_partner/models/res_users.py:15:89: E501 Line too long (162 > 88)

