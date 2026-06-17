# Configuration file for the Sphinx documentation builder.
import importlib
import os
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Sequence, cast

from docutils import nodes
from docutils.nodes import Node
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives.misc import Include, adapt_path
from jinja2 import Environment, FileSystemLoader
from sphinx.application import Sphinx

# Read the Docs liefert uns die Canonical URL direkt!
html_baseurl = os.environ.get("READTHEDOCS_CANONICAL_URL", "")

# Falls wir lokal sind, ist die Variable leer, dann setzen wir einen Fallback
if not html_baseurl:
    html_baseurl = "/"


try:
    from ftwpki.ca_root_signer._version import __version__  # noqa: I001
    version = __version__ 
    release = __version__ 
except ImportError:
    version = '1.0'  # Fallback, damit ePub nicht meckert
    release = '1.0.0'

#SECTION - Custom Includes
#SECTION - Import Custom Includes





#!SECTION - Import Custom Includes
def person_role(name, rawtext, text, lineno, inliner, options=None, content=None):
    """
    Custom role for person names styled as small caps.

    :param name: The role name used in the document.
    :type name: str
    :param rawtext: The entire markup body.
    :type rawtext: str
    :param text: The argument of the role (the option name).
    :type text: str
    :param lineno: The line number where the role appears.
    :type lineno: int
    :param inliner: The inliner instance.
    :type inliner: docutils.parsers.rst.states.Inliner
    :param options: Directive options for customization.
    :type options: dict
    :param content: The directive content.
    :type content: list
    :return: A tuple containing a list of nodes and a list of system messages.
    :rtype: tuple[list[reference], list[Any]]
    """
    node = nodes.inline(rawtext, text, classes=["person"])
    return [node], []
class IncludeIfExists(Include):
    """
    A smart include guard directive.
    If the file exists, it is included with ALL provided options.
    If it doesn't exist, the document remains clean without errors.
    """

    def run(self) -> Sequence[Node]:
        path = directives.path(self.arguments[0])
        if path.startswith("<") and path.endswith(">"):
            path = "/" + path[1:-1]
            root_prefix = self.standard_include_path
        else:
            root_prefix = self.state.document.settings.root_prefix
        path = adapt_path(path, cast(str, self.state.document.current_source), root_prefix)
        exists: bool = Path(path).exists()
        if not exists:
            return []

        return super().run()


#SECTION - Register Custom Includes
def setup(app:Sphinx) -> None:
    """Register custom components during the Sphinx setup process."""
    app.add_role("person", person_role)
    app.add_directive("include-if-exists", IncludeIfExists)
#!SECTION - Register Custom Includes
#!SECTION - Custom Includes


#SECTION - Project information -----------------------------------------------------
project = "FTW PKI CA Root Signer"
copyright = "2026, Fitzz TeΧnik Welt"
author = "Fitzz TeΧnik Welt"
html_show_copyright = True
language = "en"
#!SECTION - Project information -----------------------------------------------------

#SECTION - General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",  # Zuerst die Basis
    "sphinx.ext.intersphinx",  # Wichtig für Cross-Refs
    "myst_parser",  # Falls du Markdown nutzt
    "sphinxarg.ext",  # Das "tote Pferd" erst jetzt laden
    "sphinx.ext.coverage",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinxcontrib.mermaid",
]


templates_path = ["_templates",]
exclude_patterns = []
maximum_signature_line_length= 120
toc_object_entries_show_parents='hide'
suppress_warnings=[
    'autosummary.import_cycle',
    'config.cache',
]

#!SECTION - General configuration ---------------------------------------------------



#SECTION - Options for HTML output -------------------------------------------------
html_theme = "sphinx_nefertiti"
html_theme_options = {
    "style": "indigo",
    "documentation_font_size": "1.2rem",
    "header_links": [
        {
            "text": "Index",
            "link": "genindex",
        },
        {
            "text": "List of Modules",
            "link": "py-modindex",
        },
    ],
    "logo": "ftw-initials.svg",
    "logo_height": 40,
    "logo_width": 40*1.2,
    "logo_location": "header",
    # "header_links_in_2nd_row": True,
    "project_name_font": "Fira Sans",
    "doc_headers_font": "Fira Sans",
    "documentation_font": "Fira Sans",
    "sans_serif_font": "Fira Sans",
    "monospace_font": "Fira Code",
}

