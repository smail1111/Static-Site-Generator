# Static Site Generator

This is my fourth Boot.Dev project.

I will be building a static site generator that turns content files into static sites.

You can view an example site that this generator built at `https://smail1111.github.io/Static-Site-Generator/`

## How To Use

1. Clone Repository

`gh repo clone smail1111/Static-Site-Generator`

2. Update Static/Contents

In `static,` update the `index.css` file and add images you will use to the `images` directory.

Replace the content in the `content` directory with the content for the website you will host.

3. Host Locally

Run `./main.sh`

This will host your website at `https://localhost:8888/`

4. Host on Github

Create your own Github repository with the content from this repository.

Change the repository name in `./build.sh` to your exact Github repository name.

Run `./build.sh`

On your Github repository, go to `settings/pages` and deploy from the `main` branch and `./docs` directory.

This will host your website at `https:YourGithubName.github.io/YourRepositoryName/`
