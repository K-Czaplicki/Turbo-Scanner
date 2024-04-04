import tkinter
import tkinter.messagebox
import customtkinter
from customtkinter import filedialog
import os
import time
import re

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Set title
        self.title("Turbo Scanner")
        
        # Default file containing targets
        self.selected_file = "ips.txt"

        # Set layout of the GUI
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Create left sidebar frame
        self.left_sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.left_sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.left_sidebar_frame.grid_rowconfigure(4, weight=1)
        
        # Create logo label
        self.logo_label = customtkinter.CTkLabel(self.left_sidebar_frame, text="Turbo Scanner", font=customtkinter.CTkFont(size=25, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Create "Load targets" button
        self.load_targets_button = customtkinter.CTkButton(self.left_sidebar_frame, command=self.load_targets_file, text="Load targets")
        self.load_targets_button.grid(row=1, column=0, padx=20, pady=10)
        
        # Create "Start scan" button
        self.start_scan_button = customtkinter.CTkButton(self.left_sidebar_frame, command=self.start_scan, text="Start scan")
        self.start_scan_button.grid(row=2, column=0, padx=20, pady=(10))

        # Create appearance mode label and option menu
        self.appearance_mode_label = customtkinter.CTkLabel(self.left_sidebar_frame, text="Appearance mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.left_sidebar_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(0, 10))

        # Create UI scaling label and option menu
        self.scaling_label = customtkinter.CTkLabel(self.left_sidebar_frame, text="UI scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.left_sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(0, 20))

        # Create authors labels
        self.created_by = customtkinter.CTkLabel(self.left_sidebar_frame, text="Created by:", font=customtkinter.CTkFont(size=14, weight="bold"))
        self.created_by.grid(row=9, column=0, padx=20, pady=(5, 5))
        self.authors = customtkinter.CTkLabel(self.left_sidebar_frame, text="Krzysztof Czaplicki\nMateusz Orzełowski", font=customtkinter.CTkFont(size=12))
        self.authors.grid(row=10, column=0, padx=20, pady=(0, 10))

        # Create main scrollable frame with list of targets and checkboxes for scanners
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="List of targets", label_font=customtkinter.CTkFont(size=20))
        self.scrollable_frame.grid(row=0, column=1, rowspan=3 ,padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_checkboxes1 = []
        self.scrollable_frame_checkboxes2 = []
        self.scrollable_frame_checkboxes3 = []
        self.scrollable_frame_checkboxes4 = []
        self.scrollable_frame_labels = []

        # Load targets from selected file
        self.refresh_displayed_targets()

        # Set default values for appearence mode and UI scaling
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")

        # Create right sidebar frame
        self.right_sidebar_frame = customtkinter.CTkFrame(self, width=300, corner_radius=0)
        self.right_sidebar_frame.grid(row=0, column=2, rowspan=4, sticky="nsew")
        self.right_sidebar_frame.grid_rowconfigure(4, weight=1)
        self.right_sidebar_frame.grid_propagate(False)
        self.right_sidebar_frame.columnconfigure(0, minsize=300)

        # Create entry field for email input
        self.entry = customtkinter.CTkEntry(self.right_sidebar_frame, placeholder_text="Enter your email")
        self.entry.grid(row=0, column=0, padx=(10, 10), pady=(20, 10), sticky="nsew")

        # Create submit button
        self.right_sidebar_button_1 = customtkinter.CTkButton(self.right_sidebar_frame, command=self.submit_mail, text="Submit")
        self.right_sidebar_button_1.grid(row=1, column=0, padx=20, pady=10,  sticky="nsew")
        
        # Create scrollable frame for displaying emails
        self.scrollable_frame_right = customtkinter.CTkScrollableFrame(self.right_sidebar_frame, label_text="Mailing list", label_font=customtkinter.CTkFont(size=20))
        self.scrollable_frame_right.grid(row=4, column=0, padx=(5, 5), pady=(20, 20), sticky="nsew")
        self.scrollable_frame_right.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_right_buttons = []
        self.scrollable_frame_right_emails = []
        self.refresh_mails()
            
    # Open file input dialog
    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())
    
    # Change appearance mode
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    # Change UI scaling mode
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    # Submit email if it is valid and clear entry field
    def submit_mail(self):
        text = self.entry.get()
        if (is_valid_email(text)):
            with open("mails.txt", "a") as f:
                f.write("\n" + text)
            self.entry.delete(0, tkinter.END)
            self.refresh_mails()

    # Clear any existing emails and display newly loaded ones
    def refresh_mails(self):
        for button in self.scrollable_frame_right_buttons:
            button.destroy()
        self.scrollable_frame_right_buttons.clear()
        for email in self.scrollable_frame_right_emails:
            email.destroy()
        self.scrollable_frame_right_emails.clear()

        i = 0
        with open("mails.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                email = line.strip()
                # Check if the email is valid
                if (is_valid_email(email) != True):
                    # Skip invalid emails
                    continue
                
                button = customtkinter.CTkButton(master=self.scrollable_frame_right, text="X", width=15, height=15, command=lambda email=email: self.remove_and_refresh_mails(email))
                button.grid(row=i, column=0, padx=(5, 20), pady=(0, 20), sticky="w")
                self.scrollable_frame_right_buttons.append(button)
                
                email_label = customtkinter.CTkLabel(master=self.scrollable_frame_right, text=email)
                email_label.grid(row=i, column=0, padx=(35, 5), pady=(0, 20), sticky="w")
                self.scrollable_frame_right_emails.append(email_label)
                
                # Increment index counter for valid emails
                i += 1

    # Remove an email and update mailing list
    def remove_and_refresh_mails(self, line):
        with open("mails.txt", "r") as f:
            lines = f.readlines()
        with open("mails.txt", "w") as f:
            for l in lines:
                if (l == "\n"):
                    continue
                if l.strip() != line.strip():
                    f.write(l)
        self.refresh_mails()
        
    # Start scan with selected options
    def start_scan(self):
        # create sidebar frame with widgets
        self.start_scan_button.configure(text="Scanning...")
        color = self.start_scan_button._fg_color
        self.start_scan_button.configure(fg_color="red")
        self.start_scan_button.configure(hover=False)
        self.update()

        for i in range(len(self.scrollable_frame_checkboxes1)):
            target = (self.scrollable_frame_labels[i]._text).split(' ')[6]    # TODO fix nie na sztywno
    
            # WPPen
            if(self.scrollable_frame_checkboxes2[i].get()):
                os.system("mkdir "+target.replace('://', ''))
                print('Starting WPPen for: '+target)
                print("-> python wppen.py "+target+" > "+target.replace('://', '')+"/wppen.txt")
                os.system("python wppen.py "+target+" > "+target.replace('://', '')+"/wppen.txt")

            # ZAP
            if(self.scrollable_frame_checkboxes4[i].get()):
                os.system("mkdir "+target.replace('://', ''))
                print('Starting ZAP for: '+target)
                print("-> sudo docker run -v $(pwd)/"+target.replace('://', '')+"/:/zap/wrk/:rw -t ghcr.io/zaproxy/zaproxy:stable zap-baseline.py -t "+target+" -r zap_report.html")
                # zap-full-scan.py    <- podmień jeśli chcesz pełny skan
                os.system("echo 'skaner' | sudo -S docker run -v $(pwd)/"+target.replace('://', '')+"/:/zap/wrk/:rw -t ghcr.io/zaproxy/zaproxy:stable zap-baseline.py -t "+target+" -r zap_report.html")
            
            # Artemis
            if(self.scrollable_frame_checkboxes3[i].get()):
                os.system("mkdir "+target.replace('://', ''))
                print('Starting Artemis for: '+target)
                print('python artemis.py ' + target)
                os.system('python artemis.py ' + target)

            # OpenVAS
            if(self.scrollable_frame_checkboxes1[i].get()):
                os.system("mkdir "+target.replace('://', ''))
                print('Starting OpenVAS for: '+target)

        self.start_scan_button.configure(text="Start scan")
        self.start_scan_button.configure(fg_color=color)
        self.start_scan_button.configure(hover=True)
        self.update()

    def load_targets_file(self):
        self.selected_file = filedialog.askopenfilename(filetypes=(('text files', '.txt'),))
        self.refresh_displayed_targets()

    # Clear any existing targets and display newly loaded ones 
    def refresh_displayed_targets(self):
        for label in self.scrollable_frame_labels:
            label.destroy()
        self.scrollable_frame_labels.clear()

        for checkbox_list in [self.scrollable_frame_checkboxes1, self.scrollable_frame_checkboxes2,
                        self.scrollable_frame_checkboxes3, self.scrollable_frame_checkboxes4]:
            for checkbox in checkbox_list:
                checkbox.destroy()
            checkbox_list.clear()

        # Reset index counters
        i = 0
        
        with open(self.selected_file, "r") as f:
            lines = f.readlines()
            for line in lines:
                target = line.strip()
                
                # Check if the target is valid
                if not target or not (re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', target) 
                                      or target.startswith("http://") 
                                      or target.startswith("https://")):
                    # Skip invalid targets
                    continue

                # Increment index counter for valid targets
                i += 1

                # Display valid targets
                label_text = f"{i}.     {target}"
                label = customtkinter.CTkLabel(master=self.scrollable_frame, text=label_text, font=customtkinter.CTkFont(size=15))
                label.grid(row=i-1, column=0, padx=20, pady=(0, 10), sticky="w")
                self.scrollable_frame_labels.append(label)

                checkbox1 = customtkinter.CTkCheckBox(master=self.scrollable_frame, text="OpenVas", font=customtkinter.CTkFont(size=15))
                checkbox1.grid(row=i-1, column=1, padx=10, pady=(0, 10))
                self.scrollable_frame_checkboxes1.append(checkbox1)

                if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', target):
                    # Enable only OpenVas checkbox for IPs
                    checkbox2 = customtkinter.CTkCheckBox(master=self.scrollable_frame, text="WPPen", font=customtkinter.CTkFont(size=15), state="disabled")
                    checkbox2.grid(row=i-1, column=2, padx=10, pady=(0, 10))
                    self.scrollable_frame_checkboxes2.append(checkbox2)

                    checkbox3 = customtkinter.CTkCheckBox(master=self.scrollable_frame, text="Artemis", font=customtkinter.CTkFont(size=15), state="disabled")
                    checkbox3.grid(row=i-1, column=3, padx=10, pady=(0, 10))
                    self.scrollable_frame_checkboxes3.append(checkbox3)

                    checkbox4 = customtkinter.CTkCheckBox(master=self.scrollable_frame, text="Zap", font=customtkinter.CTkFont(size=15), state="disabled")
                    checkbox4.grid(row=i-1, column=4, padx=10, pady=(0, 10))
                    self.scrollable_frame_checkboxes4.append(checkbox4)
                else:
                    # Enable all checkboxes for URLs
                    checkbox2 = customtkinter.CTkCheckBox(master=self.scrollable_frame, text="WPPen", font=customtkinter.CTkFont(size=15))
                    checkbox2.grid(row=i-1, column=2, padx=10, pady=(0, 10))
                    self.scrollable_frame_checkboxes2.append(checkbox2)

                    checkbox3 = customtkinter.CTkCheckBox(master=self.scrollable_frame, text="Artemis", font=customtkinter.CTkFont(size=15))
                    checkbox3.grid(row=i-1, column=3, padx=10, pady=(0, 10))
                    self.scrollable_frame_checkboxes3.append(checkbox3)

                    checkbox4 = customtkinter.CTkCheckBox(master=self.scrollable_frame, text="Zap", font=customtkinter.CTkFont(size=15))
                    checkbox4.grid(row=i-1, column=4, padx=10, pady=(0, 10))
                    self.scrollable_frame_checkboxes4.append(checkbox4)

# Check if email format is correct
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

if __name__ == "__main__":
    app = App()
    app.minsize(1300, 440)
    app.geometry("{0}x{1}+0+0".format(app.winfo_screenwidth()-10,app.winfo_screenheight()-70))
    app.mainloop()
