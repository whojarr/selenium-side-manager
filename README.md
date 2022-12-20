# selenium-side-manager
Tools to work with Selenium IDE (SIDE) Project files

## docs/ide_setup/README.md

install instruction to setup the Selenim IDE browser plugin and open a side project.

## gitlab-runner

files used to setup a gitlab runner to run gitlab cicd calling the selenium-side-runner

## selenium_side_manager

main python module containing .side features


# Setup

```shell
poetry install
```

# Run

inside poetry
```shell
poetry shell

side-project-split some.side

side-projects-rebuild
```

from shell
```shell
poetry run side-project-split some.side

poetry run side-projects-rebuild
```