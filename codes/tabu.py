import time   
import matplotlib.pyplot as plot 
import matplotlib.colors as mcolors  
import requests                         # βιβλιοθήκη για να παίρνει τα αρχεία απο το github
from io import StringIO
import os                               # βιβλιοθήκη που παίρνει μόνο το όνομα του αρχείου από το file_path
import random
import numpy as np

start_time_all = time.time()  # ο αρχικός χρόνος εκτέλεσης όλου του προγράμματος



# Υπολογίζει το makespan για μια συγκεκριμένη διάταξη εργασιών με δεδομένους τους χρόνους επεξεργασίας
def makespan(permutation, processing_times):

    # Υπολογισμός των job και machine
    job = len(permutation)
    machine = len(processing_times[0])

    # Δημιουργεί μια λίστα με μηδενικά που αντιπροσωπεύει τον χρόνο ολοκλήρωσης για κάθε μηχάνημα
    makespan = [0] * machine

    for j in permutation:
        for i in range(machine):

            # Αυξάνει τον χρόνο ολοκλήρωσης για το συγκεκριμένο μηχάνημα  
            # κατά τον χρόνο επεξεργασίας της εργασίας j στο μηχάνημα i
            makespan[i] = sum([makespan[i], processing_times[j][i]])

    # Επιστρέφει το μέγιστο συνολικό χρόνο ολοκλήρωσης
    return max(makespan)




# Υλοποίηση συνάρτησης που δημιουργεί μια αρχική διάταξη (permutation) των εργασιών
# Η διάταξη αυτή δημιουργείται τυχαία, για να εξασφαλίσει ότι κάθε εργασία εμφανίζεται ακριβώς μία φορά
def initial_permutation(job):

    # Δημιουργεί μια λίστα που περιέχει τα πρώτα job και στη συνέχεια επιλέγει τυχαία job στοιχεία από αυτήν τη λίστα 
    # Το αποτέλεσμα είναι μια τυχαία διάταξη των ακεραίων από 0 έως job-1.
    return random.sample(range(job), job)




# Υλοποίηση συνάρτησης που εκτελεί μια διαταραχή (perturbation) στην τρέχουσα διάταξη των εργασιών
# Η διαταραχή γίνεται με το να ανταλλάσσονται δύο τυχαία στοιχεία της διάταξης
def perturb_permutation(permutation):

    # Δημιουργεί μια λίστα που περιέχει τα πρώτα δύο ακέραια νούμερα από 0 έως το μήκος της διάταξης
    idx1, idx2 = random.sample(range(len(permutation)), 2)

    # Ανταλλάσσει τις τιμές στις θέσεις idx1 και idx2 της διάταξης permutation
    # Αυτό αντιστοιχεί στο να ανταλλάσσονται δύο τυχαίες εργασίες στη διάταξη
    permutation[idx1], permutation[idx2] = permutation[idx2], permutation[idx1]

    # Επιστροφή διάταξης μετά τη διαταραχή
    return permutation




# Υλοποίηση του Αλγορίθμου Tabu Search
def tabu_search(processing_times, tabu_size, num_iterations):
    job = len(processing_times)
    
    current_permutation = initial_permutation(job)
    current_makespan = makespan(current_permutation, processing_times)

    best_permutation = list(current_permutation)  
    best_makespan = current_makespan

    tabu_list = []              # Αρχικοποίηση λίστας Tabu


    for iteration in range(num_iterations):
        new_permutation = perturb_permutation(current_permutation)
        new_makespan = makespan(new_permutation, processing_times)

        # Αν η νέα διάταξη δεν είναι στη λίστα Tabu 
        if new_permutation not in tabu_list and new_makespan < current_makespan:
            current_permutation = list(new_permutation)  
            current_makespan = new_makespan

            # Αν το νέο makespan είναι μικρότερο από το τρέχον makespan
            if new_makespan < best_makespan:
                best_permutation = list(new_permutation) 
                best_makespan = new_makespan

        tabu_list.append(list(new_permutation))

        # Αν η λίστα Tabu έχει υπερβεί το μέγεθος tabu_size, αφαίρεση του πρώτου στοιχείου
        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)

    return best_permutation




# Δημιουργία πίνακα χρόνων τερματισμού εκτέλεσης κάθε εργασίας σε κάθε μηχάνημα
def completion_times(permutation):
    job = len(permutation)
    machine = len(permutation)

    processing_time = 1
    C_T = np.zeros((job, machine))

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




