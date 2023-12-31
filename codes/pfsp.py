# Εισαγωγή απαραίτητων βιβλιοθηκών
# import cv2                              # cv2 : Φόρτωση του OpenCV, μιας βιβλιοθήκης προγραμματισμού ανοικτού κώδικα που παρέχει εργαλεία για την επεξεργασία εικόνων και βίντεο

import matplotlib.pyplot as plot        # matplotlib.pyplot : Χρησιμοποιείται για τη Δημιουργία Διαγραμμάτων

import matplotlib.colors as mcolors     # matplotlib.colors : Χρησιμοποιείται για τη φόρτωση του mcolors από τη βιβλιοθήκη matplotlib

import glob                             # glob : Παρέχει Συναρτήσεις για την αναζήτηση αρχείων που ταιριάζουν με ένα πρότυπο στο σύστημα αρχείων

import numpy as np                      # numpy : Παρέχει Υψηλής Απόδοσης πρωτογενείς πίνακες και λειτουργίες πινάκων

import seaborn as sns                   # seaborn : Χρησιμοποιείται συνδυαστικά με τη matplotlib για την επικοινωνία με γραφικές παραστάσεις

import pandas as pd                     # pandas : Επεξεργασία Δεδομένων


# Εμφάνιση των αρχείων του φακέλου Taillard-PFSP
glob.glob('./Taillard-PFSP/ta*')                    # Εντοπίζει όλα τα αρχεία που αρχίζουν με "ta" στον φάκελο ./Taillard-PFSP/



# Εκτύπωση της πρώτης γραμμής κάθε αρχείου προβλήματος
for fn in sorted(glob.glob('./Taillard-PFSP/ta*')):         
    print(fn)
    with open(fn , 'r') as f:                               # Διαβάζει την πρώτη γραμμή από κάθε αρχείο στον φάκελο ./Taillard-PFSP/
        print(f.readline())                                 # Εκτυπώνει την πρώτη γραμμή από κάθε αρχείο



# Ανάγνωση περιεχομένων αρχείου προβλήματος, τοποθέτηση σε μια δομή (αριθμός εργασιών, αριθμός μηχανών, λεξικό με χρόνους επεξεργασίας)
def read_pfsp_instance(fn):
    with open(fn , 'r') as f:                                   # Διαβάζει ένα αρχείο προβλήματος PFSP
        # Διαβάζει την πρώτη γραμμή από ένα αρχείο κειμένου και διαχωρίζει τους αριθμούς που περιέχει, χρησιμοποιώντας το κενό ως χαρακτηριστικό διαχωρισμού
        n_jobs , n_machines = map(int , f.readline().split())   
        p = {}                                                  # Δημιουργία κενού Λεξικού, το οποίο στη συνέχεια θα αποθηκεύει τους χρόνους επεξεργασίας για κάθε εργασία σε κάθε μηχάνημα

        # Ανάγνωση Χρόνων Επεξεργασίας από το αρχείο, για κάθε εργασία και κάθε μηχάνημα
        for j in range(n_jobs):
            for i , t in enumerate(f.readline().split()[1::2]):  # enumerate : Παίρνει τη θέση i και την τιμή t από κάθε γραμμή και τα αποθηκεύει,
                p[j,i] = int(t)                                  # στο λεξικό p χρησιμοποιώντας τους δείκτες j και i
        return n_jobs , n_machines , p                           # Επιστρέφει τα στοιχεία που διαβάστηκαν, δηλαδή τον αριθμό των εργασιών (n_jobs), τον αριθμό των μηχανών (n_machines), και το λεξικό (p) που περιέχει τους χρόνους επεξεργασίας




# Διαβάζει τα δεδομένα από μια αίτηση HTTP και εξάγει την απαραίτητη πληροφορία
def read_pfsp_request(response):
    data = response.text.split('\n')
    n_jobs , n_machines = [int(x) for x in data[0].strip().split()]   # Ανάγνωση του αριθμού των εργασιών (n_jobs) και των μηχανών (n_machines)
    p = {}

    # Για κάθε γραμμή που περιέχει τους χρόνους επεξεργασίας για κάθε εργασία και μηχάνημα,
    for j in range(n_jobs):
        for i , t in enumerate(data[j+1].strip().split()[1::2]):
            p[j,i] = int(t)                                          # Οι χρόνοι επεξεργασίας αποθηκεύονται σε ένα λεξικό p χρησιμοποιώντας τους δείκτες j και i
    return n_jobs , n_machines , p                                   # Επιστρέφει τον αριθμό των εργασιών (n_jobs), τον αριθμό των μηχανών (n_machines) και το λεξικό (p) που περιέχει τους χρόνους επεξεργασίας


