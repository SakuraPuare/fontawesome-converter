"""Main converter module for FontAwesome to PNG conversion."""

import json
import os
from pathlib import Path
from typing import Dict, List, Literal, Optional, Tuple, Union

import cairosvg
from loguru import logger
from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm

class FontAwesomeConverter:
    """Convert FontAwesome icons to PNG format."""

    def __init__(self, fa_path: str, log_level: str = "INFO"):
        """
        Initialize the converter.
        
        Args:
            fa_path: Path to the extracted FontAwesome files
            log_level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self.fa_path = Path(fa_path)
        self.metadata_path = self.fa_path / "metadata" / "icons.json"
        self.svg_path = self.fa_path / "svgs"
        self.webfonts_path = self.fa_path / "webfonts"
        
        # Set logger level
        self.set_log_level(log_level)
        
        # Check if we have a desktop or web package
        if not self.webfonts_path.exists():
            self.webfonts_path = self.fa_path / "otfs"
            
        # Load icon metadata
        with open(self.metadata_path, 'r', encoding='utf-8') as f:
            self.icons_data = json.load(f)
            
        logger.info(f"Loaded {len(self.icons_data)} icons from metadata")
        
        # Default size presets
        self.default_sizes = [16, 24, 32, 48, 64, 128, 256, 512]
        
    def set_log_level(self, level: str):
        """
        Set the logger level.
        
        Args:
            level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        logger.remove()  # Remove default handler
        logger.add(
            sink=lambda msg: tqdm.write(msg, end=""), 
            level=level,
            colorize=True
        )
        
    def convert_svg(
        self, 
        icon_name: str, 
        style: Literal["solid", "regular", "brands"] = "solid", 
        size: Union[int, List[int]] = 512, 
        color: Optional[str] = None, 
        output_dir: str = "output",
        organize_by_size: bool = True,
        organize_by_color: bool = True,
        organize_by_style: bool = True
    ) -> List[str]:
        """
        Convert an SVG icon to PNG using direct SVG rendering.
        
        Args:
            icon_name: The name of the icon to convert
            style: Icon style (solid, regular, or brands)
            size: Output size in pixels or list of sizes (max size if single value)
            color: Color for the icon (as hex code)
            output_dir: Directory to save the output
            organize_by_size: Whether to organize output files by size in subdirectories
            organize_by_color: Whether to organize output files by color in subdirectories
            organize_by_style: Whether to organize output files by style (solid/regular/brands) in subdirectories
            
        Returns:
            List of paths to the generated PNG files
        """
        output_files = []
        
        # Check if icon exists
        if icon_name not in self.icons_data:
            logger.error(f"Icon '{icon_name}' not found in metadata")
            return output_files
            
        # Check if requested style is available
        icon_info = self.icons_data[icon_name]
        if style not in icon_info.get("styles", []):
            available_styles = ", ".join(icon_info.get("styles", []))
            logger.error(f"Style '{style}' not available for '{icon_name}'. Available: {available_styles}")
            return output_files
            
        # Create output directory if it doesn't exist
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Find SVG file
        svg_file = self.svg_path / style / f"{icon_name}.svg"
        if not svg_file.exists():
            logger.error(f"SVG file for '{icon_name}' ({style}) not found at {svg_file}")
            return output_files
            
        # Determine sizes to generate
        sizes_to_generate = self._get_sizes_to_generate(size)
        
        # Log icon processing at INFO level
        logger.info(f"Converting '{icon_name}' ({style}) to PNG using SVG rendering")
        
        # Normalize color for directory name if needed
        color_dirname = "default" if not color else color.replace("#", "")
        
        # Convert SVG file to PNG at each requested size
        for current_size in sizes_to_generate:
            # Determine the output directory based on organization options
            current_output_dir = output_dir
            
            # Organization order: style -> color -> size
            # Organize by style if requested
            if organize_by_style:
                style_dir = current_output_dir / style
                style_dir.mkdir(parents=True, exist_ok=True)
                current_output_dir = style_dir
                
            # Organize by color if requested
            if organize_by_color:
                color_dir = current_output_dir / color_dirname
                color_dir.mkdir(parents=True, exist_ok=True)
                current_output_dir = color_dir
                
            # Organize by size if requested
            if organize_by_size:
                size_dir = current_output_dir / f"{current_size}px"
                size_dir.mkdir(parents=True, exist_ok=True)
                current_output_dir = size_dir
                
            # Generate output file path
            filename_parts = [icon_name]
            if not organize_by_style:
                filename_parts.append(style)
            if not organize_by_size:
                filename_parts.append(f"{current_size}")
            if not organize_by_color and color:
                filename_parts.append(color_dirname)
            
            output_file = current_output_dir / f"{'_'.join(filename_parts)}.png"
            
            # Convert SVG to PNG
            if color:
                # If color is specified, we need to modify the SVG content
                with open(svg_file, 'r', encoding='utf-8') as f:
                    svg_content = f.read()
                    
                # Replace fill color in SVG
                if 'fill=' not in svg_content:
                    # Add fill attribute to the first path element
                    svg_content = svg_content.replace('<path ', f'<path fill="{color}" ')
                else:
                    # Replace existing fill attribute
                    svg_content = svg_content.replace('fill="currentColor"', f'fill="{color}"')
                    svg_content = svg_content.replace('fill="#', f'fill="{color}" fill-old="#')
                    
                # Convert modified SVG to PNG
                cairosvg.svg2png(bytestring=svg_content.encode('utf-8'), 
                                write_to=str(output_file),
                                output_width=current_size,
                                output_height=current_size)
            else:
                # Convert original SVG to PNG
                cairosvg.svg2png(url=str(svg_file), 
                                write_to=str(output_file),
                                output_width=current_size,
                                output_height=current_size)
                
            logger.debug(f"Created '{icon_name}' ({style}) at size {current_size}px: {output_file}")
            output_files.append(str(output_file))
            
        return output_files
        
    def convert_font(
        self, 
        icon_name: str, 
        style: Literal["solid", "regular", "brands"] = "solid", 
        size: Union[int, List[int]] = 512, 
        color: str = "#000000", 
        output_dir: str = "output",
        organize_by_size: bool = True,
        organize_by_color: bool = True,
        organize_by_style: bool = True
    ) -> List[str]:
        """
        Convert an icon to PNG using font rendering.
        
        Args:
            icon_name: The name of the icon to convert
            style: Icon style (solid, regular, or brands)
            size: Output size in pixels or list of sizes (max size if single value)
            color: Color for the icon (as hex code)
            output_dir: Directory to save the output
            organize_by_size: Whether to organize output files by size in subdirectories
            organize_by_color: Whether to organize output files by color in subdirectories
            organize_by_style: Whether to organize output files by style (solid/regular/brands) in subdirectories
            
        Returns:
            List of paths to the generated PNG files
        """
        output_files = []
        
        # Check if icon exists
        if icon_name not in self.icons_data:
            logger.error(f"Icon '{icon_name}' not found in metadata")
            return output_files
            
        # Check if requested style is available
        icon_info = self.icons_data[icon_name]
        if style not in icon_info.get("styles", []):
            available_styles = ", ".join(icon_info.get("styles", []))
            logger.error(f"Style '{style}' not available for '{icon_name}'. Available: {available_styles}")
            return output_files
            
        # Create output directory if it doesn't exist
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Map style to font file
        font_file_map = {
            "solid": "fa-solid-900.ttf",
            "regular": "fa-regular-400.ttf",
            "brands": "fa-brands-400.ttf"
        }
        
        font_file = self.webfonts_path / font_file_map.get(style, "fa-solid-900.ttf")
        if not font_file.exists():
            logger.error(f"Font file not found: {font_file}")
            return output_files
            
        # Get unicode value for the icon
        unicode_hex = icon_info.get("unicode")
        if not unicode_hex:
            logger.error(f"Unicode value not found for '{icon_name}'")
            return output_files
            
        # Convert hex to Unicode character
        unicode_char = chr(int(unicode_hex, 16))
        
        # Determine sizes to generate
        sizes_to_generate = self._get_sizes_to_generate(size)
        
        # Log icon processing at INFO level
        logger.info(f"Converting '{icon_name}' ({style}) to PNG using font rendering")
        
        # Normalize color for directory name
        color_dirname = color.replace("#", "")
        
        # Create images of each requested size
        for current_size in sizes_to_generate:
            try:
                # Determine the output directory based on organization options
                current_output_dir = output_dir
                
                # Organization order: style -> color -> size
                # Organize by style if requested
                if organize_by_style:
                    style_dir = current_output_dir / style
                    style_dir.mkdir(parents=True, exist_ok=True)
                    current_output_dir = style_dir
                    
                # Organize by color if requested
                if organize_by_color:
                    color_dir = current_output_dir / color_dirname
                    color_dir.mkdir(parents=True, exist_ok=True)
                    current_output_dir = color_dir
                    
                # Organize by size if requested
                if organize_by_size:
                    size_dir = current_output_dir / f"{current_size}px"
                    size_dir.mkdir(parents=True, exist_ok=True)
                    current_output_dir = size_dir
                    
                # Generate output file name
                filename_parts = [icon_name]
                if not organize_by_style:
                    filename_parts.append(style)
                if not organize_by_size:
                    filename_parts.append(f"{current_size}")
                if not organize_by_color:
                    filename_parts.append(color_dirname)
                
                output_file = current_output_dir / f"{'_'.join(filename_parts)}.png"
                
                # Create image with transparent background
                img = Image.new("RGBA", (current_size, current_size), (0, 0, 0, 0))
                draw = ImageDraw.Draw(img)
                
                # Load font and calculate position to center icon
                font_size = int(current_size * 0.9)  # Font size slightly smaller than image
                font = ImageFont.truetype(str(font_file), font_size)
                
                # Get icon dimensions
                left, top, right, bottom = draw.textbbox((0, 0), unicode_char, font=font)
                icon_width, icon_height = right - left, bottom - top
                
                # Calculate position to center
                x = (current_size - icon_width) // 2 - left
                y = (current_size - icon_height) // 2 - top
                
                # Draw icon
                draw.text((x, y), unicode_char, font=font, fill=color)
                
                # Save the image
                img.save(output_file)
                
                logger.debug(f"Created '{icon_name}' ({style}) at size {current_size}px: {output_file}")
                output_files.append(str(output_file))
            except Exception as e:
                logger.error(f"Error rendering icon '{icon_name}' at size {current_size}px: {e}")
                
        return output_files
    
    def _get_sizes_to_generate(self, size: Union[int, List[int]]) -> List[int]:
        """
        Determine the sizes to generate based on the input parameter.
        
        Args:
            size: Either a single max size or a list of explicit sizes
            
        Returns:
            List of sizes to generate
        """
        if isinstance(size, list):
            # If a list is provided, use those exact sizes
            return sorted(size)
        else:
            # If a single value is provided, use it as the maximum size
            # and generate all default sizes up to that maximum
            return [s for s in self.default_sizes if s <= size]
            
    def convert_all(
        self, 
        style: Optional[Literal["solid", "regular", "brands"]] = None, 
        size: Union[int, List[int]] = 512,
        color: Optional[str] = None,
        render_method: Literal["svg", "font"] = "svg",
        output_dir: str = "output",
        organize_by_size: bool = True,
        organize_by_color: bool = True,
        organize_by_style: bool = True
    ) -> List[str]:
        """
        Convert all FontAwesome icons to PNG.
        
        Args:
            style: Filter by icon style (solid, regular, or brands). If None, all styles will be used.
            size: Output size in pixels or list of sizes
            color: Color for the icon (as hex code)
            render_method: Method to use for rendering (svg or font)
            output_dir: Directory to save the output
            organize_by_size: Whether to organize output files by size in subdirectories
            organize_by_color: Whether to organize output files by color in subdirectories
            organize_by_style: Whether to organize output files by style in subdirectories
            
        Returns:
            List of paths to the generated PNG files
        """
        output_files = []
        icons_processed = 0
        
        # Create output directory if it doesn't exist
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Get a list of all icons to process
        total_icons = len(self.icons_data)
        logger.info(f"Processing {total_icons} icons...")
        
        # Create progress bar
        with tqdm(total=total_icons, desc="Converting icons") as pbar:
            # Process each icon
            for icon_name, icon_info in self.icons_data.items():
                styles_to_process = []
                
                # If a specific style is requested, only process that style
                if style is not None:
                    if style in icon_info.get("styles", []):
                        styles_to_process = [style]
                else:
                    # Otherwise, process all available styles for the icon
                    styles_to_process = icon_info.get("styles", [])
                    
                # Process each style for the icon
                for current_style in styles_to_process:
                    # Choose the appropriate method for rendering
                    try:
                        if render_method == "svg":
                            files = self.convert_svg(
                                icon_name, 
                                style=current_style,
                                size=size,
                                color=color,
                                output_dir=output_dir,
                                organize_by_size=organize_by_size,
                                organize_by_color=organize_by_color,
                                organize_by_style=organize_by_style
                            )
                        else:
                            files = self.convert_font(
                                icon_name,
                                style=current_style,
                                size=size,
                                color=color or "#000000",
                                output_dir=output_dir,
                                organize_by_size=organize_by_size,
                                organize_by_color=organize_by_color,
                                organize_by_style=organize_by_style
                            )
                        
                        output_files.extend(files)
                    except Exception as e:
                        logger.error(f"Error processing '{icon_name}' ({current_style}): {str(e)}")
                        
                icons_processed += 1
                pbar.update(1)
                
                # Log progress at INFO level
                if icons_processed % 100 == 0:
                    logger.info(f"Processed {icons_processed}/{total_icons} icons")
                    
        logger.info(f"Completed converting {icons_processed} icons to PNG, created {len(output_files)} files")
        return output_files 