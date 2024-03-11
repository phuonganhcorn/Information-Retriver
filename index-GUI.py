import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
from assignment2 import index_corpus, search, search_and, search_or, search_and_not, search_or_not

class SearchApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Search Application")

        self.data_folder_label = tk.Label(master, text="Data Folder:")
        self.data_folder_label.grid(row=0, column=0, sticky="w")

        self.data_folder_entry = tk.Entry(master, width=50)
        self.data_folder_entry.grid(row=0, column=1)

        self.browse_button = tk.Button(master, text="Browse", command=self.browse_folder)
        self.browse_button.grid(row=0, column=2)

        self.index_button = tk.Button(master, text="Index Corpus", command=self.index_corpus)
        self.index_button.grid(row=1, column=0, columnspan=3, pady=10)

        self.query_label = tk.Label(master, text="Enter Query:")
        self.query_label.grid(row=2, column=0, sticky="w")

        self.query_entry = tk.Entry(master, width=50)
        self.query_entry.grid(row=2, column=1)

        self.search_button = tk.Button(master, text="Search", command=self.search_query)
        self.search_button.grid(row=2, column=2)

        self.result_label = tk.Label(master, text="Search Result:")
        self.result_label.grid(row=3, column=0, sticky="w")

        self.result_text = tk.Text(master, width=50, height=10)
        self.result_text.grid(row=3, column=1, columnspan=2)

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        self.data_folder_entry.delete(0, tk.END)
        self.data_folder_entry.insert(0, folder_path)

    def index_corpus(self):
        folder_path = self.data_folder_entry.get()
        if folder_path:
            try:
                index_corpus(folder_path, "index.txt")
                messagebox.showinfo("Indexing Completed", "Corpus has been indexed successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
        else:
            messagebox.showwarning("Warning", "Please select a data folder.")

    def search_query(self):
        folder_path = self.data_folder_entry.get()
        index_path = os.path.join(folder_path, "index.txt")
        index = {}
        with open(index_path, 'r') as file:
            for line in file:
                term, postings = line.strip().split('\t')
                index[term] = postings.split()

        query = self.query_entry.get()
        if query:
            try:
                # Perform search based on query
                # You need to implement the search functions accordingly
                # and update the result_text accordingly
                # For example:
                search_result = search(index, query)
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, '\n'.join(search_result))
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
        else:
            messagebox.showwarning("Warning", "Please enter a query.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SearchApp(root)
    root.mainloop()
