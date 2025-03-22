"""CLI tool for converting FontAwesome icons to PNG."""

import os
import sys
from pathlib import Path
from typing import Optional

import click
from loguru import logger
from tqdm import tqdm
from .converter import FontAwesomeConverter

@click.group()
@click.option('--log-level', 
              type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], case_sensitive=False),
              default='INFO',
              help='Set the logging level')
@click.pass_context
def cli(ctx, log_level):
    """Convert FontAwesome icons to PNG format."""
    # Store log level in context for subcommands to use
    ctx.ensure_object(dict)
    ctx.obj['LOG_LEVEL'] = log_level.upper()


@cli.command()
@click.argument('icon_name')
@click.argument('fa_path', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('--style', type=click.Choice(['solid', 'regular', 'brands']), default='solid',
              help='Icon style (solid, regular, or brands)')
@click.option('--size', type=int, default=512, help='Output size in pixels')
@click.option('--color', help='Color for the icon (as hex code, e.g. "#FF0000")')
@click.option('--render-method', type=click.Choice(['svg', 'font']), default='svg',
              help='Method to use for rendering (svg or font)')
@click.option('--output-dir', type=click.Path(file_okay=False), default='output',
              help='Directory to save the output')
@click.pass_context
def convert(
    ctx,
    icon_name: str,
    fa_path: str,
    style: str,
    size: int,
    color: Optional[str],
    render_method: str,
    output_dir: str
):
    """
    Convert a single FontAwesome icon to PNG.
    
    ICON_NAME is the name of the icon to convert (e.g. 'arrow-right').
    
    FA_PATH is the path to the extracted FontAwesome files.
    """
    # Create converter with log level from context
    converter = FontAwesomeConverter(fa_path, log_level=ctx.obj['LOG_LEVEL'])
    
    if render_method == 'svg':
        output_files = converter.convert_svg(
            icon_name, 
            style=style, 
            size=size, 
            color=color, 
            output_dir=output_dir
        )
    else:
        output_files = converter.convert_font(
            icon_name, 
            style=style, 
            size=size, 
            color=color or "#000000", 
            output_dir=output_dir
        )
        
    if output_files:
        click.echo(f"Icon converted successfully: {len(output_files)} files created")
        if ctx.obj['LOG_LEVEL'] == 'DEBUG':
            for file in output_files:
                click.echo(f"  - {file}")
    else:
        click.echo("Failed to convert icon.", err=True)
        sys.exit(1)


@cli.command()
@click.argument('fa_path', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('--style', type=click.Choice(['solid', 'regular', 'brands']),
              help='Filter by icon style (solid, regular, or brands)')
@click.option('--size', type=int, default=512, help='Output size in pixels')
@click.option('--color', help='Color for the icon (as hex code, e.g. "#FF0000")')
@click.option('--render-method', type=click.Choice(['svg', 'font']), default='svg',
              help='Method to use for rendering (svg or font)')
@click.option('--output-dir', type=click.Path(file_okay=False), default='output',
              help='Directory to save the outputs')
@click.pass_context
def convert_all(
    ctx,
    fa_path: str,
    style: Optional[str],
    size: int,
    color: Optional[str],
    render_method: str,
    output_dir: str
):
    """
    Convert all FontAwesome icons to PNG.
    
    FA_PATH is the path to the extracted FontAwesome files.
    """
    # Create converter with log level from context
    converter = FontAwesomeConverter(fa_path, log_level=ctx.obj['LOG_LEVEL'])
    
    output_files = converter.convert_all(
        style=style, 
        size=size, 
        color=color, 
        render_method=render_method, 
        output_dir=output_dir
    )
    
    if output_files:
        # Display organization information
        sizes = converter._get_sizes_to_generate(size)
        click.echo(f"Successfully converted {len(output_files)} icons to {output_dir}")
        click.echo(f"Icons organized in {len(sizes)} subdirectories by size: {', '.join([f'{s}px' for s in sizes])}")
    else:
        click.echo("No icons were converted.", err=True)
        sys.exit(1)


if __name__ == '__main__':
    cli(obj={}) 