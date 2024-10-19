# Using Ruff as Linter and Formatter in Odoo Projects
This project shows how to use Ruff as a linter and formatter tool, specifically for Odoo projects.

## What's Ruff?
Ruff is an extremely fast Python linter and code formatter, written in Rust. The official documentation explains it better than I could, so here is the link: [Ruff](https://docs.astral.sh/ruff/)

## Can I use it in my Odoo projects?
**Yes you can**, and it's very simple. Continue reading to find out how.

First, let's install Ruff using pip. You can create a `venv` and install it there if you don't want to interfere with your global Python packages, but I won't do that.

Install it using pip3:
```bash
pip3 install ruff
```

Or, if you're a Mac user, you can install it using Homebrew:
```bash
brew install ruff
```

In either case, check if Ruff is installed correctly by running the following command:
```bash
ruff --version
```
**Note**: If you encounter any issues, you can refer to this section of the official documentation: [Ruff Installation](https://docs.astral.sh/ruff/installation/)

## Using this repo to test Ruff

First of all, clone this repo and check out the `linter-issues` branch. Trust me blindly, I will explain just below 😎
```bash
git clone https://github.com/rejamen/odoo-ruff.git && cd odoo-ruff && git checkout linter-issues
```

Let me first describe the project structure, regarding **files** and **branches**.

There are two **branches**:
- `main`: A branch without any code yet, only documentation.
- `linter-issues`: The branch I hope you are in. This branch contains Python code that needs to be styled by Ruff. I have created a `pull request` to merge this branch into `main` because I want to show you a cool feature of Ruff with GitHub 🚀. Just wait for it 🕐

The **folder structure** is very simple: 
- `README.md`: This file.
- `docs`: A folder with the documentation of this repo.
- `addons`: A folder with the Odoo modules, divided in two subfolders:
  - `custom-addons`: the modules we develop.
  - `external-addons`: The modules we download from the Odoo Apps Store or from other developers, etc. These are basically the addons we don't develop.
  
**Note**: 🤔 Why have I separated the addons folder? Basically, because I want to apply the linter only to the code I write. I'll keep the external addons as they were written by the authors. I will show you later how to exclude some folders from the styling process.

**Note:** What those addons in the repo do is not relevant. It's just Python code with a lot of styling issues 😁

So, let's try Ruff for the first time. I hope you're still on the **linter-issues** branch, in the root folder **odoo-ruff**.
```bash
ruff check
```

The result of this command is a list of linter issues found in your project, and it should look like this image: 

![Ruff check](/docs/1.png)

Basically from the output you can indetify:
- failing files, like `addons/custom-addons/custom_partner/__init__.py`
- error codes, like `F401`, `F841`, etc.

We can modify the previous command to show a more concise output. Just add the `--output-format concise` option.
```bash
ruff check --output-format concise
```

And now you have a simpler output, easier to read, like in this image:

![Ruff check concise](/docs/2.png)

**Note**: This is the complete list of available `--output-format` options. Test them and find the one you like the most. For me `concise` its enough. However, later in this documentation I will show you how to use a cool feature of Ruff when working with Github 😎
* `concise`, `full`, `json`, `json-lines`, `junit`, `grouped`, `github`, `gitlab`, `pylint`, `rdjson`, `azure`, `sarif`

The previous command was executed in the root folder `odoo-ruff`, and it checked all the addons, including the external-addons. As mentioned before, I don't want to do that. Let's modify the previous command to include only the folder I want to check. Don't worry, later we will add all these options in a **configuration file**; but for now, let's continue in the command line. 

```bash
ruff check addons/custom-addons --output-format concise 
```

Now, the terminal output shows fewer issues, and only in the `custom_partner` and `custom_sale` modules (the folders inside custom-addons, the ones we are interested in).
![Ruff check custom addons](/docs/3.png)

🤩 Can we fix the issues now? Wait, not yet. Let's check a final detail before we proceed. Please, run this command and see the output:
```bash
ruff check addons/custom-addons/custom_partner/models/__init__.py --output-format concise 
```

It shows some issues in the `__init__.py` file. But wait 🤔, this is the `Odoo way` to import models. It could be an issue for Ruff but not for Odoo developers 😅

![Ruff check init file](/docs/4.png)

I want to say Ruff to ignore those files because I know what I am doing 😄. Lets stop playing with the terminal and we better add a `config file`.

Create a file called `ruff.toml` in the root folder `odoo-ruff` and add the following content:
```toml
line-length = 88
preview = true
output-format = "concise"

[lint.per-file-ignores]
"__init__.py" = ["F401", "I001"]

[lint]
select = [
    "E",  # pycodestyle errors (PEP 8)
    "F",  # pyflakes errors (unused imports, etc.)
    "I",  # isort errors (import sorting)
    "C",  # Pylint convention violations
    "N",  # PEP 8 naming conventions
    "W",  # pycodestyle warnings. 
]
exclude = ["addons/external-addons/**"]
```

Now, we just run the following command, from the root folder `odoo-ruff` and just like that we dont have to pass any other option to the **ruff check** command
```bash
ruff check
```
**Note**: I found that the structure of the file is related to the `filename` and also to the `IDE` you are using. I am not 100% sure on this point, and I wasn't able to fully understand it. What I can ensure is that using `VS Code` and the `ruff.toml` filename works as described in this documentation.

### Let's fix the issues now 🚀
Ok, now its time to fix our issues. Actually `ruff will do it for us`. Lets run the following command:
```bash
ruff check --fix
```

Which shows us that ``23`` errors were found, `20` were fixed and `3` are still remaining.

![Ruff check fix](/docs/5.png)

As you can imagine, Ruff cannot fix all of them, but we now have a smaller list of files to check.  Now its your turn. Fix them until the `ruff check` command gives you a clean output `All checks passed!`.

## Cool feature with GitHub 🤩 🚀
Until here you should be able to detect and fix any linter issues with Ruff. But, what if we forget doing this before pushing our code to the repository? 🤔

Ruff can be integrated with Github defining a github action to run the linter with the options we just set. The output can be adjusted and Ruff structures its output so that GitHub Actions can display annotations directly in the pull request or code review interface. 
Find more details here: [Ruff GitHub Action](https://docs.astral.sh/ruff/integrations/#github-actions)

Create a new file called `ruff.yml` on the following path `odoo-ruff/.github/workflows/` and add the following content:
```yaml
name: CI
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install ruff
      # Update output format to enable automatic inline annotations.
      - name: Run Ruff
        run: ruff check --output-format=github .
```
After you create this file, just commit this change. I am assuming you are still in the `linter-issues` branch. If not, please checkout to it and commit the changes.
```bash
git add .github/workflows/ruff.yml && git commit -m "Add Ruff GitHub Action" && git push origin linter-issues
```