# Developer

This guide helps you get started developing Media Market Generating API

## Dependencies

Make sure you have the following dependecies installed before setting up your devloper environmnent:


- [Git](https://git-scm.com/)
- [Docker Engine](https://docs.docker.com/engine/install/) On Windows you can either install it through WSL or Docker Desktop
- [Docker Compose](https://docs.docker.com/compose/)

Optional, but highly recommended:
- [uv](https://docs.astral.sh/uv/getting-started/installation/)


## Download Media Marketing Generating API

We recommend using the Git command-line interface to download the source code for API project:

1. Open a terminal and run `git clone https://github.com/Ivareh/media-marketing-gen-api.git`. This command downloads the API to a new `media-marketing-gen-api` directory in your current directory. Open a terminal and run `git clone https://github.com/Ivareh/media-marketing-gen-api.git`. This command downloads the API to a new `media-marketing-gen-api` directory in your current directory.
1. Open the `media-marketing-gen-api` directory in your favorite code editor.

For alternative ways of cloning this repository, refer to [GitHub's documentation](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository).


### Configure precommit hooks

We use [pre-commit](https://pre-commit.com/) hooks to lint, fix, and format code as you commit your changes.

You can find a file `.pre-commit-config.yaml` with configurations at the root of the project.


#### Install pre-commit to run automatically

`pre-commit` is already part of the dependencies of the project, but you could also install it globally if you prefer to, following the [official pre-commit docs](https://pre-commit.com/#usage).

After having the pre-commit tool installed and available, you need to "install" it in the local repository, so that it runs automatically before each commit.


Using `uv`, you could do it with:

```sh
uv run pre-commit install
```

Now whenever you try to commit, e.g. with:

```sh
git commit
```

...pre-commit will run and check and format the code you are about to commit, and will ask you to add that code (stage it) with git again before committing.

Then you can git add the modified/fixed files again and now you can commit.


#### Run pre-commit hooks manually

You can also run `pre-commit` manually on all the files, you can do it using `uv` with:

```sh
uv run pre-commit run --all-files
```


## Docker Compose

- Start the local stack with Docker Compose:

```sh
docker compose watch
```

- Now you can open your browser and interact with these URL:

Backend, based on OpenAPI: [http://localhost:8000/](http://localhost:8000/)

Traefik UI, to see the routes being handled by the proxy: [http://localhost:8090/](http://localhost:8090/)



## The .env file

The `.env` file is the one that contains all your configurations, generated keys and passwords, etc.


### Configure Azure Authentication


Please refer to [Azure Setup](https://intility.github.io/fastapi-azure-auth/multi-tenant/azure_setup) to setup your Azure app registrations for this API.


Note the two variables `Application (Client) ID` for the Backend API and OpenAPI Documentation. Insert them in the `.env` file to `APP_CLIENT_ID` and `OPENAPI_CLIENT_ID` respectively.



