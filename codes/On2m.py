import time                         # Για τη μέτρηση του χρόνου εκτέλεσης κομματιών του κώδικα
import os
import matplotlib.pyplot as plot
import matplotlib.colors as mcolors  # Βιβλιοθήκη για την προσθήκη χρωμάτων στα γραφήματα
import timeit
import requests
from io import StringIO

start_time_all = time.time()  # ο αρχικός χρόνος εκτέλεσης όλου του προγράμματος



# Υπολογίζει το makespan για μια συγκεκριμένη διάταξη εργασιών με δεδομένους τους χρόνους επεξεργασίας
def improved_makespan(permutation, processing_times):

    # Υπολογίζει το makespan για μια δεδομένη διάταξη (permutation) των εργασιών
    # Ορισμός των n και m, αντίστοιχα
    job = len(permutation)
    machine = len(processing_times[0])


    # Δημιουργία πίνακα completion_times διαστάσεων n x m
    completion_times = [[0] * machine for _ in range(job)]


    # Υπολογισμός των χρόνων ολοκλήρωσης (completion times) για κάθε εργασία σε κάθε μηχάνημα
    for i in range(job):
        for j in range(machine):
            if i == 0:      # Αναφέρεται στην πρώτη εργασία
                # Ο χρόνος ολοκλήρωσης για το 1ο μηχάνημα είναι ο χρόνος επεξεργασίας της πρώτης εργασίας σε αυτό το μηχάνημα
                completion_times[i][j] = processing_times[permutation[i]][j]

            elif j == 0:    # Αναφέρεται στο πρώτο μηχάνημα για κάθε εργασία που δεν είναι η πρώτη
                # Ο χρόνος ολοκλήρωσης για το πρώτο μηχάνημα είναι ο χρόνος ολοκλήρωσης της
                # προηγούμενης εργασίας στο ίδιο μηχάνημα συν το χρόνο επεξεργασίας της τρέχουσας εργασίας
                completion_times[i][j] = completion_times[i-1][j] + processing_times[permutation[i]][j]

            else:
                # Ο χρόνος ολοκλήρωσης για το τρέχον μηχάνημα και την τρέχουσα εργασία υπολογίζεται ως μέγιστος
                # από τον χρόνο ολοκλήρωσης της προηγούμενης εργασίας στο ίδιο μηχάνημα και τον χρόνο ολοκλήρωσης 
                # της τρέχουσας εργασίας στο προηγούμενο μηχάνημα
                completion_times[i][j] = max(completion_times[i][j-1] , completion_times[i-1][j]) + processing_times[permutation[i]][j]


    # Ενημερώνει τον πίνακα completion_times με τους χρόνους ολοκλήρωσης κάθε εργασίας σε κάθε μηχάνημα
    return completion_times[-1][-1]




