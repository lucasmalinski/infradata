import camelot
import pandas as pd
from pathlib import Path

MAIN_DATA_DIR = Path(__file__).resolve().parent / "raw_data"
PDF_DIR = MAIN_DATA_DIR / "trechos" / "SRDF_2025.pdf"

# ── 1. Extract all pages ──────────────────────────────────────────────────────
tables = camelot.read_pdf(
    str(PDF_DIR),
    pages='45-77',
    flavor='lattice',
    line_scale=40,        # helps detect thin grid lines
    copy_text=['v'],      # propagate text down in vertically merged cells
)

# ── 2. Combine all pages into one DataFrame ───────────────────────────────────
raw_frames = [t.df for t in tables]
df = pd.concat(raw_frames, ignore_index=True)

# ── 3. Clean newlines inside cells ───────────────────────────────────────────
df = df.replace(r'\n', ' ', regex=True)
df = df.map(lambda x: ' '.join(x.split()) if isinstance(x, str) else x)
# ── 4. Fix headers (rows 0 and 1 are both header rows — merge them) ───────────
# Combine the two header rows into one, joining non-empty parts with a space
header_row0 = df.iloc[0].tolist()
header_row1 = df.iloc[1].tolist()

merged_header = []
for a, b in zip(header_row0, header_row1):
    a, b = str(a).strip(), str(b).strip()
    if a and b and a != b:
        merged_header.append(f"{a} {b}")
    else:
        merged_header.append(a or b)

df.columns = merged_header
df = df.iloc[2:].reset_index(drop=True)  # drop the two header rows

# ── 5. Drop rows that are repeated headers (appear on every page) ─────────────
# Detect by checking if the first column matches the header value
first_col = merged_header[0]
df = df[df[first_col] != "TRECHO"].reset_index(drop=True)
df = df[df[first_col] != "CÓDIGO DO TRECHO"].reset_index(drop=True)

# ── 6. Drop fully empty rows ──────────────────────────────────────────────────
df = df[df[first_col].str.strip().astype(bool)].reset_index(drop=True)

# ── 7. Preview & save ─────────────────────────────────────────────────────────
print(df.shape)
print(df.head(10).to_string())

df.to_csv(MAIN_DATA_DIR / "trechos_cleaned.csv", index=False, encoding="utf-8-sig")
df.to_excel(MAIN_DATA_DIR / "trechos_cleaned.xlsx", index=False)