# Μετρά τον χρόνο εκτέλεσης ενός αλγορίθμου με δεδομένες παραμέτρους
def measure_execution_time(algorithm, *args):
    start_time = time.time()                # Χρόνος Έναρξης
    result = algorithm(*args)               # * : επιτρέπει τη μετατροπή μιας λίστας, σε ξεχωριστά ορίσματα
    end_time = time.time()                  # Χρόνος λήξης
    execution_time = end_time - start_time  # Ο χρόνος εκτέλεσης υπολογίζεται ως η διαφορά μεταξύ του end_time και του start_time
    return execution_time                   # Επιστρέφει το χρόνο εκτέλεσης του αλγορίθμου




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
    # Έλεγχος εάν το μονοπάτι αντιστοιχεί σε URL του GitHub   --- public or private  ---
    if file_path.startswith("https://github.com/ppatsea/Algorithms/"):
        return read_data_from_github(file_path)
    
    with open(file_path, 'r') as file:
        lines = file.readlines()  # Διάβασμα όλων των γραμμών των αρχείων

        permutation = map(int, lines[0].split())  # Κάνει split τις διαστάσεις του προβλήματος στο permutation

        # Εξαγωγή των χρόνων επεξεργασίας των εργασιών από κάθε γραμμή, παραλείποντας την πρώτη γραμμή με τον αριθμό των εργασιών
        
        processing_times = [list(map(int, line.strip().split()[1::2])) for line in lines[1::2]]
    # Επιστρέφει μια λίστα με τα δεδομένα (processing times)
    return processing_times




"""
####################################################
######  ΕΜΦΑΝΙΣΗ  ΑΠΟΤΕΛΕΣΜΑΤΩΝ  ΣΤΗΝ  ΟΘΟΝΗ  ######
####################################################
"""

# Εκτέλεση του αλγορίθμου Tabu Search, για όλα τα αρχεία
def execution_tabu_search(file_path, tabu_size, num_iterations):
    
    # Διαβάζει όλους τους χρόνους επεξεργασίας, για κάθε αρχείο
    processing_times = read_data_from_file(file_path)
    
    processing_times_from_file = read_data_from_file(file_path)
    execution_time = measure_execution_time(tabu_search, processing_times_from_file, tabu_size_tabu_search, num_iterations_tabu_search)
    final_permutation = tabu_search(processing_times, tabu_size, num_iterations)

    final_makespan = makespan(final_permutation, processing_times)

    C_T = completion_times(final_permutation)

    # Εκτύπωση των αποτελεσμάτων
    print(f"File: {file_path}")                                                 # Το αντίστοιχο εκτελώμενο αρχείο
    print("\nΒέλτιστη Διάταξη Εργασιών Tabu Search:", final_permutation)        # Η βέλτιστη διάταξη εργασιών,
    print("\nΧρόνος Εκτέλεσης Tabu Search:", final_makespan)                    # Ο χρόνος εκτέλεσης Tabu Search, και
    print(f"\nΣυνολικός Χρόνος Εκτέλεσης Αρχείου: {execution_time} seconds")    # Ο αντίστοιχος χρόνος εκτέλεσης
    print("\n\n\n")




# Μορφοποίηση αριθμού αρχείου που ξεκινάει με μηδενικά
def format_file_number(file_number):
    return f"{file_number:03d}"

# Δημιουργία λίστας με file paths που διαβάζει και τα 120 αρχεία txt
file_paths = [f'./Taillard-PFSP/ta{format_file_number(i)}.txt' for i in range(1, 21)]

# Παράμετροι για τον Tabu Search
tabu_size_tabu_search = 10
num_iterations_tabu_search = 1000


# Εκτέλεση αλγορίθμου Tabu Search για τα 120 txt αρχεία 
for file_path in file_paths:
    execution_tabu_search(file_path, tabu_size_tabu_search, num_iterations_tabu_search)




"""
####################################################
######  ΕΜΦΑΝΙΣΗ  ΑΠΟΤΕΛΕΣΜΑΤΩΝ  ΣΤΗΝ  ΟΘΟΝΗ  ######
######  ΚΑΙ  ΕΓΓΡΑΦΗ  ΑΥΤΩΝ  ΣΕ  ΑΡΧΕΙΟ  ΤΧΤ  ######
####################################################
"""

# # Εκτέλεση του αλγορίθμου Tabu Search, για όλα τα αρχεία
# def execution_tabu_search(file_path, tabu_size, num_iterations, output_file):
    
#     # Διβάζει όλους τους χρόνους επεξεργασίας, για κάθε αρχείο
#     processing_times = read_data_from_file(file_path)
    
#     processing_times_from_file = read_data_from_file(file_path)
#     execution_time = measure_execution_time(tabu_search, processing_times_from_file, tabu_size_tabu_search, num_iterations_tabu_search)
#     final_permutation = tabu_search(processing_times, tabu_size, num_iterations)
    
#     final_makespan = makespan(final_permutation, processing_times)

