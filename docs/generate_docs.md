# Writing Docs

Docstrings are written using reStructuredText Docstring Format.

# Generating Docs

Install dependencies:
`pip install sphinx-autoapi sphinx_rtd_theme`

Go to the `sphinx-docs/` folder and run: `sphinx-build -b html . _build`

Open `_build/index.html`

# Generating Ukrainian Translation

Go to the `sphinx-docs/` folder and run: `sphinx-build -b html -D language='uk' . _build/uk`

Open `_build/uk/index.html`

# Updating Translation

Extract texts: `sphinx-build -b gettext . _build/gettext`

Refresh translation files: `sphinx-intl update -p _build/gettext -l uk`

Update any changed `index.po` files in `locale/` using `poedit`

e.g.
`poedit locale/uk/LC_MESSAGES/autoapi/audiobooksyncer/utils/index.po`
