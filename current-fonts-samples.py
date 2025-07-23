#!/usr/bin/env python3

"""
Generate samples for the fonts currently used in welcome-banner.py
"""

from pyfiglet import Figlet

# Fonts from welcome-banner.py line 80
current_fonts = ['poison', 'larry3d', 'graffiti', 'nancyj-fancy', 'modular', 'sub-zero', 'starwars', 'bloody', 'blocky', 'bubble__', 'colossal', 'dos_rebel', 'gradient', 'georgia11', 'red_phoenix', 'tubular', 'the_edge', 'univers']

def generate_current_font_samples(text="Wils"):
    """Generate samples for currently used fonts only"""
    print(f"🎨 Generating samples for {len(current_fonts)} currently used fonts...")
    
    output_file = "current-fonts-samples.txt"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"CURRENT WELCOME BANNER FONTS\n")
        f.write(f"Text: '{text}'\n")
        f.write(f"Fonts in use: {len(current_fonts)}\n")
        f.write("=" * 80 + "\n\n")
        
        for i, font in enumerate(current_fonts, 1):
            try:
                # Create figlet with specific font
                fig = Figlet(font=font)
                result = fig.renderText(text)
                
                # Write font name and sample
                f.write(f"[{i:2d}/{len(current_fonts)}] FONT: {font}\n")
                f.write("-" * 40 + "\n")
                f.write(result)
                f.write("\n" + "=" * 80 + "\n\n")
                    
            except Exception as e:
                f.write(f"[{i:2d}/{len(current_fonts)}] FONT: {font} (ERROR: {e})\n")
                f.write("-" * 40 + "\n")
                f.write("Failed to render\n")
                f.write("\n" + "=" * 80 + "\n\n")
    
    print(f"✅ Current font samples saved to: {output_file}")
    
    # Also print to console for quick review
    print("\n" + "="*50)
    print("CURRENT FONTS PREVIEW:")
    print("="*50)
    
    for font in current_fonts:
        try:
            fig = Figlet(font=font)
            result = fig.renderText(text)
            print(f"\n[{font.upper()}]")
            print("-" * 20)
            print(result)
        except Exception as e:
            print(f"\n[{font.upper()}] - ERROR: {e}")

if __name__ == "__main__":
    generate_current_font_samples()