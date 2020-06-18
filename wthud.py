# wthud - Head-up Display for War Thunder
# Copyright (C) 2020 wysiwyng
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# Main graphics functions

import tkinter as tk
from tkinter import ttk

import win32api, win32con, pywintypes
from telemetry import get_flight_data
import json

class SettingsScreen(object):
    def __init__(self, master):
        self.master = master
        self.container = ttk.Frame(self.master)
        self.canvas = tk.Canvas(self.container)
        self.scrollbar = ttk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)

        self.btn_frame = ttk.Frame(self.master)
        self.reload_btn = ttk.Button(self.btn_frame, text='Reload', command=self.reload)
        self.save_btn = ttk.Button(self.btn_frame, text='Save Config', command=self.save)
        self.load_btn = ttk.Button(self.btn_frame, text='Load Config', command=self.load)

        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas_elements = {}
        self.craft_name = ''

        self.container.pack(fill="both", expand=True)
        self.btn_frame.pack()
        self.reload_btn.pack(side="left")
        self.save_btn.pack(side="left")
        self.load_btn.pack(side="left")


        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")


    def save(self):
        if self.craft_name:
            options = {}
            for text, (enable, disp, unit, _, _, _) in self.canvas_elements.items():
                if enable.get():
                    options[text] = (disp.get(), unit.get())
            with open(f'configs/{self.craft_name}_hud.json', 'w') as outf:
                json.dump(options, outf)
        pass

    def load(self):
        self.reload()
        if self.craft_name:
            with open(f'configs/{self.craft_name}_hud.json', 'r') as inf:
                options = json.load(inf)

                for text, (disp, unit) in options.items():
                    self.canvas_elements[text][0].set(1)
                    self.canvas_elements[text][1].set(disp)
                    self.canvas_elements[text][2].set(unit)
            pass

    def add_to_canvas(self, text):
        enable = tk.IntVar()
        disp = tk.StringVar()
        unit = tk.StringVar()
        disp.set(text)
        unit.set('')

        cb = ttk.Checkbutton(self.scrollable_frame, text=text, variable=enable)
        e = ttk.Entry(self.scrollable_frame, width=20, textvariable=disp)
        e2 = ttk.Entry(self.scrollable_frame, width=20, textvariable=unit)

        cb.grid(column=0, row=len(self.canvas_elements), sticky=tk.W)
        e.grid(column=1, row=len(self.canvas_elements))
        e2.grid(column=2, row=len(self.canvas_elements))

        #self.canvas_elements.append((enable, disp, unit, text, cb, e, e2))
        self.canvas_elements[text] = (enable, disp, unit, cb, e, e2)

    def destroy_canvas(self):
        for _, (_, _, _, cb, e, e2) in self.canvas_elements.items():
            cb.destroy()
            e.destroy()
            e2.destroy()

        self.canvas_elements.clear()

    def reload(self):
        self.destroy_canvas()
        obj = get_flight_data()

        if obj:
            self.craft_name = obj['type']
            for k, v in obj.items():
                self.add_to_canvas(k)

class HUDScreen(object):
    def __init__(self, master, canvas_elements):
        self.master = master
        self.canvas_elements = canvas_elements
        self.toplevel = tk.Toplevel(self.master)
        self.label = tk.Label(self.toplevel, text='Climb Rate', font=('Courier New', '14', 'bold'), fg='white', bg='black', justify=tk.LEFT)
        self.toplevel.overrideredirect(True)
        self.toplevel.geometry("+25+500")
        self.toplevel.lift()
        self.toplevel.wm_attributes("-topmost", True)
        self.toplevel.wm_attributes("-disabled", True)
        self.toplevel.wm_attributes("-transparentcolor", "black")

        hWindow = pywintypes.HANDLE(int(self.toplevel.frame(), 16))
        # http://msdn.microsoft.com/en-us/library/windows/desktop/ff700543(v=vs.85).aspx
        # The WS_EX_TRANSPARENT flag makes events (like mouse clicks) fall through the window.
        exStyle = win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT
        win32api.SetWindowLong(hWindow, win32con.GWL_EXSTYLE, exStyle)

        self.label.pack()

    def update(self):
        rate = 1000
        label_text = ''

        obj = get_flight_data()
        try:
            if obj:
                rate = 100
                for var_name, (on, disp, unit, _, _, _) in self.canvas_elements.items():
                    if on.get():
                        label_text += f'{disp.get():<10}{obj[var_name]:7.1f} {unit.get()}\n'
        except:
            pass

        self.label.config(text=label_text)

        self.master.after(rate, self.update)


root = tk.Tk()

app = SettingsScreen(root)
hud = HUDScreen(root, app.canvas_elements)
hud.update()

root.mainloop()
