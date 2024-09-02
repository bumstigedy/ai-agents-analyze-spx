import os
from PyPDF2 import PdfMerger

def merge_pdfs(output_filename):
    """Merge all PDF files in the current directory into a single PDF file."""
    merger = PdfMerger()
    
    # List all files in the current directory
    for item in os.listdir('.'):
        if item.endswith('.pdf'):
            print(f"Adding {item} to the merger")
            merger.append(item)
    
    # Write the merged PDF to a file
    with open(output_filename, 'wb') as output_pdf:
        merger.write(output_pdf)
    
    print(f"Merged PDF saved as {output_filename}")

def main():
    output_filename = "merged.pdf"
    merge_pdfs(output_filename)

if __name__ == "__main__":
    main()
