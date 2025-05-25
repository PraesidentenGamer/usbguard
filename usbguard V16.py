import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import ctypes
import wmi
import wmi
import time
import os
import threading
import time

class USBGuardApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("USBGuard V16 - USB Laufwerksverwaltung")
        self.geometry("900x600")

        # Sprache: 'DE' oder 'EN'
        self.language = 'DE'

        # Whitelist (Laufwerksbuchstaben Großbuchstaben, z.B. ['E', 'F'])
        self.whitelist = []

        # Adminrechte prüfen
        self.is_admin = self.check_admin()

        # WMI Objekt
        self.wmi_obj = wmi.WMI()

        # GUI Setup
        self.create_widgets()

        self.log(self.tr("Programm gestartet."))
        self.log(self.tr(f"Adminrechte: {'Ja' if self.is_admin else 'Nein'}"))

        self.update_usb_drives()
        self.update_hide_drives()

    def tr(self, text):
        # Übersetzungen (sehr einfach, erweiterbar)
        translations = {
            "Programm gestartet.": {"EN": "Program started."},
            "Adminrechte: Ja": {"EN": "Admin rights: Yes"},
            "Adminrechte: Nein": {"EN": "Admin rights: No"},
            "Gefundene USB-Wechseldatenträger:": {"EN": "Detected USB removable drives:"},
            "Keine USB-Wechseldatenträger gefunden.": {"EN": "No USB removable drives found."},
            "Laufwerke wurden versteckt. Bitte Explorer neu starten (oder abmelden) für Änderung.": {"EN": "Drives have been hidden. Please restart Explorer (or log off) to apply changes."},
            "Alle Laufwerke werden jetzt im Explorer angezeigt. Bitte Explorer neu starten (oder abmelden).": {"EN": "All drives are now visible in Explorer. Please restart Explorer (or log off)."},
            "Whitelist (Laufwerksbuchstaben):": {"EN": "Whitelist (Drive letters):"},
            "Log:": {"EN": "Log:"},
            "Nicht-Whitelist Laufwerke verstecken": {"EN": "Hide non-whitelist drives"},
            "USB Laufwerke aktualisieren": {"EN": "Refresh USB drives"},
            "Alle Laufwerke anzeigen": {"EN": "Show all drives"},
            "Whitelist Laufwerk hinzufügen": {"EN": "Add whitelist drive"},
            "Whitelist Laufwerk entfernen": {"EN": "Remove whitelist drive"},
            "Adminrechte benötigt": {"EN": "Admin rights required"},
            "Um Laufwerke auszublenden, bitte das Programm mit Administratorrechten neu starten.": {"EN": "To hide drives, please restart the program with administrator rights."},
            "Um Laufwerke wieder anzuzeigen, bitte das Programm mit Administratorrechten neu starten.": {"EN": "To show drives again, please restart the program with administrator rights."},
            "Fehler beim Auslesen der Laufwerke:": {"EN": "Error reading drives:"},
            "FEHLER: Keine Adminrechte. Laufwerke können nicht versteckt werden.": {"EN": "ERROR: No admin rights. Cannot hide drives."},
            "FEHLER: Keine Adminrechte. Laufwerke können nicht eingeblendet werden.": {"EN": "ERROR: No admin rights. Cannot show drives."},
            "Keine Laufwerke zum Verstecken gefunden.": {"EN": "No drives to hide found."},
            "Alle Laufwerke sind auf der Whitelist. Keine Versteckaktion nötig.": {"EN": "All drives are whitelisted. No hiding needed."},
            "Info": {"EN": "Info"},
            "Fehler": {"EN": "Error"},
            "Bitte einen einzelnen Buchstaben A-Z eingeben.": {"EN": "Please enter a single letter A-Z."},
            "Laufwerk {drive} ist bereits auf der Whitelist.": {"EN": "Drive {drive} is already whitelisted."},
            "Laufwerk {drive} zur Whitelist hinzugefügt.": {"EN": "Drive {drive} added to whitelist."},
            "Laufwerk {drive} von der Whitelist entfernt.": {"EN": "Drive {drive} removed from whitelist."},
            "Laufwerk {drive} ist nicht auf der Whitelist.": {"EN": "Drive {drive} is not in the whitelist."},
            "Laufwerke {drives} wurden im Explorer versteckt. (NoDrives=0x{mask:X})": {"EN": "Drives {drives} have been hidden in Explorer. (NoDrives=0x{mask:X})"},
            "Gefundene USB-Wechseldatenträger": {"EN": "Detected USB removable drives"},
            "Sprache gewechselt.": {"EN": "Language switched."},
            # Weitere Übersetzungen können hier hinzugefügt werden
        }

        if text in translations and self.language == 'EN':
            # Ersetze evtl. Platzhalter {drive}, {drives}, {mask:X}
            if '{drive}' in text or '{drives}' in text or '{mask:X}' in text:
                return translations[text]['EN'].format(drive=getattr(self, 'last_drive', ''),
                                                       drives=getattr(self, 'last_drives', ''),
                                                       mask=getattr(self, 'last_mask', 0))
            return translations[text]['EN']
        return text

    def check_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            return False

    def create_widgets(self):
        # Sprache wechseln Button
        frame_lang = ttk.Frame(self)
        frame_lang.pack(fill='x', padx=10, pady=3)
        self.btn_lang = ttk.Button(frame_lang, text="Switch to English" if self.language == 'DE' else "Wechsel zu Deutsch", command=self.toggle_language)
        self.btn_lang.pack(anchor='e')

        # Frame für Buttons oben
        self.frame_top = ttk.Frame(self)
        self.frame_top.pack(fill='x', padx=10, pady=5)

        self.btn_refresh = ttk.Button(self.frame_top, text=self.tr("USB Laufwerke aktualisieren"), command=self.update_usb_drives)
        self.btn_refresh.pack(side='left', padx=5)

        self.btn_hide = ttk.Button(self.frame_top, text=self.tr("Nicht-Whitelist Laufwerke verstecken"), command=self.update_hide_drives)
        self.btn_hide.pack(side='left', padx=5)

        self.btn_show_all = ttk.Button(self.frame_top, text=self.tr("Alle Laufwerke anzeigen"), command=self.show_all_drives)
        self.btn_show_all.pack(side='left', padx=5)

        self.btn_add_whitelist = ttk.Button(self.frame_top, text=self.tr("Whitelist Laufwerk hinzufügen"), command=self.add_whitelist)
        self.btn_add_whitelist.pack(side='left', padx=5)

        self.btn_remove_whitelist = ttk.Button(self.frame_top, text=self.tr("Whitelist Laufwerk entfernen"), command=self.remove_whitelist)
        self.btn_remove_whitelist.pack(side='left', padx=5)

        # Frame für Liste und Log
        frame_main = ttk.Frame(self)
        frame_main.pack(fill='both', expand=True, padx=10, pady=5)

        # USB Laufwerke Liste (mit Scrollbar)
        lbl_usb = ttk.Label(frame_main, text=self.tr("Gefundene USB-Wechseldatenträger:"))
        lbl_usb.pack(anchor='w')

        self.tree_usb = ttk.Treeview(frame_main, columns=("drive", "volume", "manufacturer", "pnpid", "serial", "size_total", "size_free", "filesystem"), show='headings')
        self.tree_usb.pack(fill='both', expand=True)

        headings = {
            "drive": "Laufwerksbuchstabe" if self.language == 'DE' else "Drive Letter",
            "volume": "Name" if self.language == 'DE' else "Volume Name",
            "manufacturer": "Hersteller" if self.language == 'DE' else "Manufacturer",
            "pnpid": "PNPDeviceID",
            "serial": "Seriennummer" if self.language == 'DE' else "Serial Number",
            "size_total": "Speichergröße" if self.language == 'DE' else "Total Size",
            "size_free": "Freier Speicher" if self.language == 'DE' else "Free Space",
            "filesystem": "Format" if self.language == 'DE' else "File System",
        }

        for col, text in headings.items():
            self.tree_usb.heading(col, text=text)
            self.tree_usb.column(col, anchor='center')

        # Whitelist Anzeige
        lbl_whitelist = ttk.Label(frame_main, text=self.tr("Whitelist (Laufwerksbuchstaben):"))
        lbl_whitelist.pack(anchor='w', pady=(10,0))

        self.whitelist_var = tk.StringVar(value=", ".join(self.whitelist))
        self.whitelist_label = ttk.Label(frame_main, textvariable=self.whitelist_var)
        self.whitelist_label.pack(anchor='w')

        # Log Bereich
        lbl_log = ttk.Label(frame_main, text=self.tr("Log:"))
        lbl_log.pack(anchor='w', pady=(10,0))

        self.text_log = tk.Text(frame_main, height=10, state='disabled', wrap='word')
        self.text_log.pack(fill='both', expand=True)

        # Scrollbar für Log
        scrollbar = ttk.Scrollbar(frame_main, command=self.text_log.yview)
        self.text_log.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

    def log(self, message):
        self.text_log.configure(state='normal')
        self.text_log.insert('end', message + "\n")
        self.text_log.see('end')
        self.text_log.configure(state='disabled')

    def update_usb_drives(self):
        self.tree_usb.delete(*self.tree_usb.get_children())
        try:
            drives = self.get_usb_drives()
            if not drives:
                self.log(self.tr("Keine USB-Wechseldatenträger gefunden."))
                return
            for d in drives:
                self.tree_usb.insert('', 'end', values=(
                    d['DriveLetter'],
                    d['VolumeName'],
                    d['Manufacturer'],
                    d['PNPDeviceID'],
                    d['SerialNumber'],
                    d['SizeTotal'],
                    d['SizeFree'],
                    d['FileSystem'],
                ))
            self.log(self.tr("Gefundene USB-Wechseldatenträger:"))
            self.last_drives = ", ".join([d['DriveLetter'] for d in drives])
        except Exception as e:
            self.log(f"{self.tr('Fehler beim Auslesen der Laufwerke:')} {e}")

        # Update Whitelist Anzeige
        self.whitelist_var.set(", ".join(self.whitelist))

    def get_usb_drives(self):
        drives = []
        # Suche alle Wechseldatenträger mit WMI
        try:
            for disk in self.wmi_obj.Win32_DiskDrive():
                if disk.MediaType and "Removable Media" in disk.MediaType:
                    # Verbundene Partitionen und Laufwerke abfragen
                    for partition in disk.associators("Win32_DiskDriveToDiskPartition"):
                        for logical_disk in partition.associators("Win32_LogicalDiskToPartition"):
                            drive_letter = logical_disk.DeviceID
                            if not drive_letter:
                                continue
                            drive_letter = drive_letter.rstrip(':')
                            # Info sammeln
                            volume_name = logical_disk.VolumeName or ""
                            fs = logical_disk.FileSystem or ""
                            size_total = int(logical_disk.Size or 0)
                            size_free = int(logical_disk.FreeSpace or 0)
                            # Hersteller, Seriennummer
                            manufacturer = disk.Manufacturer or ""
                            pnpid = disk.PNPDeviceID or ""
                            serial = self.get_serial_from_pnpid(pnpid)

                            drives.append({
                                'DriveLetter': drive_letter,
                                'VolumeName': volume_name,
                                'Manufacturer': manufacturer,
                                'PNPDeviceID': pnpid,
                                'SerialNumber': serial,
                                'SizeTotal': self.format_bytes(size_total),
                                'SizeFree': self.format_bytes(size_free),
                                'FileSystem': fs,
                            })
            return drives
        except Exception as e:
            raise e

    def get_serial_from_pnpid(self, pnpid):
        # Extrahiere Seriennummer aus PNPDeviceID falls möglich
        # Beispiel: USBSTOR\DISK&VEN_SANDISK&PROD_ULTRA&REV_1.00\4C530001230416105283&0
        try:
            if pnpid:
                parts = pnpid.split('\\')
                if len(parts) > 2:
                    serial = parts[2]
                    # Seriennummer ist der Teil vor dem '&' (manchmal)
                    serial = serial.split('&')[0]
                    return serial
        except:
            pass
        return ""

    def format_bytes(self, size):
        # Formatiert Bytes in lesbare Form
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} TB"

    def update_hide_drives(self):
        if not self.is_admin:
            messagebox.showerror(self.tr("Fehler"), self.tr("FEHLER: Keine Adminrechte. Laufwerke können nicht versteckt werden."))
            self.log(self.tr("FEHLER: Keine Adminrechte. Laufwerke können nicht versteckt werden."))
            return

        # Hole alle Laufwerke auf dem System (Buchstaben)
        all_drives = self.get_all_drive_letters()

        # Nicht-Whitelist-Laufwerke ermitteln
        drives_to_hide = [d for d in all_drives if d not in self.whitelist]

        if not drives_to_hide:
            self.log(self.tr("Alle Laufwerke sind auf der Whitelist. Keine Versteckaktion nötig."))
            messagebox.showinfo(self.tr("Info"), self.tr("Alle Laufwerke sind auf der Whitelist. Keine Versteckaktion nötig."))
            return

        # Setze Registry für NoDrives
        mask = 0
        for d in drives_to_hide:
            pos = ord(d.upper()) - ord('A')
            mask |= (1 << pos)

        self.last_drives = ", ".join(drives_to_hide)
        self.last_mask = mask

        # Registry-Pfad und Wert
        import winreg
        reg_path = r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer"

        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_SET_VALUE)
        except FileNotFoundError:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path)

        winreg.SetValueEx(key, "NoDrives", 0, winreg.REG_DWORD, mask)
        winreg.CloseKey(key)

        self.log(self.tr("Laufwerke {drives} wurden im Explorer versteckt. (NoDrives=0x{mask:X})"))
        messagebox.showinfo(self.tr("Info"), self.tr("Laufwerke wurden versteckt. Bitte Explorer neu starten (oder abmelden) für Änderung."))

    def show_all_drives(self):
        if not self.is_admin:
            messagebox.showerror(self.tr("Fehler"), self.tr("FEHLER: Keine Adminrechte. Laufwerke können nicht eingeblendet werden."))
            self.log(self.tr("FEHLER: Keine Adminrechte. Laufwerke können nicht eingeblendet werden."))
            return

        import winreg
        reg_path = r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer"

        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_SET_VALUE)
        except FileNotFoundError:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path)

        winreg.SetValueEx(key, "NoDrives", 0, winreg.REG_DWORD, 0)
        winreg.CloseKey(key)

        self.log(self.tr("Alle Laufwerke werden jetzt im Explorer angezeigt. Bitte Explorer neu starten (oder abmelden)."))
        messagebox.showinfo(self.tr("Info"), self.tr("Alle Laufwerke werden jetzt im Explorer angezeigt. Bitte Explorer neu starten (oder abmelden)."))

    def get_all_drive_letters(self):
        # Liefert alle Laufwerksbuchstaben (A-Z) als Liste
        import string
        drives = []
        bitmask = ctypes.cdll.kernel32.GetLogicalDrives()
        for i in range(26):
            if bitmask & (1 << i):
                drives.append(chr(ord('A') + i))
        return drives

    def add_whitelist(self):
        answer = simpledialog.askstring(self.tr("Whitelist Laufwerk hinzufügen"), self.tr("Bitte einen einzelnen Buchstaben A-Z eingeben."))
        if not answer:
            return
        drive = answer.strip().upper()
        if len(drive) != 1 or drive < 'A' or drive > 'Z':
            messagebox.showerror(self.tr("Fehler"), self.tr("Bitte einen einzelnen Buchstaben A-Z eingeben."))
            return
        if drive in self.whitelist:
            messagebox.showinfo(self.tr("Info"), self.tr("Laufwerk {drive} ist bereits auf der Whitelist.").format(drive=drive))
            return
        self.whitelist.append(drive)
        self.whitelist_var.set(", ".join(self.whitelist))
        self.last_drive = drive
        self.log(self.tr("Laufwerk {drive} zur Whitelist hinzugefügt.").format(drive=drive))

    def remove_whitelist(self):
        answer = simpledialog.askstring(self.tr("Whitelist Laufwerk entfernen"), self.tr("Bitte einen einzelnen Buchstaben A-Z eingeben."))
        if not answer:
            return
        drive = answer.strip().upper()
        if len(drive) != 1 or drive < 'A' or drive > 'Z':
            messagebox.showerror(self.tr("Fehler"), self.tr("Bitte einen einzelnen Buchstaben A-Z eingeben."))
            return
        if drive not in self.whitelist:
            messagebox.showinfo(self.tr("Info"), self.tr("Laufwerk {drive} ist nicht auf der Whitelist.").format(drive=drive))
            return
        self.whitelist.remove(drive)
        self.whitelist_var.set(", ".join(self.whitelist))
        self.last_drive = drive
        self.log(self.tr("Laufwerk {drive} von der Whitelist entfernt.").format(drive=drive))

    def toggle_language(self):
        self.language = 'EN' if self.language == 'DE' else 'DE'
        self.btn_lang.config(text="Switch to English" if self.language == 'DE' else "Wechsel zu Deutsch")

        # Text der Buttons aktualisieren
        self.btn_refresh.config(text=self.tr("USB Laufwerke aktualisieren"))
        self.btn_hide.config(text=self.tr("Nicht-Whitelist Laufwerke verstecken"))
        self.btn_show_all.config(text=self.tr("Alle Laufwerke anzeigen"))
        self.btn_add_whitelist.config(text=self.tr("Whitelist Laufwerk hinzufügen"))
        self.btn_remove_whitelist.config(text=self.tr("Whitelist Laufwerk entfernen"))

        # Überschriften Treeview
        headings = {
            "drive": "Laufwerksbuchstabe" if self.language == 'DE' else "Drive Letter",
            "volume": "Name" if self.language == 'DE' else "Volume Name",
            "manufacturer": "Hersteller" if self.language == 'DE' else "Manufacturer",
            "pnpid": "PNPDeviceID",
            "serial": "Seriennummer" if self.language == 'DE' else "Serial Number",
            "size_total": "Speichergröße" if self.language == 'DE' else "Total Size",
            "size_free": "Freier Speicher" if self.language == 'DE' else "Free Space",
            "filesystem": "Format" if self.language == 'DE' else "File System",
        }
        for col, text in headings.items():
            self.tree_usb.heading(col, text=text)

        # Labels aktualisieren
        for widget in self.winfo_children():
            widget.destroy()
        self.create_widgets()
        self.update_usb_drives()
        self.log(self.tr("Sprache gewechselt."))

