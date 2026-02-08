#!/usr/bin/env python3

import os
from pathlib import Path
import re

def parse_palette(palette_file):
    """Parse the palette.conf file and extract color definitions."""
    colors = {}
    
    with open(palette_file, 'r') as f:
        for line in f:
            line = line.strip()
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
            
            # Parse key=value or key: value format
            if '=' in line:
                key, value = line.split('=', 1)
            elif ':' in line:
                key, value = line.split(':', 1)
            else:
                continue
            
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            
            # Validate hex color format
            if re.match(r'^#?[0-9A-Fa-f]{6}$', value):
                if not value.startswith('#'):
                    value = '#' + value
                colors[key] = value
    
    return colors

def generate_vim_theme(colors, output_file):
    """Generate a Neovim theme file from the color palette."""
    
    theme_content = f'''\" Generated Neovim color scheme
\" Auto-generated from palette configuration

set background=dark
highlight clear
if exists("syntax_on")
    syntax reset
endif
let g:colors_name = "custom_theme"

\" UI Elements
highlight Normal guifg={colors.get('foreground', '#ffffff')} guibg={colors.get('background', '#000000')}
highlight StatusLine guifg={colors.get('foreground', '#ffffff')} guibg={colors.get('color8', '#444444')}
highlight StatusLineNC guifg={colors.get('color8', '#444444')} guibg={colors.get('background', '#000000')}
highlight VertSplit guifg={colors.get('color8', '#444444')} guibg={colors.get('background', '#000000')}
highlight LineNr guifg={colors.get('color8', '#444444')} guibg={colors.get('background', '#000000')}
highlight CursorLineNr guifg={colors.get('color3', '#ffff00')} guibg={colors.get('background', '#000000')} gui=bold
highlight CursorLine guibg={colors.get('color0', '#1c1c1c')} gui=NONE
highlight ColorColumn guibg={colors.get('color0', '#1c1c1c')}
highlight SignColumn guibg={colors.get('background', '#000000')}

\" Syntax Highlighting
highlight Comment guifg={colors.get('color8', '#444444')} gui=italic
highlight Constant guifg={colors.get('color1', '#ff0000')}
highlight String guifg={colors.get('color2', '#00ff00')}
highlight Character guifg={colors.get('color2', '#00ff00')}
highlight Number guifg={colors.get('color5', '#ff00ff')}
highlight Boolean guifg={colors.get('color5', '#ff00ff')}
highlight Float guifg={colors.get('color5', '#ff00ff')}

highlight Identifier guifg={colors.get('color4', '#0000ff')}
highlight Function guifg={colors.get('color6', '#00ffff')} gui=bold

highlight Statement guifg={colors.get('color3', '#ffff00')} gui=bold
highlight Conditional guifg={colors.get('color3', '#ffff00')}
highlight Repeat guifg={colors.get('color3', '#ffff00')}
highlight Label guifg={colors.get('color3', '#ffff00')}
highlight Operator guifg={colors.get('foreground', '#ffffff')}
highlight Keyword guifg={colors.get('color1', '#ff0000')} gui=bold

highlight PreProc guifg={colors.get('color6', '#00ffff')}
highlight Include guifg={colors.get('color6', '#00ffff')}
highlight Define guifg={colors.get('color6', '#00ffff')}
highlight Macro guifg={colors.get('color6', '#00ffff')}
highlight PreCondit guifg={colors.get('color6', '#00ffff')}

highlight Type guifg={colors.get('color4', '#0000ff')} gui=bold
highlight StorageClass guifg={colors.get('color3', '#ffff00')}
highlight Structure guifg={colors.get('color4', '#0000ff')}
highlight Typedef guifg={colors.get('color4', '#0000ff')}

highlight Special guifg={colors.get('color5', '#ff00ff')}
highlight SpecialChar guifg={colors.get('color5', '#ff00ff')}
highlight Tag guifg={colors.get('color3', '#ffff00')}
highlight Delimiter guifg={colors.get('foreground', '#ffffff')}
highlight SpecialComment guifg={colors.get('color6', '#00ffff')} gui=italic

highlight Error guifg={colors.get('color9', '#ff0000')} guibg={colors.get('background', '#000000')} gui=bold
highlight Todo guifg={colors.get('color3', '#ffff00')} guibg={colors.get('background', '#000000')} gui=bold

\" Search and Visual
highlight Search guifg={colors.get('background', '#000000')} guibg={colors.get('color3', '#ffff00')}
highlight IncSearch guifg={colors.get('background', '#000000')} guibg={colors.get('color1', '#ff0000')}
highlight Visual guibg={colors.get('color8', '#444444')}
highlight VisualNOS guibg={colors.get('color8', '#444444')}

\" Popup Menu
highlight Pmenu guifg={colors.get('foreground', '#ffffff')} guibg={colors.get('color0', '#1c1c1c')}
highlight PmenuSel guifg={colors.get('background', '#000000')} guibg={colors.get('color4', '#0000ff')}
highlight PmenuSbar guibg={colors.get('color8', '#444444')}
highlight PmenuThumb guibg={colors.get('foreground', '#ffffff')}
'''
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Write the theme file
    with open(output_file, 'w') as f:
        f.write(theme_content)
    
    print(f"✓ Theme file generated: {output_file}")

def main():
    # Define file paths
    home = Path.home()
    palette_file = home / '.config' / 'colors' / 'palate.conf'
    output_file = home / '.config' / 'nvim' / 'colors' / 'theme.vim'
    
    # Check if palette file exists
    if not palette_file.exists():
        print(f"Error: Palette file not found at {palette_file}")
        print("Please create the file with color definitions.")
        return 1
    
    try:
        # Parse the palette
        colors = parse_palette(palette_file)
        
        if not colors:
            print("Warning: No colors found in palette file")
            return 1
        
        print(f"Loaded {len(colors)} colors from {palette_file}")
        
        # Generate the Neovim theme
        generate_vim_theme(colors, output_file)
        
        print(f"\nTo use this theme in Neovim, add to your init.vim:")
        print(f"  colorscheme custom_theme")
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == '__main__':
    exit(main())
