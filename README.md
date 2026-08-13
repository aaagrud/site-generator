# Static Site Generator

A static site generator built in Python that converts Markdown content into a fully linked static HTML website, complete with images, CSS, and nested pages (e.g. blog posts).

[Demo generated site](https://aaagrud.github.io/site-generator/)

(from `/contents` and `/static` in this repo)

## Stack

- Python 3
- Standard library only (`sys`, `os`, `pathlib`, `shutil`, etc.)
- No third-party dependencies

## Setup
```
git clone https://github.com/aaagrud/site-generator.git
cd site-generator
```

No installation needed beyond Python 3 itself. There are no external packages to install.

## How to Use Locally

Run the following from the project root:
 
 `./main.sh`

This starts a local HTTP server and serves your generated site at `http://localhost:8888`. 
The default basepath for local development is `/`.

Place your Markdown content (organized into folders per page) inside `/content`, and your static assets (CSS, images) inside `/static`. 
The generator will process content from `/content`, apply `template.html`, and copy static assets automatically.

## How to Build and Deploy to GitHub Pages
Run the following from the project root:
 
 `./build.sh`

This builds the site using a basepath matching your repository name (e.g. `/site-generator/`) instead of `/`, so that internal links and asset paths resolve correctly once hosted on GitHub Pages. Output is generated into `/docs`.

To deploy:
1. Commit and push the generated `/docs` directory to your `main` branch.
2. In your repository settings on GitHub, go to **Pages** (under Code and automation).
3. Set the source to the `main` branch and `/docs` folder.
4. Save. GitHub Pages will auto-deploy from `/docs` on every push to `main`.

Your live site will be available at:

https://USERNAME.github.io/site-generator/

## Repo Structure

- `src/` — All source code for the static site generator (Markdown parsing, HTML conversion, page generation logic).
- `content/` — Your Markdown files, organized into folders that mirror your desired website paths (e.g. `content/blog/my-post/index.md` becomes `/blog/my-post`).
- `static/` — Static assets (CSS, images), organized into folders as needed. These are copied as-is into the output directory.
- `docs/` — The generated output. This is what gets served locally and deployed via GitHub Pages. Do not edit files here directly, they're overwritten on every build.
- `template.html` — The base HTML template. Content and title placeholders in this file get replaced with your generated Markdown content during the build process.
<sup><sub>Built to practice python! AI didn't write the code, I did</sub></sup>
