"""Command-line interface options for the readme-ai application."""

from __future__ import annotations

from typing import Optional

import click

from readmeai.config.enums import BadgeOptions, ImageOptions, ModelOptions


def prompt_for_image(
    context: Optional[click.Context],
    parameter: Optional[click.Parameter],
    value: Optional[str],
) -> str:
    """Prompt the user for a custom image URL."""
    if value == ImageOptions.CUSTOM.name:
        return click.prompt("Provide an image file path or URL")
    elif value == ImageOptions.LLM.name:
        ...
    elif value in ImageOptions.__members__:
        return ImageOptions[value].value
    else:
        raise click.BadParameter(f"Invalid image path entered: {value}")


alignment = click.option(
    "-a",
    "--alignment",
    type=click.Choice(["center", "left"], case_sensitive=False),
    default="center",
    help="Align the text in the README.md file's header to the left or center.",
)

api = click.option(
    "--api",
    type=click.Choice(
        [opt.value for opt in ModelOptions], case_sensitive=False
    ),
    default=None,
    help="""LLM service to use for generating the README.md file. The following options are currently supported:\n

    - OFFLINE (Generate the README.md file without making any API calls) \n
    - OLLAMA (Ollama LLM) \n
    - OPENAI (OpenAI GPT-3.5) \n
    - VERTEX (Google Vertex AI) \n
    """,
)

badge_color = click.option(
    "--badge-color",
    type=str,
    default="0080ff",
    help="Custom color for the badge icon. Provide a valid color name or hex code.",
)

badge_style = click.option(
    "--badge-style",
    type=click.Choice(
        [opt.value for opt in BadgeOptions], case_sensitive=False
    ),
    default=BadgeOptions.DEFAULT.value,
    help="""\
        Badge icon style types to select from when generating README.md badges. The following options are currently available:\n
        - default \n
        - flat \n
        - flat-square \n
        - for-the-badge \n
        - plastic \n
        - skills \n
        - skills-light \n
        - social \n
        """,
)

emojis = click.option(
    "-e",
    "--emojis",
    is_flag=True,
    default=False,
    help="This option adds emojis to the README.md file's header sections. For example, the default header for the 'Overview' section generates the markdown code as '## Overview'. Adding the --emojis flag generates the markdown code as '## 📍 Overview'.",
)

image = click.option(
    "-i",
    "--image",
    type=click.Choice(
        [opt.name for opt in ImageOptions], case_sensitive=False
    ),
    default=ImageOptions.BLUE.name,
    callback=prompt_for_image,
    show_choices=True,
    help="""\
        Project logo image displayed in the README file header. The following options are currently supported:\n

        Custom image options:\n
        - CUSTOM (use a custom image file path or URL) \n
        - LLM (use LLM multi-modal capabilities to generate an image) \n

        Default image options:\n
        - BLACK \n
        - BLUE \n
        - CLOUD \n
        - GRADIENT \n
        - GREY \n
        - PURPLE \n
        """,
)

language = click.option(
    "-l",
    "--language",
    default="en",
    help="Language to use for generating the README.md file. Default is English (en).",
)

max_tokens = click.option(
    "--max-tokens",
    default=3999,
    type=int,
    help="Maximum number of tokens to generate for each section of the README.md file.",
)

model = click.option(
    "-m",
    "--model",
    default="gpt-3.5-turbo",
    help="GPT language model to use for generating various sections of the README.md file.",
)

output = click.option(
    "-o",
    "--output",
    default="readme-ai.md",
    help="Output file name for your README file. Default name is 'readme-ai.md'.",
)

repository = click.option(
    "-r",
    "--repository",
    required=True,
    help="Provide a remote repository URL (GitHub, GitLab, BitBucket), or a local directory path to your project.",
)

temperature = click.option(
    "-t",
    "--temperature",
    default=0.9,
    type=click.FloatRange(0.0, 2.0, clamp=True),
    help="Setting the model's temperature to a higher value will yield more creative content generated, while a lower value will generate more predictable content.",
)

template = click.option(
    "--template",
    type=str,
    help="README template file to use for generating the README.md file.",
)

tree_depth = click.option(
    "--tree-depth",
    default=3,
    type=int,
    help="Maximum depth of the directory tree thats included in the README.md file.",
)
