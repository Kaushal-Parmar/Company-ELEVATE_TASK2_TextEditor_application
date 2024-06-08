import tkinter as tk
from tkinter import filedialog, messagebox
import keyword

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("My Text Editor")
        self.root.geometry("800x600")
        
        self.font_size = 12
        self.font_family = 'Arial'
        
        self.line_numbers = tk.Text(self.root, width=4, padx=3, takefocus=0, border=0, background='lightgrey', state='disabled')
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        
        self.text_area = tk.Text(self.root, wrap='word', undo=True, font=(self.font_family, self.font_size))
        self.text_area.pack(fill=tk.BOTH, expand=1)
        
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)
        
        self.settings_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Settings", menu=self.settings_menu)
        self.settings_menu.add_command(label="Increase Font Size", command=self.increase_font_size)
        self.settings_menu.add_command(label="Decrease Font Size", command=self.decrease_font_size)
        
        self.search_frame = tk.Frame(self.root)
        self.search_frame.pack(fill=tk.X)
        
        self.search_label = tk.Label(self.search_frame, text="Search")
        self.search_label.pack(side=tk.LEFT, padx=5)
        
        self.search_entry = tk.Entry(self.search_frame)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.search_button = tk.Button(self.search_frame, text="Find", command=self.search_text)
        self.search_button.pack(side=tk.LEFT, padx=5)
        
        self.text_area.bind("<KeyRelease>", self.on_key_release)
        self.update_line_numbers()
    
    def update_line_numbers(self, event=None):
        self.line_numbers.config(state='normal')
        self.line_numbers.delete(1.0, tk.END)
        line_numbers_str = "\n".join(str(i+1) for i in range(int(self.text_area.index('end-1c').split('.')[0])))
        self.line_numbers.insert(1.0, line_numbers_str)
        self.line_numbers.config(state='disabled')
    
    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r') as file:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, file.read())
            self.root.title(f"Python Text Editor - {file_path}")
            self.update_line_numbers()
    
    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt"),
                                                            ("Python files", "*.py"),
                                                            ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.text_area.get(1.0, tk.END))
            self.root.title(f"My Text Editor - {file_path}")
    
    def save_as_file(self):
        self.save_file()
    
    def search_text(self):
        self.text_area.tag_remove('search', '1.0', tk.END)
        search_query = self.search_entry.get()
        if search_query:
            idx = '1.0'
            while True:
                idx = self.text_area.search(search_query, idx, nocase=1, stopindex=tk.END)
                if not idx:
                    break
                lastidx = f"{idx}+{len(search_query)}c"
                self.text_area.tag_add('search', idx, lastidx)
                idx = lastidx
            self.text_area.tag_config('search', foreground='white', background='blue')
    
    def on_key_release(self, event=None):
        self.update_line_numbers()
        self.highlight_syntax()
    
    def increase_font_size(self):
        self.font_size += 2
        self.update_font()
    
    def decrease_font_size(self):
        self.font_size -= 2
        self.update_font()
    
    def update_font(self):
        self.text_area.config(font=(self.font_family, self.font_size))
        self.line_numbers.config(font=(self.font_family, self.font_size))
    
    def highlight_syntax(self):
        self.text_area.tag_remove('keyword', '1.0', tk.END)
        words = self.text_area.get('1.0', tk.END).split()
        for word in words:
            if word in keyword.kwlist:
                idx = '1.0'
                while True:
                    idx = self.text_area.search(word, idx, nocase=0, stopindex=tk.END)
                    if not idx:
                        break
                    lastidx = f"{idx}+{len(word)}c"
                    self.text_area.tag_add('keyword', idx, lastidx)
                    idx = lastidx
        self.text_area.tag_config('keyword', foreground='blue')

if __name__ == "__main__":
    root = tk.Tk()
    editor = TextEditor(root)
    root.mainloop()