#     C_T = completion_times(final_permutation)

#     # Δημιουργία αρχείου txt για εγγραφή των αποτελεσμάτων
#     with open(output_file, 'a', encoding='utf-8') as f:
#         f.write(f"File: {file_path}")
#         f.write("\nΒέλτιστη Διάταξη Εργασιών Tabu Search: {}".format(final_permutation))   # Η βέλτιστη διάταξη εργασιών,
#         f.write("\nΧρόνος Eκτέλεσης Tabu Search: {}".format(final_makespan))               # Ο χρόνος εκτέλεσης Tabu Search, και
#         f.write(f"\nΣυνολικός Χρόνος Εκτέλεσης Αρχείου: {execution_time} seconds")      # Ο αντίστοιχος χρόνος εκτέλεσης
#         f.write("\n\n\n")


#     # Εκτύπωση των αποτελεσμάτων
#     print(f"File: {file_path}")                                                        # Το αντίστοιχο εκτελώμενο αρχείο
#     print("\nΒέλτιστη Διάταξη Εργασιών Tabu Search:", final_permutation)               # Η βέλτιστη διάταξη εργασιών,
#     print("\nΧρόνος Eκτέλεσης Tabu Search:", final_makespan)                           # Ο χρόνος εκτέλεσης Tabu Search, και
#     print(f"\nΣυνολικός Χρόνος Εκτέλεσης Αρχείου: {execution_time} seconds")           # Ο αντίστοιχος χρόνος εκτέλεσης
#     print("\n\n\n")




# # Μορφοποίηση αριθμού αρχείου που ξεκινάει με μηδενικά
# def format_file_number(file_number):
#     return f"{file_number:03d}"

# # Δημιουργία λίστας με file paths που διαβάζει και τα 120 αρχεία txt
# file_paths = [f'./Taillard-PFSP/ta{format_file_number(i)}.txt' for i in range(1, 12)]

# # Παράμετροι για τον Tabu Search
# tabu_size_tabu_search = 10
# num_iterations_tabu_search = 1000


# # Αποθήκευση των αποτελεσμάτων σε συγκεκριμένο Αρχείο
# output_file = 'C:/Users/user/Desktop/Algorithms'
# output_file = 'results_tabu_search.txt'

# # Εκτέλεση αλγορίθμου Tabu Search για τα 120 txt αρχεία 
# for file_path in file_paths:
#     execution_tabu_search(file_path, tabu_size_tabu_search, num_iterations_tabu_search, output_file)




# Γράφημα Gannt
def gantt_chart(processing_times, makespan, C_T):
    jobs, machines = len(processing_times), len(processing_times[0])
    colors = list(mcolors.TABLEAU_COLORS.values())

    plot.figure(figsize=(10, machines * 3))

    for i in range(machines):
        machine_start_time = 0

        for j in range(jobs):
            machine_start_time = max(C_T[j][i], machine_start_time)
            plot.barh(i, width=processing_times[j][i], left=machine_start_time, height=0.8,
                      color=colors[j % len(colors)], label=f"Εργασία {j}" if i == 0 else "")

    handles, labels = plot.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))

    plot.yticks(range(machines), [f"Μηχανή {i}" for i in range(1, machines + 1)])
    plot.xlabel("Χρόνος")
    plot.title(f"Διάγραμμα Gantt → Makespan: {makespan}")
    plot.legend(by_label.values(), by_label.keys(), loc="upper right")
    plot.show()


# Εκτύπωση του Διαγράμματος Gantt
processing_times_from_file = read_data_from_file(file_path)
best_permutation = tabu_search(processing_times_from_file, tabu_size_tabu_search, num_iterations_tabu_search)
best_makespan = makespan(best_permutation, processing_times_from_file)

C_T = completion_times(best_permutation)

gantt_chart(processing_times_from_file, best_makespan, C_T)




# Ο χρόνος εκτέλεσης όλου του προγράμματος 
end_time_all = time.time()
final_time = end_time_all - start_time_all

print(f"\nΣυνολικός Χρόνος Εκτέλεσης Προγράμματος: {final_time} seconds")
print("\n")




""""
Αν ο χρήστης θέλει τα αποτελέσματα να εκτυπώνονται στην οθόνη, βάζει σε σχόλια τις γραμμές: 238-289,
και στη γραμμή 276 επιλέγει το εύρος των αρχείων που επθυμεί να εκτελέσει.

Αντιθέτως, αν επιθυμεί τα αποτελέσματα να εγγράφονται στο αρχείο με όνομα "results_tabu_search.txt", τοποθετεί σε σχόλια τις γραμμές 188-226,
και στη γραμμή 217 επιλέγει το εύρος των αρχείων που θέλει να εκτελέσει.
"""