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
import json
import os

from functools import partial

from telemetry import get_flight_data

class SettingsScreen(object):
    def __init__(self, master):
        self.master = master

        # create scrollable list for options
        self.container = ttk.Frame(self.master)
        self.canvas = tk.Canvas(self.container)
        self.scrollbar = ttk.Scrollbar(self.container, orient='vertical', command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            '<Configure>',
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox('all')
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # create buttons
        self.btn_frame = ttk.Frame(self.master, padding=(3,3,12,12))
        self.reload_btn = ttk.Button(self.btn_frame, text='Reload', command=self.reload_defaults)
        self.save_btn = ttk.Button(self.btn_frame, text='Save Config', command=self.save)
        self.load_btn = ttk.Button(self.btn_frame, text='Load Config', command=self.load)

        # create position spinners
        self.spinner_frame = ttk.Frame(self.master, padding=(3,3,12,12))
        self.xpos_var = tk.IntVar()
        self.xpos_var.set(25)
        self.xpos_spinner = ttk.Spinbox(self.spinner_frame, width=10, from_=0, to=10000, textvariable=self.xpos_var)
        self.ypos_var = tk.IntVar()
        self.ypos_var.set(500)
        self.ypos_spinner = ttk.Spinbox(self.spinner_frame, width=10, from_=0, to=10000, textvariable=self.ypos_var)

        # init class variables
        self.canvas_elements = {}
        self.craft_name = ''

        # place gui elements
        self.container.pack(fill='both', expand=True)

        self.btn_frame.pack()
        self.reload_btn.pack(side='left')
        self.save_btn.pack(side='left')
        self.load_btn.pack(side='left')

        self.spinner_frame.pack()
        ttk.Label(self.spinner_frame, text='X:').pack(side='left')
        self.xpos_spinner.pack(side='left')
        ttk.Label(self.spinner_frame, text='Y:').pack(side='left')
        self.ypos_spinner.pack(side='left')

        self.canvas.pack(side='left', fill='both', expand=True)
        self.scrollbar.pack(side='right', fill='y')


    def save(self):
        # only save if the craft name is known
        if self.craft_name:
            options = {}

            # iterate over all list elements
            for text, (enable_var, disp_var, unit_var, fmt_var, _, _, _, _) in self.canvas_elements.items():
                # only save if the parameter is enabled
                if enable_var.get():
                    options[text] = (disp_var.get(), unit_var.get(), fmt_var.get())

            global configs_base_path
            with open(os.path.join(configs_base_path, f'{self.craft_name}_hud.json'), 'w') as outf:
                json.dump(options, outf, indent=4)

    def load_name(self, fname):
        global configs_base_path

        fpath = os.path.join(configs_base_path, f'{fname}_hud.json')

        # check if craft specific config exists
        if os.path.exists(fpath):
            print(f'loading config for {fname}')
            with open(fpath, 'r') as inf:
                options = json.load(inf)

                for text, (disp, unit, fmt) in options.items():
                    try:
                        self.canvas_elements[text][0].set(1)
                        self.canvas_elements[text][1].set(disp)
                        self.canvas_elements[text][2].set(unit)
                        self.canvas_elements[text][3].set(fmt)
                    except:
                        # ignore exceptions, some elements might not be supported
                        pass

        # if not load default config
        elif fpath != 'default':
            print(f'no config for {fname} found, loading defaults')
            self.load_name('default')

        # if that also doesn't exist throw an error
        else:
            raise FileNotFoundError('default config file not found, check your installation')

    def load(self):
        self.reload()
        if self.craft_name:
            self.load_name(self.craft_name)

    def add_to_canvas(self, text):
        enable_var = tk.IntVar()
        disp_var = tk.StringVar()
        unit_var = tk.StringVar()
        fmt_var = tk.StringVar()

        # set default values for above vars
        disp_var.set(text)
        unit_var.set('')
        fmt_var.set('7.1f')

        # create user controls
        enable_chkbtn = ttk.Checkbutton(self.scrollable_frame, text=text, variable=enable_var)
        disp_entry = ttk.Entry(self.scrollable_frame, width=20, textvariable=disp_var)
        unit_entry = ttk.Entry(self.scrollable_frame, width=10, textvariable=unit_var)
        fmt_entry = ttk.Entry(self.scrollable_frame, width=10, textvariable=fmt_var)

        enable_chkbtn.grid(column=0, row=len(self.canvas_elements), sticky=tk.W)
        disp_entry.grid(column=1, row=len(self.canvas_elements))
        unit_entry.grid(column=2, row=len(self.canvas_elements))
        fmt_entry.grid(column=3, row=len(self.canvas_elements))

        # keep track of tk [int][string]Vars and widgets for later reference
        self.canvas_elements[text] = (enable_var, disp_var, unit_var, fmt_var, enable_chkbtn, disp_entry, unit_entry, fmt_entry)

    def destroy_canvas(self):
        # destroy the scrolling canvas gui elements, removing them from the actual UI
        for _, (_, _, _, _, enable_chkbtn, disp_entry, unit_entry, fmt_entry) in self.canvas_elements.items():
            enable_chkbtn.destroy()
            disp_entry.destroy()
            unit_entry.destroy()
            fmt_entry.destroy()

        # clear the dictionary
        self.canvas_elements.clear()

    def reload_defaults(self):
        self.reload()
        self.load_name('default')

    def reload(self):
        self.destroy_canvas()
        obj = get_flight_data()

        if obj:
            self.craft_name = obj['type']
            for k in obj.keys():
                self.add_to_canvas(k)

class HUDScreen(object):
    def __init__(self, master, canvas_elements, reload_fcn):
        self.master = master
        self.canvas_elements = canvas_elements
        self.reload_fcn = reload_fcn
        self.toplevel = tk.Toplevel(self.master)
        self.label = tk.Label(self.toplevel, text='Climb Rate', font=('Courier New', '14', 'bold'), fg='white', bg='black', justify=tk.LEFT)

        # make HUD transparent, non clickable and always-on-top
        self.toplevel.overrideredirect(True)
        self.toplevel.geometry('+25+500')
        self.toplevel.lift()
        self.toplevel.wm_attributes('-topmost', True)
        self.toplevel.wm_attributes('-disabled', True)
        self.toplevel.wm_attributes('-transparentcolor', 'black')

        self.data_valid = False
        self.was_valid = False

        hWindow = pywintypes.HANDLE(int(self.toplevel.frame(), 16))
        # http://msdn.microsoft.com/en-us/library/windows/desktop/ff700543(v=vs.85).aspx
        # The WS_EX_TRANSPARENT flag makes events (like mouse clicks) fall through the window.
        exStyle = win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT
        win32api.SetWindowLong(hWindow, win32con.GWL_EXSTYLE, exStyle)

        self.label.pack()

    def update(self):
        # hud update rate, update faster if data is valid
        rate = 1000
        label_text = ''

        obj = get_flight_data()

        if obj:
            rate = 100
            self.data_valid = True
            for var_name, (on, disp, unit, fmt, _, _, _, _) in self.canvas_elements.items():
                if on.get():
                    try:
                        label_text += f'{disp.get():<6}{obj[var_name]:{fmt.get()}} {unit.get()}\n'
                    except:
                        pass
        else:
            self.data_valid = False

        # on data valid change reload hud
        if self.was_valid == False and self.data_valid == True:
            self.reload_fcn()

        self.was_valid = self.data_valid
        self.label.config(text=label_text)

        # continue running hud updates
        self.master.after(rate, self.update)

    def set_size(self, x, y):
        self.toplevel.geometry(f'+{x}+{y}')

# get absolute path to this script, construct config paths
app_path = os.path.realpath(__file__)
configs_base_path = os.path.join(os.path.dirname(app_path), 'configs')
window_config_path = os.path.join(configs_base_path, 'window.json')

# create root Tk window
root = tk.Tk()
root.title('WTHUD Config')
root.minsize(430, 600)

# create settings and hud screens
app = SettingsScreen(root)
hud = HUDScreen(root, app.canvas_elements, app.load)

# lambda function to update the hud position directly from tk.IntVars
pos_updater = lambda a, b, c: hud.set_size(app.xpos_var.get(), app.ypos_var.get())

# register pos_updater to IntVars containing the hud position
app.xpos_var.trace('w', pos_updater)
app.ypos_var.trace('w', pos_updater)

# load hud position
with open(window_config_path, 'r') as inf:
    sizes = json.load(inf)
    app.xpos_var.set(sizes['xpos'])
    app.ypos_var.set(sizes['ypos'])

# begin hud updating
hud.update()

# start tk event loop
root.mainloop()

# save hud position
with open(window_config_path, 'w') as outf:
    json.dump({'xpos': app.xpos_var.get(), 'ypos': app.ypos_var.get()}, outf, indent=4)
