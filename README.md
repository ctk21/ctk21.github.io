# Technical Notes

Technical Notes is a small Jekyll blog for Markdown-based writing on AI/ML, research and development, quantitative research, software, and engineering. GitHub Actions builds changes pushed to `main`, and GitHub Pages hosts the generated site.

## Prerequisites

The preferred environment is the included development container; it provides Ruby, Bundler, and Git. Outside the container, install equivalent versions of Ruby, Bundler, and Git before working with the site.

## Initial setup

From the repository root, install the locked dependencies:

```bash
bundle install
```

Commit `Gemfile.lock` when dependency resolution intentionally changes so local builds and CI remain aligned.

## Preview

Build the production site before committing content or configuration changes:

```bash
bundle exec jekyll build
```

Preview changes locally:

```bash
bundle exec jekyll serve
```

Visit <http://localhost:4000/>. Jekyll writes generated output to `_site/`; do not edit or commit that directory.

## Create a post

Create a portable Markdown file named:

```text
_posts/YYYY-MM-DD-post-title.md
```

Start with this front matter:

```yaml
---
layout: post
title: Post title
date: YYYY-MM-DD
description: One-sentence description.
tags:
  - example
---
```

Then add the article body below the front matter. Run `bundle exec jekyll serve` and review the post locally before committing it.

## Images

Store a post's images under:

```text
assets/images/<post-slug>/
```

Use the shared include in a post:

```liquid
{% include image.html
   src="/assets/images/example/image.jpg"
   alt="Descriptive alternative text"
   caption="Optional caption."
   width="500"
%}
```

`alt` describes the image. `caption` and `width` are optional. Images remain responsive at narrow widths.

## Publish

The normal workflow is: edit Markdown, add real image assets when needed, preview locally, review, commit, and push.

```bash
git status
git add .
git commit -m "Add article"
git push
```

Pushes to `main` automatically build and deploy the site. There is no separate deployment command and no `gh-pages` branch.


## Atom feed

Subscribe at <https://ctk21.github.io/feed.xml>. The feed regenerates automatically
on deployment when a new article is published under `_posts/`.

In the dev container, run `bundle exec jekyll serve --host 0.0.0.0`, forward port
4000, and visit <http://localhost:4000/>. Check the footer's **Atom feed** link,
open <http://localhost:4000/feed.xml>, and inspect the homepage source for
`type="application/atom+xml"`. Restart Jekyll after configuration changes.

For production validation, run these commands from the repository root
(requires Python 3):

```bash
bundle exec jekyll build
python3 scripts/validate_feed.py
```

The [validation script](scripts/validate_feed.py) checks XML syntax, the Atom
namespace, required metadata, author names, dates, unique entry IDs, and canonical
HTTPS article links in `_site/feed.xml`. It also checks the feed ID, self link,
and homepage link against their expected public URLs. It exits with a nonzero
status if a check fails.

The GitHub Pages build runs this validator before uploading the site artifact;
validation failures stop deployment.

Check that the feed includes the expected articles and absolute HTTPS entry
links. The `url` and `baseurl` in `_config.yml` must match the canonical deployed
site for correct links; local serve mode normally uses the preview origin.
After deployment, check the public feed URL and subscribe with a feed reader.


## GitHub Pages activation

After the repository is connected to GitHub, a repository administrator must enable the workflow deployment source once:

```text
Settings → Pages → Build and deployment → Source → GitHub Actions
```

After activation, inspect the Actions run after the next push to confirm that both the build and deployment jobs succeed. Then check the homepage, About page, article, stylesheet, and any image assets for obvious 404s.

## Site structure

```text
.
├── .github/workflows/pages.yml  # GitHub Pages deployment
├── _includes/                   # Reusable Liquid includes
├── _layouts/                    # Shared page and post layouts
├── _posts/                      # Dated Markdown articles
├── assets/
│   ├── css/                     # Site stylesheet
│   └── images/                  # Post images, added as needed
├── _config.yml                  # Jekyll configuration
├── Gemfile                      # Ruby dependencies
└── README.md                    # This guide
```
