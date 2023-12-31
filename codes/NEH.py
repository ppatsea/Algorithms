import time                          
import os
import matplotlib.pyplot as plot
import matplotlib.colors as mcolors  

import requests
from io import StringIO

start_all = time.time()  # ο αρχικός χρόνος εκτέλεσης όλου του προγράμματος




# Υπολογίζει το makespan για μια συγκεκριμένη διάταξη εργασιών με δεδομένους τους χρόνους επεξεργασίας
def makespan(permutation, processing_times):

    # Υπολογίζει το makespan για μια δεδομένη διάταξη (permutation) των εργασιών
    # Ορισμός των n και m, αντίστοιχα
    job = len(permutation)
    machine = len(permutation[0])


    # Δημιουργία πίνακα completion_times διαστάσεων n x m
    completion_times = [[0] * machine for _ in range(job)]

    completion_times[0][0] = processing_times[0][0]

    # Υπολογισμός των χρόνων ολοκλήρωσης (completion times) για κάθε εργασία σε κάθε μηχάνημα
    for j in range(1, job):
        completion_times[j][0] = completion_times[j-1][0] + processing_times[j][0]

    for i in range(1, machine):
        completion_times[0][i] = completion_times[0][i-1] + processing_times[0][i]


    for j in range(1, job):
        for i in range(1, machine):
            completion_times[j][i] = max(completion_times[j-1][i], completion_times[j][i-1]) + processing_times[j][i]

    makespan = completion_times[job-1][machine-1]

    return makespan




# Υλοποήση του αλγορίθμου NEH για το πρόβλημα PFSP
def neh(processing_times, job_sequence=None):

    # Οι εργασίες ταξινομούνται βάσει των αθροισμάτων τους
    processing_times.sort(key=lambda x: sum(x), reverse=True)
    
    # Αρχικοποίηση του προγράμματος
    permutation = [processing_times[0], processing_times[1]]

    # Εάν παρέχεται η σειρά job_sequence, χρησιμοποιείται ως αρχική σειρά
    if job_sequence:
        processing_times = [processing_times[i] for i in job_sequence]

    # Εξερεύνηση όλων των πιθανών περιπτώσεων για την εύρεση της βέλτιστης λύσης
    for i in range(2, len(processing_times)):
        best_permutation = None
        best_makespan = float('inf')

        # Εισάγει την τρέχουσα εργασία I σε διαφορετικές θέσεις στο χρονοδιάγραμμα (permutation)
        for j in range(len(permutation) + 1):
            current_permutation = permutation[:j] + [processing_times[i]] + permutation[j:]
            current_makespan = makespan(current_permutation, processing_times)   # Υπολογισμός του makespan για το προτεινόμενο πρόγραμμα

            # Αν η νέα διάταξη είναι καλύτερη, ενημέρωσε τον καλύτερο
            if current_makespan < best_makespan:        # Έλεγχος αν ο current_makespan είναι μικρότερος από τον best_makespan
                best_makespan = current_makespan        # Αν είναι, ενημερώνεται ο best_makespan και 
                best_permutation = current_permutation  # ο best_permutation, με τις αντίστοιχες τιμές

        permutation = best_permutation                  # Ενημέρωση του προγράμματος με το καλύτερο permutation για την εργασία i
    
    # Επιστρέφεται η βέλτιστη διάταξη (best_permutation) και ο αντίστοιχος χρόνος ολοκλήρωσης (best_makespan)
    return permutation, best_makespan




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
    

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None


    with open(file_path, 'r') as file:
        lines = file.readlines()  # Διάβασμα όλων των γραμμών των αρχείων
        permutation = map(int, lines[0].split())

        processing_times = [list(map(int, line.strip().split())) for line in lines[1:]]

        # Εξαγωγή των χρόνων επεξεργασίας των εργασιών από κάθε γραμμή, παραλείποντας την πρώτη γραμμή με τον αριθμό των εργασιών
        # job = [list(map(int, line.strip().split()[1:])) for line in lines[1:]]

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

# Εκτέλεση του αλγορίθμου NEH, για όλα τα αρχεία
def execution_neh(file_path):

    # Διβάζει όλους τους χρόνους επεξεργασίας, για κάθε αρχείο
    processing_times_from_file = read_data_from_file(file_path)

    # Εκτέλεση του αλγορίθμου NEH, στις εργασίες
    best_permutation, best_makespan = neh(processing_times_from_file)


    # processing_times = read_data_from_file(file_path)
    execution_time = measure_execution_time(neh, processing_times_from_file)


    # Εκτέλεση του αλγορίθμου NEH με τη σειρά job_sequence για τη λήψη της σωστής σειράς των εργασιών
    optimal_order, _ = neh(processing_times_from_file, job_sequence=range(len(processing_times_from_file)))
    
    optimal_order_indices = [processing_times_from_file.index(processing_times) for processing_times in optimal_order]
    
    

    # Εκτύπωση των αποτελεσμάτων
    print(f"File: {file_path}")
    print("\nΒέλτιστη Διάταξη Εργασιών NEH:", best_permutation)                # Η βέλτιστη σειρά διατάξεων,
    print("\nΒέλτιστη Σειρά Εργασιών NEH:", optimal_order_indices)             # Η βέλτιστη διάταξη εργασιών,
    print("\nΧρόνος Εκτέλεσης NEH:", best_makespan)                            # Ο χρόνος εκτέλεσης NEH, 
    print(f"\nΣυνολικός Χρόνος Εκτέλεσης Αρχείου: {execution_time} seconds")   # Ο χρόνος εκτέλεσης του αντίστοιχου αρχείου
    print("\n\n\n")