html_static_path = ["_static"]
html_css_files = ["custom_nefertiti_html.css"]
toc_object_entries = True
toc_object_entries_show_parents = "hide"

#!SECTION - Options for HTML output -------------------------------------------------



#SECTION - Options for Intersphinx
intersphinx_mapping = {
    "python": (f"https://docs.python.org/{sys.version_info.major}.{sys.version_info.minor}", None),
}
#!SECTION - Options for Intersphinx

#SECTION - Options for ePub output -------------------------------------------------


def render_cover(
    programname: str, version: str, covertemplate: str = "cover.svg"
) -> tuple[str, str]:
    templates_dir = "_templates"
    static_dir = "_static"

    if not os.path.exists(static_dir):
        os.makedirs(static_dir)

    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template(covertemplate)

    # Rendern mit der echten 'release' Variable
    output_path = os.path.join(static_dir, covertemplate)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(template.render(version=version, programname=programname))
    return (output_path, "epub-cover.html")


if "epub" in sys.argv:
    epub_cover = render_cover("ftw-pki-caroot-signer", version.split("+")[0])


epub_theme = 'epub'
epub_basename = 'FTW_Development_Tools_Manual'
epub_title = project
epub_author = author
epub_publisher = author
# epub_identifier = 'https://github.com/ftwpki.client_server.git'
epub_scheme = 'URL'
epub_css_files = ['custom_epub.css']
# Fügt den Index und Modulindex zum internen Guide hinzu
epub_use_index = True  # Erlaubt die Generierung des Index
# Dies erzwingt die Aufnahme in das Inhaltsverzeichnis des Readers
epub_tocscope = 'default'
epub_tocdepth = 3

auto_exclude_files=[]
if "epub" in sys.argv:
    woff2_files = [str(file_) for file_ in Path().rglob("*.woff2")]
    fira_fonts= [str(file_) for file_ in Path().rglob("fira-*/*")]
    auto_exclude_files=list(set([*woff2_files,*fira_fonts]))


epub_exclude_files = [
    "_static/fonts/GUST-FONT-LICENSE.txt",
    "_static/fonts/OFL.md",
    "_static/fonts/OFL.txt",
    ".buildinfo.bak",
    *auto_exclude_files,
]

#!SECTION - Options for ePub output -------------------------------------------------

#SECTION - Options for Mermaid -----------------------------------------------------
# mermaid_use_local = "_static/mermaid.min.js"
#!SECTION - Options for Mermaid -----------------------------------------------------


#SECTION - Autodoc / Autosummary configuration -------------------------------------
#SECTION - Options for Autodoc
autodoc_typehints = "description"
autodoc_class_signature = "separated"
autodoc_typehints_description_target = "documented_params"
autodoc_default_options = {
    "members": True,
    'special-members': False,
    # 'private-members': "_ANSI,_color_map",
    #    'inherited-members': False,
    # 'undoc-members': True,
    "exclude-members": "__weakref__,__new__",
    "class-doc-from": "class",
}

if sys.version_info < (3, 14):
    autodoc_mock_imports = ["annotationlib"]
#!SECTION - Options for Autodoc