# Υλοποίηση του βελτιωμένου αλγορίθμου NEH για το πρόβλημα σειριακής διάταξης εργασιών (PFSP)
def improved_neh(processing_times, job_sequence=None):

    # Ορισμός των n και m, αντίστοιχα
    job = len(processing_times)
    machine = len(processing_times[0])


    # Δημιουργία αρχικής διάταξης των εργασιών, ταξινομημένη βάσει του makespan που υπολογίζεται για κάθε εργασία χωριστά
    initial_permutation = list(range(job))                   # Δημιουργία λίστας που περιέχει ακέραιους από το 0 έως το n-1
    initial_permutation.sort(key=lambda x: improved_makespan([x] , processing_times))                 # Ταξινόμηση Λίστας



    best_permutation = initial_permutation      # Δημιουργία μιας νέας λίστας "best_permutation" και αντιγράφει  
                                                # τα περιεχόμενά της από την "initial_permutation" 

    best_makespan = improved_makespan(best_permutation , processing_times)  # Υπολογίζει το makespan για την αρχική διάταξη 
                                                                            # "best_permutation" χρησιμοποιώντας τη συνάρτηση "improved_makespan"


    if job_sequence:
        processing_times = [processing_times[i] for i in job_sequence]


    for i in range(1, job):       # Εξετάζει κάθε εργασία > της πρώτης
        current_job = initial_permutation[i]    # Επιλέγει την τρέχουσα εργασία που εξετάζεται στον βρόχο

        # Δημιουργεί μια υποψήφια διάταξη εργασιών
        # Αυτή η διάταξη αποτελείται από τις εργασίες που έχουν ήδη τοποθετηθεί στη
        # βέλτιστη διάταξη (best_permutation) και την τρέχουσα εργασία που εξετάζεται
        candidate_permutation = best_permutation[:i] + [current_job] + best_permutation[i:]


        # Υπολογίζει το makespan για την υποψήφια διάταξη, χρησιμοποιώντας τη συνάρτηση "improved_makespan"
        candidate_makespan = improved_makespan(candidate_permutation , processing_times)


        # Αν το makespan της υποψήφιας διάταξης (candidate_makespan)
        # είναι μικρότερο από το τρέχον καλύτερο makespan (best_makespan)
        if candidate_makespan < best_makespan:
            best_makespan = candidate_makespan          # Ο καλύτερος makespan ενημερώνεται με το makespan της υποψήφιας διάταξης
            best_permutation = candidate_permutation    # Η καλύτερη διάταξη ενημερώνεται με την υποψήφια διάταξη

    return best_permutation , best_makespan             # Επιστρέφει την καλύτερη διάταξη και τον αντίστοιχο καλύτερο χρόνο ολοκλήρωσης




# Δημιουργία πίνακα χρόνων τερματισμού εκτέλεσης κάθε εργασίας σε κάθε μηχάνημα
def completion_times(permutation):
    job = len(permutation)
    machine = len(permutation)

    processing_time = 1
    C_T = [[0] * machine for _ in range(job)]

    # Υπολογισμός του completion times για την πρώτη μηχανή
    C_T[0][0] = processing_time * permutation[0]
    for j in range(1, job):
        C_T[j][0] = C_T[j-1][0] + processing_time

    # Υπολογισμός του completion times για τις μηχανές που απομένουν
    for i in range(1, machine):
        C_T[0][i] = C_T[0][i-1] + processing_time

    for j in range(1, job):
        for i in range(1, machine):
            C_T[j][i] = max(C_T[j-1][i], C_T[j][i-1]) + processing_time

    return C_T

# Ο κώδικας των γραμμών 124-129, σε μερικούς χρόνους στην έξοδο έβγαζε 0.0. Γι αυτό αντικαταστάθηκε με τις γραμμές 132-134, ώστε να προσφέρει μεγαλύτερη ακρίβεια στο χρόνο
# def measure_execution_time(algorithm, *args):
#     start_time = time.time()                # Χρόνος Έναρξης
#     result = algorithm(*args)               # * : επιτρέπει τη μετατροπή μιας λίστας, σε ξεχωριστά ορίσματα
#     end_time = time.time()                  # Χρόνος λήξης
#     execution_time = end_time - start_time  # Ο χρόνος εκτέλεσης υπολογίζεται ως η διαφορά μεταξύ του end_time και του start_time
#     return execution_time                   # Επιστρέφει το χρόνο εκτέλεσης του αλγορίθμου

# Μετρά τον χρόνο εκτέλεσης ενός αλγορίθμου με δεδομένες παραμέτρους
def measure_execution_time(algorithm, *args):
    execution_time = timeit.timeit(lambda: algorithm(*args), number=1)
    return execution_time


# Εύρεση αρχείων στο GitHub και έλεγχος ύπαρξης
def read_data_from_github(file_url):
    try:
        response = requests.get(file_url)
        response.raise_for_status()  # Έλεγχος εάν το request έγινε επιτυχώς
        content = response.text
        return content
    
    # Διαφορετικά εμφάνιση error μηνύματος
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Request Error: {err}")
    return None