# n_jobs, n_machines, p = read_pfsp_instance('./Taillard-PFSP/ta001')
# n_jobs, n_machines, p




# Ένας Απλοϊκός Επιλυτής
# Υλοποιεί έναν απλό αλγόριθμο εύρεσης λύσης, που δημιουργεί μια τυχαία διάταξη εργασιών
def naive_solution(n_jobs , seed=None):     # Παίρνει δύο παραμέτρους: τον αριθμό των εργασιών (n_jobs) και έναν προαιρετικό (seed) για την αρχικοποίηση με τυχαίους αριθμούς
    if seed is not None:
        np.random.seed(seed)                # Η συνάρτηση την επιστρέφει ως πίνακα NumPy
    return np.random.permutation(n_jobs)    # Δημιουργεί μια τυχαία σειρά αριθμών από το 0 έως το (n_jobs - 1). Αυτή η σειρά αριθμών αντιστοιχεί σε μια πιθανή λύση για το πρόβλημα



# Δημιουργία πίνακα χρόνων τερματισμού εκτέλεσης κάθε εργασίας σε κάθε μηχάνημα
# Υλοποιεί το πρόγραμμα προγραμματισμού χρόνου εκτέλεσης (scheduling) βάσει της δεδομένης λύσης
# Χρησιμοποιείται για τον υπολογισμό του χρόνου ολοκλήρωσης (makespan).
def schedule(n_jobs , n_machines , p , solution):           # solution : Μια λύση για το πρόβλημα, που αντιστοιχεί στη σειρά εκτέλεσης των εργασιών
    C = np.zeros((n_jobs , n_machines))                     # Δημιουργία πίνακα C με διαστάσεις (n_jobs, n_machines) για την αποθήκευση των χρόνων τερματισμού

    for idx , j in enumerate(solution):                     # Για κάθε εργασία και κάθε μηχάνημα, υπολογίζει τον χρόνο τερματισμού 
        for i in range(n_machines):                         # βάσει της προηγούμενης εργασίας και του χρόνου επεξεργασίας σε αυτό το μηχάνημα
           
            if idx == 0:                                    # Αν η εργασία είναι η πρώτη στον χρόνο εκτέλεσης,
                if i == 0:                                  # τότε ο χρόνος τερματισμού είναι:
                    C[j,i] = p[j,i]                         # είτε ο χρόνος επεξεργασίας της εργασίας σε αυτό το μηχάνημα, εάν είναι το πρώτο μηχάνημα

                else:
                    C[j,i] = C[j,i-1] + p[j,i]              # είτε ο χρόνος τερματισμού της προηγούμενης εργασίας στο ίδιο μηχάνημα, εάν δεν είναι το πρώτο μηχάνημα


            else:                                           # Αν όμως η εργασία δεν είναι η πρώτη, 
                if i == 0:                                  # τότε ο χρόνος τερματισμού είναι:
                    C[j,i] = C[solution[idx-1],i] + p[j,i]  # είτε ο χρόνος τερματισμού της προηγούμενης εργασίας στο ίδιο μηχάνημα, εάν δεν είναι το πρώτο μηχάνημα

                else:
                    # είτε ο μέγιστος χρόνος τερματισμού ανάμεσα στον χρόνο τερματισμού της προηγούμενης εργασίας στο ίδιο μηχάνημα και τον χρόνο τερματισμού της προηγούμενης εργασίας στο προηγούμενο μηχάνημα
                    C[j,i] = max(C[j,i-1] , C[solution[idx-1],i]) + p[j,i]   


    return C                                                # Η συνάρτηση επιστρέφει τον πίνακα χρόνων τερματισμού



# Συνολικός Χρόνος Ολοκλήρωσης Προγράμματος
# Υπολογίζει τον χρόνο ολοκλήρωσης για μια δεδομένη ακολουθία εργασιών και ένα πρόγραμμα προγραμματισμού χρόνου εκτέλεσης
def makespan(job_sequence , C):                             # Παίρνει δύο παραμέτρους: τη σειρά εκτέλεσης των εργασιών, και τον πίνακα χρόνων τερματισμού
    return C[job_sequence[-1] , -1]                         # Επιστρέφει το χρόνο τερματισμού της τελευταίας εργασίας στο τελευταίο μηχάνημα, ο οποίος αποτελεί το συνολικό κόστος εκτέλεσης της σειράς εργασιών