# Μορφοποίηση αριθμού αρχείου που ξεκινάει με μηδενικά
def format_file_number(file_number):
    return f"{file_number:03d}"

# Δημιουργία λίστας με file paths που διαβάζει και τα 120 αρχεία txt
file_paths = [f'./Taillard-PFSP/ta{format_file_number(i)}.txt' for i in range(1, 21)]


# Εκτέλεση αλγορίθμου NEH για τα 120 txt αρχεία 
for file_path in file_paths:
    execution_neh(file_path)




"""
####################################################
######  ΕΜΦΑΝΙΣΗ  ΑΠΟΤΕΛΕΣΜΑΤΩΝ  ΣΤΗΝ  ΟΘΟΝΗ  ######
######  ΚΑΙ  ΕΓΓΡΑΦΗ  ΑΥΤΩΝ  ΣΕ  ΑΡΧΕΙΟ  ΤΧΤ  ######
####################################################             
"""

# Εκτέλεση του αλγορίθμου NEH, για όλα τα αρχεία
# def execution_neh(file_path, output_file):

#     # for file_number, file_path in enumerate(file_paths, start=1):
#         processing_times_from_file = read_data_from_file(file_path)

#         best_permutation, best_makespan = neh(processing_times_from_file)
#         execution_time = measure_execution_time(neh, processing_times_from_file)

#         optimal_order, _ = neh(processing_times_from_file, job_sequence=range(len(processing_times_from_file)))
#         optimal_order_indices = [processing_times_from_file.index(processing_times) for processing_times in optimal_order]

#         elapsed_time = measure_execution_time(neh, processing_times_from_file)
#         file_name = os.path.basename(file_path)

#         # Corrected output file path
#         with open(output_file, 'a', encoding='utf-8') as f:
#             f.write(f"\nFile: {file_path}\n")
#             f.write("\nΒέλτιστη Διάταξη Εργασιών NEH:".format(best_permutation))
#             f.write("\nΒέλτιστη Σειρά Εργασιών NEH:".format(optimal_order_indices))
#             f.write("\nΧρόνος Εκτέλεσης NEH:".format(best_makespan))
#             f.write(f"\nΣυνολικός Χρόνος Εκτέλεσης Αρχείου: {execution_time} seconds")
#             f.write("\n\n\n")
    

#         # Print results to the console
#         print(f"File: {file_path}")
#         print("\nΒέλτιστη Διάταξη Εργασιών NEH:", best_permutation)                # Η βέλτιστη σειρά διατάξεων,
#         print("\nΒέλτιστη Σειρά Εργασιών NEH:", optimal_order_indices)             # Η βέλτιστη διάταξη εργασιών,
#         print("\nΧρόνος Eκέλεσης NEH:", best_makespan)                             # Ο χρόνος εκτέλεσης NEH, 
#         print(f"\nΣυνολικός Χρόνος Εκτέλεσης Αρχείου: {execution_time} seconds")   # Ο χρόνος εκτέλεσης του αντίστοιχου αρχείου
#         print("\n\n\n")




# # Μορφοποίηση αριθμού αρχείου που ξεκινάει με μηδενικά
# def format_file_number(file_number):
#     return f"{file_number:03d}"

# file_paths = [f'./Taillard-PFSP/ta{format_file_number(i)}.txt' for i in range(1, 121)]

# output_file = 'results_On2m.txt'


# for file_path in file_paths:
#     execution_neh(file_path, output_file)
    



# Γράφημα Gannt
def gantt_chart(permutation, makespan):
    machines = list(zip(*permutation))
    colors = list(mcolors.TABLEAU_COLORS.values())

    plot.figure(figsize=(10, 5))
    
    for i, machine in enumerate(machines):
        machine_start_time = 0
        for j, end_time in enumerate(machine):
            plot.barh(i, end_time - machine_start_time, left=machine_start_time, color=f"C{j}", alpha=0.7)
            machine_start_time = end_time

    plot.yticks(range(len(permutation[0])), [f"Εργασία {i}" for i in range(1, len(permutation[0]) + 1)])
    plot.xlabel("Χρόνος")
    plot.title(f"Διάγραμμα Gantt → Makespan: {makespan}")
    plot.grid(axis = "x")
    plot.show()


# Εκτύπωση του Διαγράμματος Gantt
processing_times_from_file = read_data_from_file(file_path)
best_permutation, best_makespan = neh(processing_times_from_file)

gantt_chart(best_permutation, best_makespan)



# Συνολικός Χρόνος Εκτέλεσης Προγράμματος 
end_all = time.time()
total_time = end_all - start_all

print(f"\nΣυνολικός Χρόνος Εκτέλεσης Προγράμματος: {total_time} seconds")




""""
Αν ο χρήστης θέλει τα αποτελέσματα να εκτυπώνονται στην οθόνη, βάζει σε σχόλια τις γραμμές: 208-254,
και στη γραμμή 191 επιλέγει το εύρος των αρχείων που επθυμεί να εκτελέσει.

Αντιθέτως, αν επιθυμεί τα αποτελέσματα να εγγράφονται στο αρχείο με όνομα "results_NEH.txt", τοποθετεί σε σχόλια τις γραμμές 155-196,
και στη γραμμή 248 επιλέγει το εύρος των αρχείων που θέλει να εκτελέσει.
"""