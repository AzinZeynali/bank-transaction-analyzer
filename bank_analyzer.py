import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk

df_global = None

def clean_columns(columns):
return columns.str.strip().str.replace('\u200c', '', regex=False).str.replace(' ', '', regex=False)

def load_file():
global df_global
file_path = filedialog.askopenfilename(
filetypes=[("Excel Files", "*.xlsx *.xls")],
title="انتخاب فایل اکسل"
)
if not file_path:
return

try:
df = pd.read_excel(file_path)
# df.columns = clean_columns(df.columns)

# check that required columns exist
required_columns = ['تاريخ', 'شماره سند', 'کد عمل']
for col in required_columns:
if col not in df.columns:
messagebox.showerror("خطا", f"ستون '{col}' پیدا نشد.")
return

df = df.dropna(subset=required_columns)
df_global = df

# extract unique dates
unique_dates = sorted(df['تاريخ'].unique())
combo_date['values'] = unique_dates
combo_date.set("انتخاب تاریخ")

combo_sanad['values'] = []
combo_sanad.set("شماره سند")

output_text.delete("1.0", tk.END)
output_text.insert(tk.END, " فایل با موفقیت بارگذاری شد. لطفاً یک تاریخ انتخاب کنید.\n")

except Exception as e:
messagebox.showerror("خطا در پردازش فایل", str(e))

def on_date_selected(event=None):
global df_global
selected_date = combo_date.get()
if not selected_date or df_global is None:
return

df = df_global
date_rows = df[df['تاريخ'] == selected_date]
unique_sanads = sorted(date_rows['شماره سند'].unique())

combo_sanad['values'] = unique_sanads
combo_sanad.set("انتخاب شماره سند")
output_text.delete("1.0", tk.END)
output_text.insert(tk.END, f" تاریخ انتخاب‌شده: {selected_date}\n")
output_text.insert(tk.END, " لطفاً شماره سند را انتخاب کنید.\n")

def on_sanad_selected(event=None):
global df_global
selected_date = combo_date.get()
selected_sanad = combo_sanad.get()

if not selected_date or not selected_sanad:
return

df = df_global

rows = df[(df['تاريخ'] == selected_date) & (df['شماره سند'] == selected_sanad)]
if rows.empty:
output_text.insert(tk.END, "\n هیچ رکوردی برای این تاریخ و شماره سند یافت نشد.\n")
return

output_text.delete("1.0", tk.END)
output_text.insert(tk.END, f" رکوردهای تاریخ {selected_date} و شماره سند {selected_sanad}:\n")
output_text.insert(tk.END, rows.to_string(index=False) + "\n\n")

# check for mismatched action codes within the same document
unique_actions = rows['کد عمل'].unique()
if len(unique_actions) > 1:
output_text.insert(tk.END, " کدهای عمل مختلف یافت شد:\n")
for action in unique_actions:
sub = rows[rows['کد عمل'] == action]
output_text.insert(tk.END, f"\n کد عمل: {action}\n")
output_text.insert(tk.END, sub.to_string(index=False) + "\n")
else:
output_text.insert(tk.END, " همه رکوردها کد عمل یکسان دارند.\n")

# GUI setup
root = tk.Tk()
root.title("تحلیل تراکنش بانکی")
root.geometry("850x600")

btn_load = tk.Button(root, text=" انتخاب فایل اکسل", command=load_file, font=("Tahoma", 12))
btn_load.pack(pady=10)

combo_date = ttk.Combobox(root, font=("Tahoma", 12), width=30, state="readonly")
combo_date.pack(pady=5)
combo_date.bind("<<ComboboxSelected>>", on_date_selected)

combo_sanad = ttk.Combobox(root, font=("Tahoma", 12), width=30, state="readonly")
combo_sanad.pack(pady=5)
combo_sanad.bind("<<ComboboxSelected>>", on_sanad_selected)

output_text = scrolledtext.ScrolledText(root, font=("Courier New", 10), wrap=tk.WORD)
output_text.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

root.mainloop()
