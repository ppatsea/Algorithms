# Εισαγωγή απαραίτητων βιβλιοθηκών
import tkinter as tk                # tkinter : Δημιουργία Γραφικού Περιβάλλοντος - Παραθύρου
from tkinter import ttk
from tkinter import messagebox

from urllib.error import HTTPError  # urllib.error.HTTPError : Χρησιμοποιείται για την αντιμετώπιση σφαλμάτων που προκύπτουν κατά την ανάκτηση πόρων από δικτυακούς τόπους
from io import StringIO             # io.StringIO : Χρησιμοποιείται για να διαχειριστεί κείμενο ως αρχείο, δημιουργώντας ένα αρχείο-κατακερματισμό στη μνήμη

import requests                     # requests : Ανάγνωση Δεδομένων από URL

import matplotlib.pyplot as plot    # matplotlib.pyplot : Για τη Δημιουργία Διαγραμμάτων

import pandas as pd                 # pandas : Επεξεργασία Δεδομένων

import pfsp                         # pfsp : Κλήση κώδικα, όπου υλοποιείται το πρόβλημα Permutation Flow-shop Scheduling Problem

# import seaborn as sns               # seaborn : Χρησιμοποιείται συνδυαστικά με τη matplotlib για την επικοινωνία με γραφικές παραστάσεις



# Δημιουργία Λίστας, με τα Διαθέσιμα Αρχεία που θα εμφανίζονται στην μπάρα επιλογής του Παραθύρου (Combo Box)
comboboxvals = ('001',
                '002',
                '003',
                '004',
                '005',
                '006',
                '007',
                '008',
                '009',
                '010',
                '011',
                '012',
                '013',
                '014',
                '015',
                '016',
                '017',
                '018',
                '019',
                '020',
                '021',
                '022',
                '023',
                '024',
                '025',
                '026',
                '027',
                '028',
                '029',
                '030',
                '031',
                '032',
                '033',
                '034',
                '035',
                '036',
                '037',
                '038',
                '039',
                '040',
                '041',
                '042',
                '043',
                '044',
                '045',
                '046',
                '047',
                '048',
                '049',
                '050',
                '051',
                '052',
                '053',
                '054',
                '055',
                '056',
                '057',
                '058',
                '059',
                '060',
                '061',
                '062',
                '063',
                '064',
                '065',
                '066',
                '067',
                '068',
                '069',
                '070',
                '071',
                '072',
                '073',
                '074',
                '075',
                '076',
                '077',
                '078',
                '079',
                '080',
                '081',
                '082',
                '083',
                '084',
                '085',
                '086',
                '087',
                '088',
                '089',
                '090',
                '091',
                '092',
                '093',
                '094',
                '095',
                '096',
                '097',
                '098',
                '099',
                '100',
                '101',
                '102',
                '103',
                '104',
                '105',
                '106',
                '107',
                '108',
                '109',
                '110',
                '111',
                '112',
                '113',
                '114',
                '115',
                '116',
                '117',
                '118',
                '119',
                '120')