# Διάβασμα αρχείων από το GitHub
def read_data_from_file(file_path):
    # Έλεγχος εάν το μονοπάτι αντιστοιχεί σε URL του GitHub
    if file_path.startswith("https://github.com/ppatsea/Algorithms/"):
        return read_data_from_github(file_path)
    

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None


    with open(file_path, 'r') as file:
        lines = file.readlines()  # Διάβασμα όλων των γραμμών των αρχείων
        
        # Εξαγωγή των χρόνων επεξεργασίας των εργασιών από κάθε γραμμή, παραλείποντας την πρώτη γραμμή με τον αριθμό των εργασιών
        permutation = map(int, lines[0].split())
        
        
        processing_times = [list(map(int, line.strip().split()[1::2])) for line in lines[1::2]]

    # Επιστρέφει μια λίστα με τα δεδομένα (processing times)
    return processing_times


# Μορφοποίηση αριθμού αρχείου που ξεκινάει με μηδενικά
def format_file_number(file_number):
    return f"{file_number:03d}"




"""
####################################################
######  ΕΜΦΑΝΙΣΗ  ΑΠΟΤΕΛΕΣΜΑΤΩΝ  ΣΤΗΝ  ΟΘΟΝΗ  ######
#################################################### 
"""

# # Εκτέλεση του αλγορίθμου O(n^2 * m), για όλα τα αρχεία
# def execution_improved_neh(file_path):

#     # Διβάζει όλους τους χρόνους επεξεργασίας, για κάθε αρχείο
#     processing_times_from_file = read_data_from_file(file_path)

#     # Εκτέλεση του βελτιωμένου αλγορίθμου NEH, στις εργασίες
#     best_permutation, best_makespan = improved_neh(processing_times_from_file)


#     processing_times = read_data_from_file(file_path)
#     execution_time = measure_execution_time(improved_neh, processing_times_from_file)

#     C_T = completion_times(best_permutation)
    
#     file_name = os.path.basename(file_path)


#     # Εκτύπωση των αποτελεσμάτων
#     print(f"File: {file_path}")
#     print("\nΒέλτιστη Διάταξη Εργασιών O(n^2 * m):", best_permutation)         # Η βέλτιστη διάταξη εργασιών,
#     print("\nΧρόνος Εκτέλεσης O(n^2 * m):", best_makespan)                     # Ο χρόνος εκτέλεσης O(n2m), 
#     print(f"\nΣυνολικός Χρόνος Εκτέλεσης Αρχείου: {execution_time} seconds")   # Ο χρόνος εκτέλεσης του αντίστοιχου αρχείου
#     print("\n\n\n")




# # Μορφοποίηση αριθμού αρχείου που ξεκινάει με μηδενικά
# def format_file_number(file_number):
#     return f"{file_number:03d}"

# # Δημιουργία λίστας με file paths που διαβάζει και τα 120 αρχεία txt
# file_paths = [f'./Taillard-PFSP/ta{format_file_number(i)}.txt' for i in range(1, 21)]


# # Εκτέλεση αλγορίθμου O(n2m) για τα 120 txt αρχεία 
# for file_path in file_paths:
#     execution_improved_neh(file_path)




"""
####################################################
######  ΕΜΦΑΝΙΣΗ  ΑΠΟΤΕΛΕΣΜΑΤΩΝ  ΣΤΗΝ  ΟΘΟΝΗ  ######
######  ΚΑΙ  ΕΓΓΡΑΦΗ  ΑΥΤΩΝ  ΣΕ  ΑΡΧΕΙΟ  ΤΧΤ  ######
####################################################             
"""

