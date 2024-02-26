# [secret-garden](https://github.com/danielmuringe/secret-garden)
## A better way to manage your dotenv variables


### Installation
- You can use your most preferred package manager to install the package

    `pip install secret-garden` or `poetry add secret-garden` ...


## Table of Contents

1. [Usage](#usage)
    - [loading from a file](#load_file-function)
    - [loading from the environment namespace](#load_space-function)
    - [loading from a file using the environment namespace as an alternative](#load-function)

1. [Examples](#examples)
    - [Using a file](#using-a-file)
        - [env](#env)
        - [json](#json)
        - [toml](#toml)
        - [yaml](#yaml)
    - [Using the environment namespace](#using-the-environment-namespace)

1. [Objects](#objects)
    - [load](#load)
    - [load_file](#load_file)
    - [load_space](#load_space)

1. [Upcoming Features](#upcoming-features)


<h2 id="usage">Usage</h2>

You can put your variables in a file or use the environment namespace

<h3 id="load_file-function">Loading from a file</h3>

Create a file using one of the following formats and add your variables:

- `.env`
- `.json`
- `.yaml`
- `.toml`

    **Note: When using the `.env` file, the variables should be declared as python variables**
    

Use the `load_file` function to load the variables, specifying the format of the file

```python
from secret_garden import load_file
load_file('path/to/your/file', format_='<your_format>')
```

Pass the globals dictionary if you want to load the variables into the global namespace

```python
from secret_garden import load_file
load_file(
    'path/to/your/file',
    format_='<your_format>',
    globals_=globals()
)
```

<h3 id="load_space-function">Loading from the environment namespace</h3>

Add your variables into the environment namespace

```bash
export STR_VAR="string"
export INT_VAR=1
export FLOAT_VAR=1.0
export BOOL_VAR=True
export LIST_VAR="['item1', 'item2']"
export DICT_VAR="{'key1': 'value1', 'key2': 'value2'}"
```

Use the `load_space` function to load the variables

```python
from secret_garden import load_space
load_space(['STR_VAR', 'INT_VAR', 'FLOAT_VAR', 'BOOL_VAR', 'LIST_VAR', 'DICT_VAR'])
```

Pass the globals dictionary if you want to load the variables into the global namespace

```python
from secret_garden import load_space
load_space(
    ['STR_VAR', 'INT_VAR', 'FLOAT_VAR', 'BOOL_VAR', 'LIST_VAR', 'DICT_VAR'],
    globals_=globals()
)
```


<h3 id="load-function">Loading from a file using the environment namespace as an alternative</h3>

- This is done using the `load` function.

- If both path and include are provided, the variables are loaded from the file and the include argument is ignored.

    ```python
    from secret_garden import load
    load(
        "/path/to/your/file", # path to the file containing the variables
        ["VAR1", "VAR2"], # this will be ignored
        format_ = 'env',
        globals_ = None, 
    )
    ```

- If path does not exist, the variables are loaded from the environment namespace. The include argument is used to know which variables to get from the environment namespace.
    ```python
    from secret_garden import load
    load(
        "/path/to/the/non-existent/file", # path to the non-existent file
        ["VAR1", "VAR2"], # variables to be included from the environment namespace
        format_ = 'env',
        globals_ = None, 
    )
    ```

<h2 id="examples">Examples</h2>

<h3 id="using-a-file">Using a file</h3>

<h4 id="env">env</h4>

- Add your variables into the `.env` file

    ```python
    STR_VAR="string"
    INT_VAR=1
    FLOAT_VAR=1.0
    BOOL_VAR=True
    LIST_VAR=['item1', 'item2']
    DICT_VAR={'key1': 'value1', 'key2': 'value2'}
    ```

- Use the `load_file` function to load the variables

    ```python
    from secret_garden import load_file
    load_file('path/to/your/file.env', format_='env')
    ```

- Using the `globals_` parameter

    ```python
    from secret_garden import load_file
    load_file(
        'path/to/your/.env',
        format_='env',
        globals_=globals()
    )
    ```

<h4 id="json">json</h4>

- Add your variables into the `.json` file

    ```json
    {
        "STR_VAR": "string",
        "INT_VAR": 1,
        "FLOAT_VAR": 1.0,
        "BOOL_VAR": true,
        "LIST_VAR": ["item1", "item2"],
        "DICT_VAR": {"key1": "value1", "key2": "value2"}
    }
    ```

- Use the `load_file` function to load the variables

    ```python
    from secret_garden import load_file
    load_file('path/to/your/file.json', format_='json')
    ```

- Using the `globals_` parameter

    ```python
    from secret_garden import load_file
    load_file(
        'path/to/your/file.json',
        format_='json',
        globals_=globals()
    )
    ```

<h4 id="toml">toml</h4>

#####

- Add your variables into the `.toml` file

    ```toml
    STR_VAR = "string"
    INT_VAR = 1
    FLOAT_VAR = 1.0
    BOOL_VAR = true
    LIST_VAR = ["item1", "item2"]
    DICT_VAR = {key1 = "value1", key2 = "value2"}
    ```
- Use the `load_file` function to load the variables

    ```python
    from secret_garden import load_file
    load_file('path/to/your/file.toml', format_='toml')
    ```
- Using the `globals_` parameter

    ```python
    from secret_garden import load_file
    load_file(
        'path/to/your/file.toml',
        format_='toml',
        globals_=globals()
    )
    ```

<h4 id="yaml">yaml</h4>

#####

- Add your variables into the `.yaml` file

    ```yaml
    STR_VAR: string
    INT_VAR: 1
    FLOAT_VAR: 1.0
    BOOL_VAR: true
    LIST_VAR:
        - item1
        - item2
    DICT_VAR:
        key1: value1
        key2: value2
    ```

- Use the `load_file` function to load the variables

    ```python
    from secret_garden import load_file
    load_file('path/to/your/file.yaml', format_='yaml')
    ```

- Using the `globals_` parameter

    ```python
    from secret_garden import load_file
    load_file(
        'path/to/your/file.yaml',
        format_='yaml',
        globals_=globals()
    )
    ```

<h3 id="using-the-environment-namespace">Using the environment namespace</h3>

#####

- Add your variables into the environment namespace

    ```bash
    export STR_VAR="string"
    export INT_VAR=1
    export FLOAT_VAR=1.0
    export BOOL_VAR=True
    export LIST_VAR="['item1', 'item2']"
    export DICT_VAR="{'key1': 'value1', 'key2': 'value2'}"
    ```

- Use the `load_space` function to load the variables

    ```python
    from secret_garden import load_space
    load_space(['STR_VAR', 'INT_VAR', 'FLOAT_VAR', 'BOOL_VAR', 'LIST_VAR', 'DICT_VAR'])
    ```

- Using the `globals_` parameter

    ```python
    from secret_garden import load_space
    load_space(
        ['STR_VAR', 'INT_VAR', 'FLOAT_VAR', 'BOOL_VAR', 'LIST_VAR', 'DICT_VAR'],
        globals_=globals()
    )
    ```


<h2  id="objects">Objects</h2>

- <h3 id="load"><code>load</code></h3>

    ```python
    load(
        path_or_include: Path | PathLike | str | list[str], # path to the file or a list of variables to be included from the environment namespace
        format_: str = 'environ', # the format of the file if path_or_include is a path
        globals_: dict = None, # the execution global namespace to load the variables into
    )
    ```

    If both path and include are provided, the variables are loaded from the file and the include argument is ignored

    If path does not exist, the variables are loaded from the environment namespace and the include argument is used to filter the variables.


    - `path` (Path | PathLike | str): The path to the file containing the environment variables
    - `include` (list[str]): The variables to include when loading from the environment namespace
    - `format_` - Format of the file containing the variables.It can be one of the following:
        - 'env' - *Variables are declared as python variables*
        - 'environ' - *Variables are declared as environment variables where value are in quotes*
        - 'json'
        - 'yaml'
        - 'toml'
    - `globals_` - If not provided, variables will returned as a dictionary


- <h3 id="load_file"><code>load_file</code></h3>

    ```python
    load_file(
        path: str, # path to the file
        format_: str = 'environ', # the format of the file
        globals_: dict = None, # the execution global namespace to load the variables into
    )

    ```
    - `path` - The path to the file containing the variables
    - `format_` - Format of the file containing the variables.It can be one of the following:
        - 'env' - *Variables are declared as python variables*
        - 'json'
        - 'yaml'
        - 'toml'
    - `globals_` - If not provided, variables will returned as a dictionary

- <h3 id="load_space"><code>load_space</code></h3>

    ```python
    load_space(
        include: list, # a list of variables to be included from the environment namespace
        globals_: dict = None, # the execution global namespace to load the variables into
    )
    ```
    - `include` - A list of variables to be included from the environment namespace
    - `globals_` - If not provided, variables will returned as a dictionary


<h2 id="upcoming-features">Upcoming Features</h2>

- Support for multiline declaration in the `'env'` and `'environ'` formats

- Support for nested dictionary and list types in the `'env'` and `'environ'` formats
