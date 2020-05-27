# <img alt="BackPACK" src="./logo/backpack_logo_torch.svg" height="90"> BackPACK developer manual

## General standards 
- Python version: support 3.5+, use 3.7 for development
- `git` [branching model](https://nvie.com/posts/a-successful-git-branching-model/)
- Docstring style:  [Google](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)
- Test runner: [`pytest`](https://docs.pytest.org/en/latest/)
- Formatting: [`black`](https://black.readthedocs.io) ([`black` config](black.toml))
- Linting: [`flake8`](http://flake8.pycqa.org/) ([`flake8` config](.flake8))

---

The development tools are managed using [`make`](https://www.gnu.org/software/make/) as an interface ([`makefile`](makefile)). For an overview, call
```bash
make help 
```
  
## Suggested workflow with [Anaconda](https://docs.anaconda.com/anaconda/install/)
1. Clone the repository. Check out the `development` branch
```bash
git clone https://github.com/f-dangel/backpack.git ~/backpack
cd ~/backpack
git checkout development
```
2. Create `conda` environment `backpack` with the [environment file](.conda_env.yml). It comes with all dependencies installed, and BackPACK installed with the [--editable](http://codumentary.blogspot.com/2014/11/python-tip-of-year-pip-install-editable.html) option. Activate it.
```bash
make conda-env
conda activate backpack
```
3. Install the development dependencies and `pre-commit` hooks
```bash
make install-dev
```
4. **You're set up!** Here are some useful commands for developing
  - Run the tests
    ```bash
    make test
    ```
  - Lint code
    ```bash
    make flake8
    ```
  - Check format (code, imports, and docstrings)
    ```bash
    make format-check
    ```

## Documentation

### Build
- Use `make build-docs`
- To use the RTD theme, uncomment the line `html_theme = "sphinx_rtd_theme"` in `docs/rtd/conf.py` (this line needs to be uncommented for automatic deployment to RTD)

### View
- Go to `docs_src/rtd_output/html`, open `index.html`

### Edit
- Content in `docs_src/rtd/*.rst`
- Docstrings in code
- Examples in `examples/rtd_examples` (compiled automatically)


## Details

- Running quick/extensive tests: ([testing readme](test/readme.md))
- Continuous Integration (CI)/Quality Assurance (QA)
  - [`Travis`](https://travis-ci.org/f-dangel/backpack) ([`Travis` config](.travis.yaml))
    - Run tests: [`pytest`](https://docs.pytest.org/en/latest/)
    - Report test coverage: [`coveralls`](https://coveralls.io)
    - Run examples
  - [`Github workflows`](https://github.com/f-dangel/backpack/actions) ([config](.github/workflows))
    - Check code formatting: [`black`](https://black.readthedocs.io) ([`black` config](black.toml))
    - Lint code: [`flake8`](http://flake8.pycqa.org/) ([`flake8` config](.flake8))
    - Check docstring style: [`pydocstyle`](https://github.com/PyCQA/pydocstyle) ([`pydocstyle` config](.pydocstyle))
    - Check docstring description matches definition: [`darglint`](https://github.com/terrencepreilly/darglint) ([`darglint` config](.darglint))
- Optional [`pre-commit`](https://github.com/pre-commit/pre-commit) hooks [ `pre-commit` config ](.pre-commit-config.yaml)


## How to add new layers

- Step 1:
  - It is always advised to create a new branch before making changes to your forked version of backPACK. 
  - Make sure your forked repository is updated with the current version of backPACK. This repository changes dynamically and some of these changes are relevant to the entire framework. It is advised to `git pull upstream origin/branch-name` before making your own changes.
  - Once your new branch is ready and the repository is even with backPACK, run the tests to make sure everything is smooth.
  ```bash
    cd backpack
    make test
  ```
  - After the tests have passed, your forked version is even with backPACK and your new branch is ready, we can go to step 2.

- Step 2:
  - First step is to go through the documentation of parent classes listed below and identify the one your layer belongs to, i.e 
    - BaseDerivatives : `backpack/core/derivatives/basederivatives.py`
    - BaseParameterDerivatives : `backpack/core/derivatives/basederivatives.py`
    - BaseLossDerivatives : `backpack/core/derivatives/basederivatives.py`
    - ElementwiseDerivatives: `backpack/core/derivatives/elementwisederivatives.py`
  - It is advised to create a new file in the folder ` backpack/core/derivatives/` with the name of your layer and add your layer in that file.
  - Import all the necessary packages and create a child class which inherits the selected parent class. 
  - The first method which is necessary to implement is the `get_module()`, which returns your layer as a `torch.nn` module. 
  - Additionally, add this new layer class in `backpack/core/derivatives/__init__.py`. This is very important because this is how the layer is recognized by other backPACK modules and your new layer can be used. 

- Step 3:
  - This step varies for different parent classes. If your parent class is either of `BaseDerivatives, BaseParameterDerivatives, ElementwiseDerivatives`, it is compulsory to implement the method `df()` which is the first derivative of the layer. It is also necessary to indicate whether the second derivatives exist by setting the method `hessian_is_zero()` to True/False. If the second derivatives exist, implement the method in `d2f()`. 
  - The necessary step 3 for `BaseLossDerivatives` will be added shortly. 

- Step 4:
  - After adding the modules in your class from step 2 and step 3 it is crucial to check if the implementation is correct. For this purpose, we need to create some tests. Tests for activation function is explained here and the others are similar.
  ```bash
  cd test/core/derivatives/
  geddit activation_settings.py
  ```
  - There are different files containing test settings for different layer categories, namely: `activation/loss/layer/pooling_settings.py` and each of these contains an example and documentation regarding how to add tests for your own layer. 
  - Add your test accordingly and for each setting add `id_prefix: layer-name`, Eg: `id_prefix: softmax` (This step is optional and only for ease of testing).
  - After adding your test setting, run (from the above example):
  ```bash
  pytest -vx . -k "softmax"
  ```

- Step 5:
  - What if your test fails? These are some common and possible errors:
    - Check for the size of your tensor for the methods you have implemented. 
    - Re-check if the parent class is the correct one.
    - Check if the implementation of your derivatives is the correct one. 
    
###### _BackPACK is not endorsed by or affiliated with Facebook, Inc. PyTorch, the PyTorch logo and any related marks are trademarks of Facebook, Inc._