#SECTION - Function for Autosummary
def create_mermaid_decision_maker(whitelist:list[str]|None=None, 
                                  blacklist:list[str]|None=None) -> Callable[..., bool]:
    whitelist = whitelist or []
    blacklist = blacklist or []

    def should_render_mermaid(fullname):
        # 1. FAST RETURN: Blacklist (Geringste Kosten)
        # Wenn wir es explizit verboten haben, sofort raus.
        if fullname in blacklist:
            return False

        # 2. FAST RETURN: Whitelist (Geringe Kosten)
        # Wenn wir wissen, dass es gewollt/möglich ist, sofort ok.
        if fullname in whitelist:
            return True

        # 3. HEAVY LIFTING: Import & Analyse (Hohe Kosten)
        # Erst wenn die Listen keine Antwort liefern, werfen wir die Import-Maschine an.
        try:
            # Trennung von Modul und Attribut
            if "." not in fullname:
                return False

            module_name, class_name = fullname.rsplit(".", 1)
            module = importlib.import_module(module_name)
            obj = getattr(module, class_name)

            if isinstance(obj, type):
                # Technische Prüfung der Basisklassen
                return any(b.__name__ != "object" for b in obj.__bases__)

            return False
        except (ImportError, AttributeError, ValueError):
            return False

    return should_render_mermaid
# !SECTION - Function for Autosummary

#SECTION - Options for Autosummary 
autosummary_generate = True
autosummary_generate_overwrite = True
autosummary_imported_members = False
autosummary_ignore_module_all = True
autosummary_context = {}

inherit_diagramm: list[str] = []
exclude_inherit_diagramm: list[str] = []

class_extention_context = {
    "class_inc": "classinc",
    "module_inc": "moduleinc",
    "function_inc": "funcinc",
    "class_show_inheritance": True,
    "excl_class_show_inheritance": [
        "LineLike",
    ],
    "excl_class_show_inheritance_member": {
        "LineLike": [],
    },
    "include_private_members": {
        "LineLike": [
            "_color_map",
        ],
    },
    "autoclass_toc": True,
    "inheritence_diagram": create_mermaid_decision_maker(
        inherit_diagramm, exclude_inherit_diagramm
    ),
}

autosummary_context.update(class_extention_context)
#!SECTION - Options for Autosummary 

#!SECTION - Autodoc / Autosummary configuration -------------------------------------


#SECTION - Options for Documentationcoverage
coverage_statistics_to_stdout = True
coverage_show_missing_items = True
coverage_modules = [
    "ftwpki.ca_root_signer",
]

# NOTE - This list uses REGULAR EXPRESSIONS, not shell-style globs.
# Matches are performed against the Python dot notation of the modules.
# Remember to escape dots (e.g., '\.') if you want to match a literal dot.
coverage_ignore_modules = [
    r".*_version",
]
#!SECTION - Options for Documentationcoverage

#SECTION - Options for (Python) domain
add_module_names = False
python_display_short_literal_types = True
#!SECTION - Options for (Python) domain

if __name__ == "__main__":
    from typing import Any
    print("System Path:")
    print(sys.path)
    exclude=["os", "sys","Any","Callable", "Path" ]
    print("#"*10,"Summarized Configuration", "#"*10)
    loc=[x for x in locals().items() if x[0] not in exclude and not x[0].startswith("__")]
    def show_config(key:str, value:Any, indent:int=0) :
        indstr="    "*indent
        print(f"{indstr}{key}",end=": ")
        if isinstance(value, Callable):
            print(f"{value.__name__}() -> {value} from {value.__module__}")
        elif isinstance(value,list):
            if not value:
                print("[]")
            else:
                print("[")
                ind_bracket=indstr*2 if len(indstr) > 0 else "    "
                for list_v in value:
                    list_v = f"'{list_v}'" if isinstance(list_v, str) else list_v
                    if isinstance(list_v, dict):
                        print(f"{ind_bracket}{{")
                        for lk, lv in list_v.items():
                            show_config(lk,lv,indent +2)
                        print(f"{ind_bracket}}},")
                    else:
                        print(f"{ind_bracket}{list_v},")
                    
                print(f"{ind_bracket}]")
        elif isinstance(value, dict):
            ind_braces=indstr if len(indstr) > 0 else "    "
            print("{")
            d_list = [x for x in value.items()]
            for k1, v1 in d_list:
                show_config(k1,v1,indent +1)
            print(f"{ind_braces}}},")
            return
        elif isinstance(value, (str,int,float)):
            print(value)
        else:
            print(value)
        return

    for k,v in loc:
        show_config(k,v)