# Εκτέλεση του αλγορίθμου O(n2m), για όλα τα αρχεία
def execution_improved_neh(file_path, output_file):

    # Διβάζει όλους τους χρόνους επεξεργασίας, για κάθε αρχείο
    processing_times_from_file = read_data_from_file(file_path)

    # Εκτέλεση του αλγορίθμου O(n2m), στις εργασίες
    improved_neh_permutation, improved_neh_makespan = improved_neh(processing_times_from_file)
    best_permutation, best_makespan = improved_neh(processing_times_from_file)

    processing_times = read_data_from_file(file_path)
    execution_time = measure_execution_time(improved_neh, processing_times_from_file)

    C_T = completion_times(best_permutation)

    elapsed_time = measure_execution_time(improved_neh, processing_times_from_file)
    file_name = os.path.basename(file_path)

    # Δημιουργία αρχείου txt για εγγραφή των αποτελεσμάτων
    with open(output_file, 'a', encoding='utf-8') as f:
            f.write(f"\nFile: {file_path}\n")
            f.write("\nΒέλτιστη Διάταξη Εργασιών O(n^2 * m): {}".format(best_permutation))
            f.write("\nΧρόνος Εκτέλεσης O(n^2 * m): {}".format(best_makespan))
            f.write(f"\nΣυνολικός Χρόνος Εκτέλεσης Αρχείου: {execution_time} seconds")
            f.write("\n\n\n")


    # Εκτύπωση των αποτελεσμάτων στην οθόνη
    print(f"File: {file_path}")
    print("\nΒέλτιστη Διάταξη Εργασιών O(n^2 * m):", best_permutation)         # Η βέλτιστη διάταξη εργασιών,
    print("\nΧρόνος Εκτέλεσης O(n^2 * m):", best_makespan)                     # Ο χρόνος εκτέλεσης O(n2m), 
    print(f"\nΣυνολικός Χρόνος Εκτέλεσης Αρχείου: {execution_time} seconds")   # Ο χρόνος εκτέλεσης του αντίστοιχου αρχείου
    print("\n\n\n")




# Μορφοποίηση αριθμού αρχείου που ξεκινάει με μηδενικά
def format_file_number(file_number):
    return f"{file_number:03d}"

file_paths = [f'./Taillard-PFSP/ta{format_file_number(i)}.txt' for i in range(1, 121)]

output_file = 'results_On2m.txt'


for file_path in file_paths:
    execution_improved_neh(file_path, output_file)




# Γράφημα Gannt
def gantt_chart(processing_times, best_permutation, C_T, makespan):
    job, machine = len(processing_times), len(processing_times[0])
    C_T = completion_times(best_permutation)
    
    colors = list(mcolors.TABLEAU_COLORS.values())

    plot.figure(figsize=(10, machine * 3))

    for i in range(machine):
        machine_start_time = 0

        for j in range(len(best_permutation)):
            # machine_start_time = C_T[j][i] - processing_times[j][i]
            machine_start_time = max(C_T[j][i], machine_start_time)
            plot.barh(i, width = processing_times[j][i], left = machine_start_time, height=0.8, color = colors[j % len(colors)], label = f"Εργασία {j}" if i == 0 else "")
    
    handles, labels = plot.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))

    plot.yticks(range(len(processing_times[0])), [f"Μηχανή {i}" for i in range(1, len(processing_times[0]) + 1)])
    plot.xlabel("Χρόνος")
    
    # Προσθήκη του ονόματος του αρχείου στον τίτλο του γραφήματος
    plot.title(f"Διάγραμμα Gantt → Makespan: {makespan}")
    plot.legend(by_label.values(), by_label.keys(), loc="upper right")
    plot.show()


# Εκτύπωση του Διαγράμματος Gantt
processing_times_from_file = read_data_from_file(file_path)
best_permutation, best_makespan = improved_neh(processing_times_from_file)

C_T = completion_times(best_permutation)

gantt_chart(processing_times_from_file, best_permutation, C_T, best_makespan)



# Συνολικός Χρόνος Εκτέλεσης Προγράμματος 
end_time_all = time.time()
final_time = end_time_all - start_time_all

print(f"\nΣυνολικός Χρόνος Εκτέλεσης Προγράμματος: {final_time} seconds")
print("\n")




""""
Αν ο χρήστης θέλει τα αποτελέσματα να εκτυπώνονται στην οθόνη, βάζει σε σχόλια τις γραμμές: 247-294,
και στη γραμμή 288 επιλέγει το εύρος των αρχείων που επθυμεί να εκτελέσει.

Αντιθέτως, αν επιθυμεί τα αποτελέσματα να εγγράφονται στο αρχείο με όνομα "results_On2m.txt", τοποθετεί σε σχόλια τις γραμμές 197-235,
και στη γραμμή 230 επιλέγει το εύρος των αρχείων που θέλει να εκτελέσει.
"""