# Δημιουργία μια υπό-κλάσης, της κλάσης Tkinter, για το γραφικό περιβάλλον.
class WindowApp(tk.Tk):
    def __init__(self) -> None:                               # Καθορισμός ιδιοτήτων παραθύρου (τίτλος, διαστάσεις, ανακατανομή)
        super().__init__()


        self.title("Ερώτημα ως προς το Χρήστη")               # Τίτλος Παράθυρου
        self.geometry("500x350")                              # Διαστάσεις Παραθύρου
        self.resizable(width = False, height = False)         # Σταθερό Μέγέθος Παραθύρου
         


        ttk.Label(self, text = "Πρόβλημα PFSP",               # Kείμενο Eτικέτας για τον Tίτλο
            background = 'black', foreground = 'turquoise',   # Χρώμα Γραμματοσειράς & Υπογράμμισή της
            font = ("Century Gothic", 15, 'bold')).grid(row = 2, column = 0, padx = (175,0), pady = 10)     # font: Τύπος & Μέγεθος Γραμματοσειράς , grid: Θέση Κειμένου
            
        

        # Θέση Combo Box
        self.signalController = tk.StringVar()
        self.txtchoosen = ttk.Combobox(self, width = 15, values = comboboxvals, textvariable = self.signalController)
        self.txtchoosen.grid(row = 150, column = 1)



        # Θέση Κειμένου που περιγράφει τη λειτουργία του Combo Box
        ttk.Label (self, text = "Επιλέξτε το Αρχείο που θέλετε να ανοίξετε:",
                font = ("Century Gothic", 10)).grid(column = 0,
                row = 10, padx = 10, pady = 25)



        # Κείμενο Υποσημείωσης που επεξηγεί τι πρέπει να κάνει ο χρήστης με το Παράθυρο, καθώς και τι θα του εμφανιστεί 
        ttk.Label (self, text = "                          Υποσημείωση:",  font = ("Century Gothic", 9)).grid(column = 0, row = 70, padx = 10, pady = 15)
        ttk.Label (self, text = "         Ο χρήστης επιλέγει ποιο άρχείο επιθυμεί να τρέξει,",  font = ("Century Gothic", 9)).grid(column = 0, row = 71, padx = 10, pady = 2)
        ttk.Label (self, text = "     και κατόπιν εμφανίζεται το αντίστοιχο γράφημα.",  font = ("Century Gothic", 9)).grid(column = 0, row = 72, padx = 10, pady = 2)

        self.txtchoosen.grid(column = 1, row = 10)
        self.txtchoosen.current()



        # Προσθήκη Κουμπιών Graph & Exit αντίστοιχα, στο Παράθυρο                                                                           # command: Καλεί το όρισμα από την αντίστοιχη κλάση
        btnCalc = tk.Button (self , text = "Graph" , font = "Arial 10" , command = self.btnCalcHandler).place(x = 150 , y = 300)            # place: Θέση κουμπιών στους άξονες x και y
        buttonExit = tk.Button (self , text = "Exit" , font = "Arial 10" , command = self.Exit_App).place(x = 310 , y = 300)                # place: Θέση κουμπιών στους άξονες x και y
    


    # Παράθυρο επιβεβαίωσης πριν από την έξοδο
    def Exit_App(self):  
        response = messagebox.askyesno('Έξοδος από την Εφαρμογή','Επιθυμείτε σίγουρα την έξοδό σας από την εφαρμογή;' )     # Μήνυμα επιβεβαίωσης εξόδου
        if response:
            self.destroy()
    


    # Άντληση Δεδομένων από το παρακάτω link
    def btnCalcHandler(self):
        x = self.signalController.get()
        dataset = f"https://raw.githubusercontent.com/ppatsea/Algorithms/main/ta{x.strip()}.dat"
        
        try:                                                                # Εάν η αίτηση αποκριθεί επιτυχώς,
            response = requests.get(dataset)                                # Τα Δεδομένα Αποθηκεύονται στη μεταβλητή "response"
            n_jobs , n_machines , p = pfsp.read_pfsp_request(response)      # Ανάγνωση Δεδομένων που λήφθηκαν κατόπιν αιτήσεως HTTP
            job_sequence = pfsp.naive_solution(n_jobs , seed = 42)          # Προκαθορισμένος αλγόριθμος χρησιμοποιώντας τη συνάρτηση seed=42 για προκαθορισμένο seed, ώστε να αρχικοποιηθούν τυχαίοι αριθμοί


            C = pfsp.schedule(n_jobs, n_machines , p , job_sequence)  # Εφαρμογή χρόνου εκτέλεσης (scheduling) στα δεδομένα που λήφθηκαν
            pfsp.display_schedule(C , job_sequence , p)                 # Εμφάνιση χρόνου εκτέλεσης, των ακολουθιών εργασιών και των παραμέτρων του προβλήματος



        # Εάν συμβεί κάποιο σφάλμα τύπου HTTPError κατά τη διάρκεια αυτών των ενεργειών, η except κλάση πιάνει το σφάλμα και το εκτυπώνει
        except HTTPError as err:
            raise err



# Δημιουργείται μια έκδοση της κλάσης WindowApp και εκτελείται το κυρίως παράθυρο
if __name__ == '__main__':
    app = WindowApp()
    app.mainloop()