# Εμφανίζει το γράφημα προγράμματος προγραμματισμού χρόνου εκτέλεσης χρησιμοποιώντας το matplotlib
def display_schedule(C , job_sequence , p):                 # Δημιουργία Γραφήματος για τον χρονοπρογραμματισμό των εργασιών στο PFSP πρόβλημα
    n_jobs , n_machines = C.shape


    # Βιβλιοθήκη Matplotlib
    colors = list(mcolors.TABLEAU_COLORS.values()) 

    plot.figure(figsize=(10 , n_machines * 3))

    for i in range(n_machines):
         for j in job_sequence:
            # Η γραφική παράσταση χρησιμοποιεί μπάρες (barh) για να απεικονίσει τον χρόνο εκτέλεσης κάθε εργασίας σε κάθε μηχάνημα
             plot.barh(i , width=p[j, i] , left=C[j,i] - p[j, i] , height=0.8 , color=colors[j % len(colors)] , label=f"Job {j}" if i==0 else "")



    handles , labels = plot.gca().get_legend_handles_labels()                        # Κάθε μπάρα αντιστοιχεί σε μια εργασία και εμφανίζεται σε κάθε μηχάνημα που προχωράει
    by_label = dict(zip(labels , handles))                                           # Δημιουργία Λεξικού με:
                                                                                     # labels : Είναι η λίστα που περιέχει τις ετικέτες των αντικειμένων, και
                                                                                     # handles : Είναι η λίστα που περιέχει τα αντικείμενα που θέλουμε να αντιστοιχίσουμε στις ετικέτες

    plot.yticks(range(n_machines) , [f"Machine {i}" for i in range(n_machines)])     # Άξονας y : Αντιπροσωπεύει τα Μηχανήματα "Μachines"
    plot.xlabel('Time')                                                              # Άξονας x : Αντιπροσωπεύει τον χρόνο "Τime"
    plot.title('Permutation Flowshop Schedule')                                      # Τίτλος Γραφήματος : "Permutation Flowshop Schedule"
    plot.legend(by_label.values() , by_label.keys(), loc="upper right")              # Προσθέτει έναν κατάλογο στο γράφημα που δείχνει τα χρώματα που αντιστοιχούν σε κάθε εργασία και τις αντίστοιχες ετικέτες
    plot.gca().invert_yaxis()                                                        # Αντιστρέφει τον άξονα y του γραφήματος. Τα μηχανήματα θα εμφανίζονται στο γράφημα από πάνω προς τα κάτω, με το πρώτο μηχάνημα στην κορυφή.
    plot.show()







    # # Βιβλιοθήκη Seaborn
    # colors = sns.color_palette("husl" , n_colors=n_jobs)

    # df = pd.DataFrame()

    
    # for i in range(n_machines):

    #     for j in job_sequence:
    #         df = pd.concat([df, pd.DataFrame({'Job': [f"Job {j}"] * 2, 'Machine': [f"Machine {i}"] * 2, 'Time': [C[j, i] - p[j, i], C[j, i]]})])


    #         plot.figure(figsize=(10, n_machines * 3))
    #         sns.barplot(data=df, x='Time', y='Machine', hue='Job', palette=colors)
    #         plot.yticks(range(n_machines), [f"Machine {i}" for i in range(n_machines)])
    #         plot.xlabel('Time')
    #         plot.title('Permutation Flowshop Schedule')
    #         plot.legend(loc="upper right")
    #         plot.gca().invert_yaxis()
    #         plot.show()

            
            
    

# n_jobs, n_machines, p = read_pfsp_instance('./Taillard-PFSP/ta001')
# job_sequence = naive_solution(n_jobs)
# C = schedule(n_jobs, n_machines, p, job_sequence)
# print(makespan(job_sequence, C))
# display_schedule(C)


# Όλα τα plot στον κώδικα pfsp.py έχουν μπει σε σχόλια, ούτως ώστε όταν τρέχει ο κώδικας selector.py, να μην αναπαρίστανται δύο φορές τα ζητούμενα διαγράμματα.
# Ο χρήστης, για την οπτικοποίηση των γραφημάτων δεν τρέχει τον κώδικα pfsp.py, αλλά τον selector.py, μιας και ο ένας κώδικας καλείται μέσα στον άλλον.