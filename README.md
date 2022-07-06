# IForth

Forth kernel for the Jupyter / IPython notebook.  Requires IPython 3.x (master at the time of writing).

## Installation
1. Install [Gforth](https://www.gnu.org/software/gforth/).  Make sure it is accessible via the commandline/terminal (`gforth --version`).
2. Clone this repository and run `pip install .` inside this repository's folder (may require `sudo`, depending on Python location).    
   One sure way to avoid having to use `sudo` is to activate a virtual environment in your home directory (or wherever you have write access to).

### Development Installation
Do an [editable `pip` install](https://pip.pypa.io/en/stable/topics/local-project-installs/#editable-installs) - do `pip install -e .` (instead of `pip install .`)

## Usage
- Run `jupyter notebook` (or `ipython notebook`, whichever you prefer).
- In a new or existing notebook, use the kernel selector (located at the top right of the notebook) to select `IForth`.
