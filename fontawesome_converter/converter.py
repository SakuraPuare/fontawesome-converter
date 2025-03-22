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
        organize_by_size: bool = True
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
        
        # Convert SVG file to PNG at each requested size
        for current_size in sizes_to_generate:
            # Create size-specific output directory if organizing by size
            if organize_by_size:
                size_dir = output_dir / f"{current_size}px"
                size_dir.mkdir(parents=True, exist_ok=True)
                current_output_dir = size_dir
            else:
                current_output_dir = output_dir
                
            # Generate output file path
            if organize_by_size:
                output_file = current_output_dir / f"{icon_name}_{style}.png"
            else:
                output_file = current_output_dir / f"{icon_name}_{style}_{current_size}.png"
            
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
        organize_by_size: bool = True
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
        
        # Create images of each requested size
        for current_size in sizes_to_generate:
            try:
                # Create size-specific output directory if organizing by size
                if organize_by_size:
                    size_dir = output_dir / f"{current_size}px"
                    size_dir.mkdir(parents=True, exist_ok=True)
                    current_output_dir = size_dir
                else:
                    current_output_dir = output_dir
                
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
                
                # Generate output file path 
                if organize_by_size:
                    output_file = current_output_dir / f"{icon_name}_{style}.png"
                else:
                    output_file = current_output_dir / f"{icon_name}_{style}_{current_size}.png"
                
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
        organize_by_size: bool = True
    ) -> List[str]:
        """
        Convert all available icons or icons of a specific style.
        
        Args:
            style: Optional style filter (solid, regular, or brands)
            size: Output size in pixels or list of sizes (max size if single value)
            color: Color for the icon (as hex code)
            render_method: Method to use for rendering (svg or font)
            output_dir: Directory to save outputs
            organize_by_size: Whether to organize output files by size in subdirectories
            
        Returns:
            List of generated PNG files
        """
        output_files = []
        
        # Filter icons by style if specified
        icons_to_convert = []
        for icon_name, icon_data in self.icons_data.items():
            if style is None or style in icon_data.get("styles", []):
                icons_to_convert.append((icon_name, icon_data))
                
        # Get sizes for logging
        sizes_to_generate = self._get_sizes_to_generate(size)
        size_str = ", ".join(map(str, sizes_to_generate))
        
        # Log conversion info with organization method
        organization_method = "organized by size in subfolders" if organize_by_size else "all in the same folder"
        logger.info(f"Converting {len(icons_to_convert)} icons using {render_method} rendering at sizes: {size_str}px ({organization_method})")
        
        # Convert all matching icons with progress bar
        for icon_name, icon_data in tqdm(icons_to_convert, desc="Converting icons", smoothing=0.1):
            # Determine which styles to render for this icon
            styles_to_render = [style] if style else icon_data.get("styles", [])
            
            for icon_style in styles_to_render:
                if render_method == "svg":
                    new_files = self.convert_svg(
                        icon_name, 
                        style=icon_style, 
                        size=size, 
                        color=color, 
                        output_dir=output_dir,
                        organize_by_size=organize_by_size
                    )
                else:
                    new_files = self.convert_font(
                        icon_name, 
                        style=icon_style, 
                        size=size, 
                        color=color or "#000000", 
                        output_dir=output_dir,
                        organize_by_size=organize_by_size
                    )
                    
                output_files.extend(new_files)
        
        # Log size-specific counts if organized by size
        if organize_by_size:
            for current_size in sizes_to_generate:
                size_files = [f for f in output_files if f"{current_size}px" in f]
                logger.info(f"Size {current_size}px: {len(size_files)} icons")
                    
        logger.success(f"Successfully converted {len(output_files)} icons in {len(sizes_to_generate)} different sizes")
        return output_files 