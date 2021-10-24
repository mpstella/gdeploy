# Gcloud Wrapper

This is a wrapper specifically to help with our CI/CD deployments and gcloud functions.

It uses the [typer](https://github.com/tiangolo/typer) as the CLI and can be easily extended to add future functionality.

### General Help
```text
$> vcdibuildutils --help
Usage: vcdibuildutils [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  auth       This is an example that does a `gcloud auth list`
  functions  Wrapper for `gcloud functions`
  version    Print the current version
```

### Subcommand Help
```text
$> vcdibuildutils functions --help
Usage: vcdibuildutils functions [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  deploy
  list
```

### Detailed Help
```text
$> vcdibuildutils functions deploy --help
Usage: vcdibuildutils functions deploy [OPTIONS]

  Wrapper around `gcloud functions deploy`

  Args:     config (Path): The path to the configuration file     source
  (Path): The path to the source code to deploy

Options:
  --config FILE       Path to Jsonnet/JSON configuration file  [env var:
                      CONFIG_PATH; required]
  --source DIRECTORY  Path to the function source code  [env var: SOURCE_PATH;
                      default: src]
  --help              Show this message and exit.
```
---
## Deploying GCP Functions

This will wrap [`gcloud functions deploy`](https://cloud.google.com/sdk/gcloud/reference/functions/deploy) by passing all the parameters from a configuration file ([jsonnet](https://jsonnet.org/))

#### Command line examples
```text
$> # using environment variables
$> export CONFIG_PATH=/path/to/config.jsonnet
$> export SOURCE_PATH=/path/to/source

$> vcdibuildutils functions deploy
```

```text
$> # defaulting source to local `src` directory
$> vcdibuildutils functions deploy --config /path/to/config.jsonnet

$> # complete command line
$> vcdibuildutils functions deploy --config /path/to/config.jsonnet --source /path/to/source
```

#### Jsonnet configuration file:

Essentially the configuration file must have the following fields defined (unless not required)

|key  |description                       |required?|
|-----|----------------------------------|---------|
|name |the name of the function to deploy| Yes     |
|args |key/value pair of options         | Yes     |
|flags|flags to pass to gcloud           | Yes     |
|opts |either `alpha` or `beta`          | No      |

#### example: 

```jsonnet
local functionName = "hello-world";

{
  "name": functionName,
  "args": {
      "region": "australia-southeast1",
      "entry-point": "hello_http",
      "runtime": "python39",
      "update-labels": {
        "deployed_by": "gdeploy",
        "deployed_on": "yyyy-mm-dd"
      },
      "remove-labels": [
        "label1",
        "label2"
      ]
  },
  "flags": [
    "allow-unauthenticated",
    "trigger-http"
  ],
  "opts": ["alpha"]
}
```