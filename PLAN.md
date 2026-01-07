# App-Panel generator - initial plan for Copilot

## Goal
Generate app-panel.json automatically from .py files containing ArgParser or pydantic.BaseSettings classes that define parameters parsed from command line arguments.

## Approach
1. Accept a user-supplied file path for .py file to analyze, or discover a single file that defines argument parsing classes. If there are multiple (files or arg parsers), raise an error and request user to specify.
2. Parse the .py file and extract class definitions.
3. For each parsed argument, extract: name, type, optional default value, optional description. Only consider user-specified parameters (ie. exclude computed fields or properties).
4. Map Python field parameters to app-panel schema:
    - name -> name AND param_name
    - type -> value_type (float: number, int: integer, str: string, bool: integer)
    - default value -> default_value
    - description (from docstring or field info) -> description
    - "type" field in app-panel schema is always "text"
    - "id" field in app-panel schema is random chars, e.g. "gRSgqAsyqXsP70"
5. Determine whether an app-panel.json file already exists. If so, back it up with a timestamped filename. Merge the existing app-panel.json with the newly generated one, with a "strategy" option to either "overwrite" (default) or "preserve" existing fields. If overwriting fields, maintain the order of existing fields as much as possible, appending any new fields at the end.
6. Write the final app-panel.json file to disk at a specified path, or at the default /root/capsule/.codeocean/app-panel.json location.

## Interface
- while the above describes the internal logic, the user-facing interface will be a CLI command, e.g. `generate-app-panel --source /root/capsule/code/run.py --output /root/capsule/.codeocean/app-panel.json --strategy overwrite`

## Other implementation details
- use a modern CLI library such as Typer or Click to implement the command-line interface
- the tool should run in the same environment as the target .py file, to ensure availability of any imports used in the .py file, so the dependencies for this tool should be minimal (pydantic_settings may not need to be added explicitly, since it would necessarily be present in the target environment if used)
- the codeocean API could provide read-only metadata on existing app panel parameters, with the bonus of a complete schema, but would require authentication, so for simplicity just read the app-panel.json directly
- we can't edit the .codeocean file from a reproducible capsule run, so the CLI command should be run manually by the user in a cloud workstation terminal
- first concentrate on pydantic.BaseSettings as it's the primary use case
- make a Protocol or Abstract Base Class to define the interface for parameter extractors, allowing for future extension to other parsers e.g. ArgParser 