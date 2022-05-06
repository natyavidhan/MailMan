import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import json

ctk.set_appearance_mode("dark")


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("MailMan")
        self.root.geometry("950x470")
        self.root.resizable(False, False)

        self.data = json.load(open("data.json"))
        requests = [i["name"] for i in self.data]

        self.header = ctk.CTkFrame(self.root, corner_radius=10)
        self.header.place(width=445, height=80, x=25, y=20)

        ctk.CTkLabel(self.header, text="MailMan", text_font=("Acme", 30, "bold")).place(
            x=10, y=0, width=180, height=80
        )
        ctk.CTkButton(
            self.header,
            text="New Request",
            command=self.new_request,
            corner_radius=10,
            text_font=("Acme", 18, "bold"),
        ).place(x=200, y=15, width=235, height=55)

        self.active_request_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.active_request_frame.place(width=445, height=80, x=480, y=20)

        ctk.CTkLabel(
            self.active_request_frame,
            text="Active Request",
            text_font=("Acme", 15, "bold"),
        ).place(x=10, y=0, width=180, height=80)
        self.current_request = ttk.Combobox(
            self.active_request_frame, values=requests, state="readonly"
        )
        self.current_request.place(x=200, y=30, width=235, height=25)
        self.current_request.bind("<<ComboboxSelected>>", self.load_request)

        self.headers_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.headers_frame.place(width=445, height=145, x=25, y=135)

        ctk.CTkLabel(
            self.headers_frame, text="Headers", text_font=("Acme", 15, "bold")
        ).place(x=25, y=15, width=100, height=30)
        self.headers_input = tk.Text(
            self.headers_frame,
            bg="gray24",
            borderwidth=2,
            relief="flat",
            font=("Acme", 12),
            fg="white",
        )
        self.headers_input.place(x=25, y=50, width=395, height=85)

        self.body_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.body_frame.place(width=445, height=145, x=25, y=290)

        ctk.CTkLabel(
            self.body_frame, text="Body", text_font=("Acme", 15, "bold")
        ).place(x=25, y=15, width=100, height=30)
        self.body_input = tk.Text(
            self.body_frame,
            bg="gray24",
            borderwidth=2,
            relief="flat",
            font=("Acme", 12),
            fg="white",
        )
        self.body_input.place(x=25, y=50, width=395, height=85)

        ctk.CTkLabel(
            self.body_frame, text="Type", text_font=("Acme", 15, "bold")
        ).place(x=130, y=15, width=100, height=30)
        self.body_types = ttk.Combobox(
            self.body_frame, values=["Text", "JSON", "Form"], state="readonly"
        )
        self.body_types.place(x=215, y=15, width=100, height=25)
        self.body_types.current(0)

        self.options_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.options_frame.place(width=440, height=260, x=480, y=175)

        ctk.CTkButton(
            self.options_frame,
            text="Save",
            corner_radius=10,
            text_font=("Acme", 18, "bold"),
        ).place(x=40, y=15, width=360, height=45)
        ctk.CTkButton(
            self.options_frame,
            text="Rename",
            corner_radius=10,
            text_font=("Acme", 18, "bold"),
        ).place(x=40, y=75, width=360, height=45)
        ctk.CTkButton(
            self.options_frame,
            text="Delete",
            corner_radius=10,
            text_font=("Acme", 18, "bold"),
        ).place(x=40, y=135, width=360, height=45)
        ctk.CTkButton(
            self.options_frame,
            text="Send",
            corner_radius=10,
            text_font=("Acme", 18, "bold"),
        ).place(x=40, y=195, width=360, height=45)

        self.url = ctk.CTkEntry(
            self.root, text_font=("Acme", 12, "bold"), width=310, height=30
        )
        self.url.place(x=480, y=140)

        self.request_type = ttk.Combobox(
            self.root, values=["GET", "POST", "PUT", "DELETE"], state="readonly"
        )
        self.request_type.place(x=800, y=140, width=120, height=30)

    def new_request(self):
        prompt = ctk.CTkToplevel(self.root)
        prompt.title("New Request")
        prompt.geometry("400x200")
        prompt.resizable(False, False)

        ctk.CTkLabel(prompt, text="New Request", text_font=("Acme", 25, "bold")).place(
            x=0, y=25, width=400, height=30
        )
        ctk.CTkLabel(prompt, text="Name", text_font=("Acme", 15, "bold")).place(
            x=0, y=80, width=115, height=20
        )
        ctk.CTkLabel(prompt, text="URL", text_font=("Acme", 15, "bold")).place(
            x=0, y=110, width=115, height=20
        )
        ctk.CTkLabel(prompt, text="Type", text_font=("Acme", 15, "bold")).place(
            x=0, y=140, width=115, height=20
        )

        name = ctk.CTkEntry(
            prompt, text_font=("Acme", 15, "bold"), width=240, corner_radius=10
        )
        url = ctk.CTkEntry(
            prompt, text_font=("Acme", 15, "bold"), width=240, corner_radius=10
        )
        typ = ttk.Combobox(
            prompt, values=["GET", "POST", "PUT", "DELETE"], state="readonly"
        )

        name.place(x=115, y=80)
        url.place(x=115, y=110)
        typ.place(x=115, y=140)

        def create_request():
            data = {
                "name": name.get(),
                "url": url.get(),
                "type": typ.get(),
                "headers": "",
                "body": "",
                "body_type": "text",
            }
            requests = json.load(open("data.json"))
            requests.append(data)
            request_names = [request["name"] for request in requests]
            self.current_request.config(values=request_names)
            self.current_request.current(len(request_names) - 1)
            self.load_request("")
            json.dump(requests, open("data.json", "w"), indent=4)
            prompt.destroy()

        ctk.CTkButton(
            prompt,
            text="Create",
            corner_radius=10,
            text_font=("Acme", 12, "bold"),
            command=create_request,
        ).place(x=115, y=170, width=240, height=25)

    def load_request(self, args):
        curr_request = self.current_request.get()
        for i in self.data:
            if i["name"] == curr_request:
                self.url.delete(0, tk.END)
                self.url.insert(tk.END, i["url"])

                self.request_type.set(i["type"])

                self.headers_input.delete(1.0, tk.END)
                self.headers_input.insert(tk.END, i["headers"])

                self.body_input.delete(1.0, tk.END)
                self.body_input.insert(tk.END, i["body"])

                self.body_types.set(i["body_type"])
                break

    def save_request(self):
        curr_request = self.current_request.get()
        for i in self.data:
            if i["name"] == curr_request:
                i["url"] = self.url.get()
                i["type"] = self.request_type.get()
                i["headers"] = self.headers_input.get(1.0, tk.END)
                i["body"] = self.body_input.get(1.0, tk.END)
                i["body_type"] = self.body_types.get()
                break
        json.dump(self.data, open("data.json", "w"), indent=4)
        

if __name__ == "__main__":
    root = ctk.CTk()
    app = App(root)
    root.mainloop()