def list_usb_devices():
    c = wmi.WMI()
    usb_devices = []
    for usb in c.Win32_USBHub():
        usb_devices.append({
            "DeviceID": usb.DeviceID,
            "PNPDeviceID": usb.PNPDeviceID,
            "Description": usb.Description
        })
    return usb_devices

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def list_usb_devices():
    c = wmi.WMI()
    usb_devices = []
    for usb in c.Win32_USBHub():
        usb_devices.append({
            "DeviceID": usb.DeviceID,
            "PNPDeviceID": usb.PNPDeviceID,
            "Description": usb.Description
        })
    return usb_devices

def usb_loop():
    try:
        while True:
            devices = list_usb_devices()
            clear_console()

            if devices:
                print("Aktuelle USB-Geräte:")
                for d in devices:
                    print(f"Beschreibung: {d['Description']}")
                    print(f"DeviceID: {d['DeviceID']}")
                    print(f"PNPDeviceID: {d['PNPDeviceID']}")
                    print("-" * 40)
            else:
                print("Keine USB-Geräte gefunden.")

            time.sleep(1)

    except KeyboardInterrupt:
        print("\nProgramm beendet.")

if __name__ == "__main__":
    # Starte die USB-Überprüfung im Hintergrund (daemon=True, damit Thread mit dem Hauptprogramm endet)
    threading.Thread(target=usb_loop, daemon=True).start()

    # Starte die GUI
    app = USBGuardApp()
    app.mainloop()