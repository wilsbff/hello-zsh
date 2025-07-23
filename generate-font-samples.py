#!/usr/bin/env python3

"""
Generate pyfiglet font samples for all available fonts
Creates a comprehensive sample file to review font options
"""

from pyfiglet import Figlet
import sys

def generate_font_samples(text="Wils", output_file="font-samples.txt"):
    """Generate samples of all pyfiglet fonts with given text"""
    figlet = Figlet()
    fonts = sorted(figlet.getFonts())
    
    print(f"🎨 Generating samples for {len(fonts)} fonts...")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"PYFIGLET FONT SAMPLES\n")
        f.write(f"Text: '{text}'\n")
        f.write(f"Total fonts: {len(fonts)}\n")
        f.write("=" * 80 + "\n\n")
        
        for i, font in enumerate(fonts, 1):
            try:
                # Create figlet with specific font
                fig = Figlet(font=font)
                result = fig.renderText(text)
                
                # Write font name and sample
                f.write(f"[{i:3d}/{len(fonts)}] FONT: {font}\n")
                f.write("-" * 40 + "\n")
                f.write(result)
                f.write("\n" + "=" * 80 + "\n\n")
                
                # Progress indicator
                if i % 50 == 0:
                    print(f"  Progress: {i}/{len(fonts)} fonts processed...")
                    
            except Exception as e:
                f.write(f"[{i:3d}/{len(fonts)}] FONT: {font} (ERROR: {e})\n")
                f.write("-" * 40 + "\n")
                f.write("Failed to render\n")
                f.write("\n" + "=" * 80 + "\n\n")
    
    print(f"✅ Font samples saved to: {output_file}")
    print(f"📝 Total fonts processed: {len(fonts)}")

if __name__ == "__main__":
    # Allow custom text via command line
    text = sys.argv[1] if len(sys.argv) > 1 else "Wils"
    generate_font_samples(text)