#!/usr/bin/env python3
"""
MERLIN PDF TOOL
A unified offline PDF toolkit: Merge, Convert, Downsample, Image tools
"""

import subprocess
import sys
import shutil
from pathlib import Path
import io

# === CONFIG ===
BASE_DIR = Path(__file__).parent.resolve()
FOLDERS = {
    "pdfs": BASE_DIR / "pdfs",
    "pngs": BASE_DIR / "pngs",
    "lrgpdf": BASE_DIR / "lrgpdf",
    "smallpdf": BASE_DIR / "smallpdf",
    "PNGtoPDF": BASE_DIR / "PNGtoPDF",
    "JPG": BASE_DIR / "JPG",
    "Conversions": BASE_DIR / "Conversions",
}

# Ensure all folders exist
for f in FOLDERS.values():
    f.mkdir(exist_ok=True)

# === DEPENDENCY CHECK / INSTALL ===
REQUIRED_PACKAGES = {
    "pdf2image": "pdf2image",
    "PIL": "pillow",
    "pypdf": "pypdf",
    "reportlab": "reportlab",
}

def ensure_dependencies():
    missing = []
    for module, package in REQUIRED_PACKAGES.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)
    
    if missing:
        print("\n" + "="*50)
        print("INSTALLING MISSING PACKAGES...")
        print("="*50)
        for pkg in missing:
            print(f"  Installing {pkg}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
        print("\n+ All packages installed.\n")

# === FEATURE 1: MERGE PDFS WITH PAGE NUMBERS ===
def feature_merge():
    from pypdf import PdfWriter, PdfReader
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    input_folder = FOLDERS["pdfs"]
    output_file = BASE_DIR / "merged.pdf"
    
    pdf_files = sorted(input_folder.glob("*.pdf"))
    if not pdf_files:
        print(f"\nX No PDFs found in: {input_folder}")
        print("   Add PDF files and try again.")
        return
    
    print(f"\n+ Found {len(pdf_files)} PDF(s) in: {input_folder}")
    print("\n" + "-"*50)
    print("SELECT WHICH FILE SHOULD BE NUMBERED AS PAGE 1")
    print("-"*50)
    
    for i, pdf in enumerate(pdf_files, 1):
        print(f"  [{i}] {pdf.name}")
    
    print(f"\n  [0] Skip page numbering")
    print("-"*50)
    
    while True:
        choice = input("\nEnter number: ").strip()
        if choice == "0":
            page_number_start_index = len(pdf_files) + 999
            initial_page_number = 1
            break
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(pdf_files):
                page_number_start_index = idx
                initial_page_number = 1
                break
            else:
                print("   Invalid selection.")
        except ValueError:
            print("   Enter a number.")
    
    font_path = Path(r"C:\Windows\Fonts\arial.ttf")
    if font_path.exists():
        pdfmetrics.registerFont(TTFont('ArialCustom', str(font_path)))
        font_name = 'ArialCustom'
    else:
        font_name = 'Helvetica'
    
    writer = PdfWriter()
    current_page_number = initial_page_number
    
    def add_page_number_overlay(page_width, page_height, page_num):
        packet = io.BytesIO()
        c = canvas.Canvas(packet, pagesize=(page_width, page_height))
        c.setFont(font_name, 10)
        text = str(page_num)
        text_width = c.stringWidth(text, font_name, 10)
        x = page_width - text_width - 30
        y = 15
        c.drawString(x, y, text)
        c.save()
        packet.seek(0)
        return PdfReader(packet)
    
    print(f"\n> Merging {len(pdf_files)} file(s)...")
    if page_number_start_index < len(pdf_files):
        print(f"   Page numbering starts at file #{page_number_start_index + 1}: {pdf_files[page_number_start_index].name}")
    else:
        print("   No page numbering.")
    
    for file_index, pdf_path in enumerate(pdf_files):
        print(f"   Adding: {pdf_path.name}")
        reader = PdfReader(str(pdf_path))
        
        for page in reader.pages:
            page_width = float(page.mediabox.width)
            page_height = float(page.mediabox.height)
            
            if file_index >= page_number_start_index:
                overlay = add_page_number_overlay(page_width, page_height, current_page_number)
                overlay_page = overlay.pages[0]
                page.merge_page(overlay_page)
                current_page_number += 1
            
            writer.add_page(page)
    
    with open(output_file, "wb") as f:
        writer.write(f)
    
    print(f"\n+ Merged to: {output_file}")
    print(f"   Total pages: {len(writer.pages)}")
    if page_number_start_index < len(pdf_files):
        print(f"   Numbered pages: {current_page_number - initial_page_number}")

# === FEATURE 2: PDF TO PNG ===
def feature_pdf_to_png():
    from pdf2image import convert_from_path
    
    input_folder = FOLDERS["pdfs"]
    output_folder = FOLDERS["pngs"]
    
    pdf_files = sorted(input_folder.glob("*.pdf"))
    if not pdf_files:
        print(f"\nX No PDFs found in: {input_folder}")
        return
    
    while True:
        dpi_input = input("\nEnter DPI (150=web, 300=print, 600=high): ").strip()
        try:
            dpi = int(dpi_input)
            if 72 <= dpi <= 600:
                break
            print("   Enter between 72 and 600.")
        except ValueError:
            print("   Invalid. Enter a number.")
    
    print(f"\n> Converting {len(pdf_files)} PDF(s) at {dpi} DPI...")
    
    for pdf_path in pdf_files:
        print(f"   Converting: {pdf_path.name}")
        try:
            images = convert_from_path(pdf_path, dpi=dpi, fmt="png", thread_count=4)
            base_name = pdf_path.stem
            for i, image in enumerate(images, start=1):
                out_name = f"{base_name}_page_{i}.png"
                out_path = output_folder / out_name
                image.save(out_path, "PNG")
                print(f"      -> {out_name}")
        except Exception as e:
            print(f"      X Error: {e}")
    
    print(f"\n+ Done! PNGs saved to: {output_folder}")

# === FEATURE 3: DOWNSAMPLE PDFS ===
def feature_downsample():
    input_folder = FOLDERS["lrgpdf"]
    output_folder = FOLDERS["smallpdf"]
    
    gs_exe = shutil.which("gswin64c") or shutil.which("gswin32c") or shutil.which("gs")
    
    if not gs_exe:
        print("\nX Ghostscript not found in PATH.")
        print("   Download from: https://www.ghostscript.com/download/gsdnld.html")
        print("   Install and add to PATH, then retry.")
        return
    
    pdf_files = sorted(input_folder.glob("*.pdf"))
    if not pdf_files:
        print(f"\nX No PDFs found in: {input_folder}")
        return
    
    print(f"\n+ Found {len(pdf_files)} PDF(s) in: {input_folder}")
    
    while True:
        pct_input = input("\nEnter downsampling percentage (1-100): ").strip()
        try:
            percentage = float(pct_input)
            if 1 <= percentage <= 100:
                break
            print("   Enter 1-100.")
        except ValueError:
            print("   Invalid. Enter a number.")
    
    target_dpi = int(300 * percentage / 100)
    print(f"\n> Downsampling to {percentage}% (target {target_dpi} DPI)...")
    print("-"*50)
    
    for pdf_path in pdf_files:
        output_path = output_folder / pdf_path.name
        print(f"   Processing: {pdf_path.name}")
        
        cmd = [
            gs_exe,
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.4",
            "-dNOPAUSE",
            "-dQUIET",
            "-dBATCH",
            "-dAutoRotatePages=/None",
            "-dPreserveAnnots=false",
            f"-dColorImageResolution={target_dpi}",
            f"-dGrayImageResolution={target_dpi}",
            f"-dMonoImageResolution={target_dpi}",
            "-dDownsampleColorImages=true",
            "-dDownsampleGrayImages=true",
            "-dDownsampleMonoImages=true",
            "-dColorImageDownsampleType=/Bicubic",
            "-dGrayImageDownsampleType=/Bicubic",
            "-dMonoImageDownsampleType=/Bicubic",
            "-dCompressFonts=true",
            "-dSubsetFonts=true",
            f"-sOutputFile={output_path}",
            str(pdf_path)
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                orig_size = pdf_path.stat().st_size / 1024
                new_size = output_path.stat().st_size / 1024
                print(f"      + {orig_size:.1f} KB -> {new_size:.1f} KB")
            else:
                print(f"      X Error: {result.stderr[:200]}")
        except Exception as e:
            print(f"      X Failed: {e}")
    
    print(f"\n+ Done! Files saved to: {output_folder}")

# === FEATURE 4: PNG TO PDF ===
def feature_png_to_pdf():
    from PIL import Image
    from pypdf import PdfWriter, PdfReader
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    
    input_folder = FOLDERS["PNGtoPDF"]
    png_files = sorted(input_folder.glob("*.png"))
    
    if not png_files:
        print(f"\nX No PNGs found in: {input_folder}")
        return
    
    print(f"\n+ Found {len(png_files)} PNG(s) in: {input_folder}")
    print("\n" + "-"*50)
    print("SELECT OUTPUT MODE")
    print("-"*50)
    print("  [1] Merge all PNGs into a single PDF")
    print("  [2] Create individual PDFs for each PNG")
    print("-"*50)
    
    while True:
        mode = input("\nEnter mode: ").strip()
        if mode in ("1", "2"):
            break
        print("   Enter 1 or 2.")
    
    while True:
        dpi_input = input("\nEnter output DPI (150=web, 300=print): ").strip()
        try:
            dpi = int(dpi_input)
            if 72 <= dpi <= 600:
                break
            print("   Enter between 72 and 600.")
        except ValueError:
            print("   Invalid. Enter a number.")
    
    if mode == "1":
        output_file = BASE_DIR / "PNGtoPDF_merged.pdf"
        
        print("\n" + "-"*50)
        print("SELECT WHICH IMAGE SHOULD BE NUMBERED AS PAGE 1")
        print("-"*50)
        
        for i, png in enumerate(png_files, 1):
            print(f"  [{i}] {png.name}")
        print(f"\n  [0] Skip page numbering")
        print("-"*50)
        
        while True:
            choice = input("\nEnter number: ").strip()
            if choice == "0":
                page_number_start_index = len(png_files) + 999
                break
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(png_files):
                    page_number_start_index = idx
                    break
                else:
                    print("   Invalid selection.")
            except ValueError:
                print("   Enter a number.")
        
        font_path = Path(r"C:\Windows\Fonts\arial.ttf")
        if font_path.exists():
            pdfmetrics.registerFont(TTFont('ArialCustom', str(font_path)))
            font_name = 'ArialCustom'
        else:
            font_name = 'Helvetica'
        
        writer = PdfWriter()
        current_page_number = 1
        
        def add_page_number_overlay(page_width, page_height, page_num):
            packet = io.BytesIO()
            c = canvas.Canvas(packet, pagesize=(page_width, page_height))
            c.setFont(font_name, 10)
            text = str(page_num)
            text_width = c.stringWidth(text, font_name, 10)
            x = page_width - text_width - 30
            y = 15
            c.drawString(x, y, text)
            c.save()
            packet.seek(0)
            return PdfReader(packet)
        
        print(f"\n> Converting {len(png_files)} PNG(s) to merged PDF at {dpi} DPI...")
        if page_number_start_index < len(png_files):
            print(f"   Page numbering starts at image #{page_number_start_index + 1}: {png_files[page_number_start_index].name}")
        else:
            print("   No page numbering.")
        
        for file_index, png_path in enumerate(png_files):
            print(f"   Adding: {png_path.name}")
            img = Image.open(png_path)
            
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            width_pt = (img.width / dpi) * 72
            height_pt = (img.height / dpi) * 72
            
            temp_pdf = io.BytesIO()
            img.save(temp_pdf, format="PDF", resolution=dpi)
            temp_pdf.seek(0)
            
            reader = PdfReader(temp_pdf)
            page = reader.pages[0]
            
            if file_index >= page_number_start_index:
                overlay = add_page_number_overlay(width_pt, height_pt, current_page_number)
                overlay_page = overlay.pages[0]
                page.merge_page(overlay_page)
                current_page_number += 1
            
            writer.add_page(page)
            img.close()
        
        with open(output_file, "wb") as f:
            writer.write(f)
        
        print(f"\n+ Merged PDF saved to: {output_file}")
        print(f"   Total pages: {len(writer.pages)}")
        if page_number_start_index < len(png_files):
            print(f"   Numbered pages: {current_page_number - 1}")
    
    else:
        output_folder = FOLDERS["PNGtoPDF"]
        print(f"\n> Converting {len(png_files)} PNG(s) to individual PDFs at {dpi} DPI...")
        
        for png_path in png_files:
            output_file = output_folder / f"{png_path.stem}.pdf"
            print(f"   Converting: {png_path.name} -> {output_file.name}")
            
            try:
                img = Image.open(png_path)
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                img.save(output_file, "PDF", resolution=dpi)
                img.close()
                print(f"      + Done")
            except Exception as e:
                print(f"      X Error: {e}")
        
        print(f"\n+ Done! PDFs saved to: {output_folder}")

# === FEATURE 5: JPG TO PNG ===
def feature_jpg_to_png():
    from PIL import Image
    
    input_folder = FOLDERS["JPG"]
    output_folder = FOLDERS["Conversions"]
    
    jpg_files = sorted(input_folder.glob("*.jpg")) + sorted(input_folder.glob("*.jpeg"))
    
    if not jpg_files:
        print(f"\nX No JPG/JPEG files found in: {input_folder}")
        return
    
    print(f"\n+ Found {len(jpg_files)} JPG/JPEG file(s) in: {input_folder}")
    print(f"> Converting to PNG...")
    print("-"*50)
    
    for jpg_path in jpg_files:
        output_file = output_folder / f"{jpg_path.stem}.png"
        print(f"   {jpg_path.name} -> {output_file.name}")
        
        try:
            img = Image.open(jpg_path)
            img.save(output_file, "PNG")
            img.close()
            print(f"      + Done")
        except Exception as e:
            print(f"      X Error: {e}")
    
    print(f"\n+ Done! PNGs saved to: {output_folder}")

# === FEATURE 6: PNG TO JPG ===
def feature_png_to_jpg():
    from PIL import Image
    
    input_folder = FOLDERS["JPG"]
    output_folder = FOLDERS["Conversions"]
    
    png_files = sorted(input_folder.glob("*.png"))
    
    if not png_files:
        print(f"\nX No PNG files found in: {input_folder}")
        return
    
    while True:
        quality_input = input("\nEnter JPEG quality (1-100, default 95): ").strip()
        if not quality_input:
            quality = 95
            break
        try:
            quality = int(quality_input)
            if 1 <= quality <= 100:
                break
            print("   Enter between 1 and 100.")
        except ValueError:
            print("   Invalid. Enter a number.")
    
    print(f"\n+ Found {len(png_files)} PNG file(s) in: {input_folder}")
    print(f"> Converting to JPG at quality {quality}...")
    print("-"*50)
    
    for png_path in png_files:
        output_file = output_folder / f"{png_path.stem}.jpg"
        print(f"   {png_path.name} -> {output_file.name}")
        
        try:
            img = Image.open(png_path)
            if img.mode in ('RGBA', 'P', 'LA'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            img.save(output_file, "JPEG", quality=quality, optimize=True)
            img.close()
            print(f"      + Done")
        except Exception as e:
            print(f"      X Error: {e}")
    
    print(f"\n+ Done! JPGs saved to: {output_folder}")

# === MAIN MENU ===
def main():
    ensure_dependencies()
    
    while True:
        print("\n" + "="*60)
        print("  MERLIN PDF TOOL")
        print("="*60)
        print("\n  FOLDER STRUCTURE:")
        print("     pdfs/       -> Input for Merge and PDF-to-PNG")
        print("     pngs/       -> PNG outputs")
        print("     lrgpdf/     -> Input for PDF compression")
        print("     smallpdf/   -> Compressed PDF outputs")
        print("     PNGtoPDF/   -> PNGs to convert to PDF")
        print("     JPG/        -> Images for format conversion")
        print("     Conversions/-> Converted image outputs")
        print("\n  OPTIONS:")
        print("     [1] Merge PDFs (with optional page numbering)")
        print("     [2] Convert PDFs to PNGs")
        print("     [3] Downsample PDFs (reduce file size)")
        print("     [4] Convert PNGs to PDF (merged or individual)")
        print("     [5] Convert JPG to PNG")
        print("     [6] Convert PNG to JPG")
        print("     [Q] Quit")
        print("="*60)
        
        choice = input("\nSelect option: ").strip().lower()
        
        if choice == "1":
            feature_merge()
        elif choice == "2":
            feature_pdf_to_png()
        elif choice == "3":
            feature_downsample()
        elif choice == "4":
            feature_png_to_pdf()
        elif choice == "5":
            feature_jpg_to_png()
        elif choice == "6":
            feature_png_to_jpg()
        elif choice in ("q", "quit", "exit"):
            print("\nGoodbye!")
            break
        else:
            print("\nX Invalid option. Try again.")
        
        input("\nPress Enter to return to menu...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted. Goodbye!")
        sys.exit(0)