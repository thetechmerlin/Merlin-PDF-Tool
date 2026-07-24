# 🧙 MERLIN PDF TOOL

> **A unified offline PDF & image toolkit for Windows.**  
MERLIN PDF TOOL combines the most common PDF and image conversion tasks into one simple application. No cloud services, no subscriptions, and no uploading sensitive files—everything runs locally on your computer.

---

## ✨ Features

### 📄 Merge PDFs
Combine multiple PDF files into a single document.

- Merge unlimited PDFs
- Choose which document becomes **Page 1**
- Optional page numbering
- Preserves original quality

---

### 🖼 PDF to PNG

Convert PDF pages into high-quality PNG images.

- Batch conversion
- Custom DPI settings
- Great for graphics, printing, and editing

---

### 📦 Downsample PDFs

Reduce PDF file sizes using Ghostscript compression.

Perfect for:

- Email attachments
- Web uploads
- Archiving

---

### 📄 PNG to PDF

Convert PNG images into PDF documents.

Options include:

- One PDF containing all images
- Individual PDFs
- Optional page numbering

---

### 🖼 JPG → PNG

Losslessly convert JPG images into PNG format.

Useful when:

- Editing artwork
- Preparing graphics
- Preserving image quality

---

### 📸 PNG → JPG

Convert PNG images to JPG with adjustable quality.

Features:

- Adjustable compression quality
- Automatically replaces transparency with a white background
- Great for websites and sharing

---

# ✅ Included Files

| File | Purpose |
|------|---------|
| `merlin_engine.py` | Main application |
| `RUN_MERLIN.bat` | Launches MERLIN PDF TOOL |
| `CHECK_SETUP.bat` | Verifies all required dependencies |
| `README.md` | Local documentation |
| `README_GITHUB.md` | GitHub-ready documentation |

---

# 📁 Folder Structure

```text
MERLINPDFTOOL/
│
├── CHECK_SETUP.bat
├── RUN_MERLIN.bat
├── merlin_engine.py
├── README.md
├── README_GITHUB.md
│
├── pdfs/          ← PDF merge & PDF→PNG input
├── pngs/          ← PNG output folder
├── lrgpdf/        ← Compression input
├── smallpdf/      ← Compressed PDF output
├── PNGtoPDF/      ← PNG→PDF input
├── JPG/           ← JPG conversion input
└── Conversions/   ← Image conversion output
```

---

# 🔍 Built-in Setup Checker

MERLIN PDF TOOL includes a pre-flight diagnostic utility.

Run:

```text
CHECK_SETUP.bat
```

It verifies the installation of:

- ✅ Python 3.x
- ✅ pip
- ✅ Poppler (`pdftoppm`)
- ✅ Ghostscript (`gswin64c` / `gswin32c`)

If something is missing, the checker:

- Highlights the missing dependency
- Provides download links
- Explains how to add it to your system PATH

If everything is green, you're ready to launch:

```text
RUN_MERLIN.bat
```

---

# 💻 Requirements

- Windows 10 or newer
- Python 3.x
- Poppler
- Ghostscript

The included setup checker helps verify everything before first use.

---

# 🔒 Privacy First

MERLIN PDF TOOL works **completely offline**.

Your files:

- Never leave your computer
- Are never uploaded
- Require no internet connection
- Remain entirely under your control

Perfect for sensitive documents and professional workflows.

---

# 🚀 Getting Started

1. Download or clone the repository.
2. Run `CHECK_SETUP.bat`.
3. Install any missing dependencies if prompted.
4. Launch the application with `RUN_MERLIN.bat`.
5. Place your files into the appropriate input folders.
6. Process your files locally.

---

# 🛠 Built With

- Python
- Ghostscript
- Poppler
- Pillow
- Tkinter

---

# 📜 License

This project is provided as-is for personal and commercial use. See the LICENSE file for details.

---

## Merlin PDF Tool

**One application. Six essential tools. Completely offline.**