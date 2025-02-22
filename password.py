import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import json
import random
import string
import pyotp
import time

characters = string.ascii_letters + string.digits + string.punctuation

class PasswordManager:
    def __init__(self, root):
        self.root = root
        self.root.title("密码管理器")
        self.data = []
        self.language = tk.StringVar(value="中文")
        self.translations = {
            "中文": {
                "language": "语言:",
                "name": "名称:",
                "username": "用户名:",
                "password": "密码:",
                "totp": "TOTP验证器:",
                "generate_password": "生成密码",
                "generate_totp_secret": "生成TOTP密钥",
                "save": "保存",
                "import": "导入",
                "export": "导出",
                "info": "信息",
                "save_success": "保存成功!",
                "import_success": "导入成功!",
                "export_success": "导出成功!",
                "totp_generated": "已生成 TOTP 密钥！",
                "delete": "删除",
                "edit": "编辑",
                "no_selection": "没有选择条目",
                "delete_confirm": "确定要删除选定的条目吗?",
                "edit_title": "编辑条目",
                "confirm": "确认",
                "cancel": "取消",
                "totp_preview": "TOTP 预览:",
                "totp_time_remaining": "剩余时间: {} 秒",
                "totp_code": "TOTP 代码",
                "totp_time_remaining_col": "TOTP 剩余时间"
            },
            "English": {
                "language": "Language:",
                "name": "Name:",
                "username": "Username:",
                "password": "Password:",
                "totp": "TOTP Secret:",
                "generate_password": "Generate Password",
                "generate_totp_secret": "Generate TOTP Secret",
                "save": "Save",
                "import": "Import",
                "export": "Export",
                "info": "Info",
                "save_success": "Save Successful!",
                "import_success": "Import Successful!",
                "export_success": "Export Successful!",
                "totp_generated": "TOTP secret generated!",
                "delete": "Delete",
                "edit": "Edit",
                "no_selection": "No entry selected",
                "delete_confirm": "Are you sure you want to delete the selected entry?",
                "edit_title": "Edit Entry",
                "confirm": "Confirm",
                "cancel": "Cancel",
                "totp_preview": "TOTP Preview:",
                "totp_time_remaining": "Time remaining: {} seconds",
                "totp_code": "TOTP Code",
                "totp_time_remaining_col": "TOTP Time Remaining"
            }
        }
        self.create_widgets()
        self.update_tree()
        self.refresh_totp()

    def create_widgets(self):
        # Language selection
        lang_frame = tk.Frame(self.root)
        lang_frame.pack(pady=10)
        tk.Label(lang_frame, text=self.translations[self.language.get()]["language"]).pack(side=tk.LEFT)
        lang_options = ["中文", "English"]
        lang_menu = tk.OptionMenu(lang_frame, self.language, *lang_options, command=self.update_language)
        lang_menu.pack(side=tk.LEFT)

        # Entry fields
        self.name_var = tk.StringVar()
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.totp_var = tk.StringVar()

        tk.Label(self.root, text=self.translations[self.language.get()]["name"]).pack()
        tk.Entry(self.root, textvariable=self.name_var).pack()

        tk.Label(self.root, text=self.translations[self.language.get()]["username"]).pack()
        tk.Entry(self.root, textvariable=self.username_var).pack()

        tk.Label(self.root, text=self.translations[self.language.get()]["password"]).pack()
        tk.Entry(self.root, textvariable=self.password_var).pack()

        tk.Label(self.root, text=self.translations[self.language.get()]["totp"]).pack()
        tk.Entry(self.root, textvariable=self.totp_var).pack()

        # TOTP Preview
        self.totp_preview_var = tk.StringVar()
        self.totp_time_var = tk.StringVar()
        tk.Label(self.root, text=self.translations[self.language.get()]["totp_preview"]).pack()
        tk.Entry(self.root, textvariable=self.totp_preview_var, state='readonly').pack()
        tk.Label(self.root, textvariable=self.totp_time_var).pack()

        # Buttons
        tk.Button(self.root, text=self.translations[self.language.get()]["generate_password"], command=self.generate_password).pack(pady=5)
        tk.Button(self.root, text=self.translations[self.language.get()]["generate_totp_secret"], command=self.generate_totp_secret).pack(pady=5)
        tk.Button(self.root, text=self.translations[self.language.get()]["save"], command=self.save_entry).pack(pady=5)
        tk.Button(self.root, text=self.translations[self.language.get()]["import"], command=self.import_data).pack(pady=5)
        tk.Button(self.root, text=self.translations[self.language.get()]["export"], command=self.export_data).pack(pady=5)

        # Treeview
        self.tree = ttk.Treeview(self.root, columns=("name", "username", "password", "totp", "totp_code", "totp_time_remaining"), show="headings")
        self.tree.heading("name", text=self.translations[self.language.get()]["name"])
        self.tree.heading("username", text=self.translations[self.language.get()]["username"])
        self.tree.heading("password", text=self.translations[self.language.get()]["password"])
        self.tree.heading("totp", text=self.translations[self.language.get()]["totp"])
        self.tree.heading("totp_code", text=self.translations[self.language.get()]["totp_code"])
        self.tree.heading("totp_time_remaining", text=self.translations[self.language.get()]["totp_time_remaining_col"])
        self.tree.pack(pady=10)

        # Delete and Edit buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=5)
        tk.Button(button_frame, text=self.translations[self.language.get()]["delete"], command=self.delete_entry).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text=self.translations[self.language.get()]["edit"], command=self.edit_entry).pack(side=tk.LEFT, padx=5)

    def generate_password(self):
        length = 12
        password = ''.join(random.choice(characters) for i in range(length))
        self.password_var.set(password)

    def generate_totp_secret(self):
        secret = pyotp.random_base32()
        self.totp_var.set(secret)
        self.update_totp_preview()
        messagebox.showinfo(self.translations[self.language.get()]["info"], self.translations[self.language.get()]["totp_generated"])

    def save_entry(self):
        entry = {
            "name": self.name_var.get(),
            "username": self.username_var.get(),
            "password": self.password_var.get(),
            "totp": self.totp_var.get()
        }
        self.data.append(entry)
        self.update_tree()
        self.update_totp_preview()
        messagebox.showinfo(self.translations[self.language.get()]["info"], self.translations[self.language.get()]["save_success"])

    def import_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                self.data = json.load(file)
            self.update_tree()
            self.update_totp_preview()
            messagebox.showinfo(self.translations[self.language.get()]["info"], self.translations[self.language.get()]["import_success"])

    def export_data(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(self.data, file, ensure_ascii=False, indent=4)
            messagebox.showinfo(self.translations[self.language.get()]["info"], self.translations[self.language.get()]["export_success"])

    def update_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for entry in self.data:
            totp_code = pyotp.TOTP(entry["totp"]).now() if entry["totp"] else ""
            time_remaining = pyotp.TOTP(entry["totp"]).interval - time.time() % pyotp.TOTP(entry["totp"]).interval if entry["totp"] else ""
            self.tree.insert("", tk.END, values=(entry["name"], entry["username"], entry["password"], entry["totp"], totp_code, int(time_remaining) if time_remaining else ""))

    def delete_entry(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showinfo(self.translations[self.language.get()]["info"], self.translations[self.language.get()]["no_selection"])
            return

        if messagebox.askyesno(self.translations[self.language.get()]["info"], self.translations[self.language.get()]["delete_confirm"]):
            index = self.tree.index(selected_item[0])
            del self.data[index]
            self.update_tree()
            self.update_totp_preview()

    def edit_entry(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showinfo(self.translations[self.language.get()]["info"], self.translations[self.language.get()]["no_selection"])
            return

        index = self.tree.index(selected_item[0])
        entry = self.data[index]

        edit_window = tk.Toplevel(self.root)
        edit_window.title(self.translations[self.language.get()]["edit_title"])

        name_label = tk.Label(edit_window, text=self.translations[self.language.get()]["name"])
        name_label.pack()
        name_entry = tk.Entry(edit_window)
        name_entry.insert(0, entry["name"])
        name_entry.pack()

        username_label = tk.Label(edit_window, text=self.translations[self.language.get()]["username"])
        username_label.pack()
        username_entry = tk.Entry(edit_window)
        username_entry.insert(0, entry["username"])
        username_entry.pack()

        password_label = tk.Label(edit_window, text=self.translations[self.language.get()]["password"])
        password_label.pack()
        password_entry = tk.Entry(edit_window)
        password_entry.insert(0, entry["password"])
        password_entry.pack()

        totp_label = tk.Label(edit_window, text=self.translations[self.language.get()]["totp"])
        totp_label.pack()
        totp_entry = tk.Entry(edit_window)
        totp_entry.insert(0, entry["totp"])
        totp_entry.pack()

        def save_edit():
            self.data[index] = {
                "name": name_entry.get(),
                "username": username_entry.get(),
                "password": password_entry.get(),
                "totp": totp_entry.get()
            }
            self.update_tree()
            self.update_totp_preview()
            edit_window.destroy()

        confirm_button = tk.Button(edit_window, text=self.translations[self.language.get()]["confirm"], command=save_edit)
        confirm_button.pack(side=tk.LEFT, padx=5)
        cancel_button = tk.Button(edit_window, text=self.translations[self.language.get()]["cancel"], command=edit_window.destroy)
        cancel_button.pack(side=tk.LEFT, padx=5)

    def update_language(self, language):
        self.language.set(language)
        self.update_widgets_text()
        self.update_tree()

    def update_widgets_text(self):
        lang = self.translations[self.language.get()]
        # Update labels
        lang_frame = self.root.winfo_children()[0]
        lang_frame.winfo_children()[0].config(text=lang["language"])
        self.root.winfo_children()[1].config(text=lang["name"])
        self.root.winfo_children()[3].config(text=lang["username"])
        self.root.winfo_children()[5].config(text=lang["password"])
        self.root.winfo_children()[7].config(text=lang["totp"])

        # Update buttons
        self.root.winfo_children()[9].config(text=lang["generate_password"])
        self.root.winfo_children()[10].config(text=lang["generate_totp_secret"])
        self.root.winfo_children()[11].config(text=lang["save"])
        self.root.winfo_children()[12].config(text=lang["import"])
        self.root.winfo_children()[13].config(text=lang["export"])

        # Update tree headings
        self.tree.heading("name", text=lang["name"])
        self.tree.heading("username", text=lang["username"])
        self.tree.heading("password", text=lang["password"])
        self.tree.heading("totp", text=lang["totp"])
        self.tree.heading("totp_code", text=lang["totp_code"])
        self.tree.heading("totp_time_remaining", text=lang["totp_time_remaining_col"])

        # Update delete and edit buttons
        button_frame = self.root.winfo_children()[15]
        button_frame.winfo_children()[0].config(text=lang["delete"])
        button_frame.winfo_children()[1].config(text=lang["edit"])

    def update_totp_preview(self):
        totp_secret = self.totp_var.get()
        if totp_secret:
            totp = pyotp.TOTP(totp_secret)
            self.totp_preview_var.set(totp.now())
            time_remaining = totp.interval - time.time() % totp.interval
            self.totp_time_var.set(self.translations[self.language.get()]["totp_time_remaining"].format(int(time_remaining)))
        else:
            self.totp_preview_var.set("")
            self.totp_time_var.set("")

    def refresh_totp(self):
        self.update_totp_preview()
        self.update_tree()
        self.root.after(1000, self.refresh_totp)  # Refresh every second to update time remaining

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManager(root)
    root.mainloop()