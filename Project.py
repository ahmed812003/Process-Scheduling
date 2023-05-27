import tkinter as tk
from tkinter import messagebox

class Process:
    def __init__(self, process_id, burst_time, arrival_time):
        self.process_id = process_id
        self.burst_time = burst_time
        self.arrival_time = arrival_time
        self.waiting_time = 0
        self.turnaround_time = 0
    ##############################################################################################
class SchedulingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Process Scheduling")
        
        self.processes = []
        self.quantum = 0
        # Center the input grid
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Labels
        tk.Label(root, text="Number of Processes").grid(row=0, column=0)
        
        # Entries
        self.num_processes_entry = tk.Entry(root)
        self.num_processes_entry.grid(row=0, column=1)
        
        # Button
        tk.Button(root, text="Enter", command=self.get_num_processes).grid(row=0, column=2)
    ##############################################################################################    
    def get_num_processes(self):
        num_processes = int(self.num_processes_entry.get())
        self.num_processes_entry.config(state="disabled")
        self.create_process_entries(num_processes)
    ##############################################################################################   
    def create_process_entries(self, num_processes):
        # Destroy previous widgets
        for widget in self.root.grid_slaves():
            widget.grid_forget()
        
        # Labels
        tk.Label(self.root, text="Process ID").grid(row=0, column=0)
        tk.Label(self.root, text="Burst Time").grid(row=0, column=1)
        tk.Label(self.root, text="Arrival Time").grid(row=0, column=2)
        
        # Entries
        self.process_entries = []
        for i in range(num_processes):
            process_id_entry = tk.Entry(self.root)
            process_id_entry.grid(row=i+1, column=0)
            burst_time_entry = tk.Entry(self.root)
            burst_time_entry.grid(row=i+1, column=1)
            arrival_time_entry = tk.Entry(self.root)
            arrival_time_entry.grid(row=i+1, column=2)
            self.process_entries.append((process_id_entry, burst_time_entry, arrival_time_entry))
        
        tk.Label(self.root, text="quantum").grid(row=0, column=3)
        quantum_entry = tk.Entry(self.root)
        quantum_entry.grid(row=1 , column=3)
        
        self.quantumValue = quantum_entry
        
        # Button
        button1 = tk.Button(self.root, text="First Come First Served", command=self.apply_fcfs).grid(row=num_processes+3, column=0)
        button2 = tk.Button(self.root, text="Shortest Job First (Primitive)", command=self.apply_sjf_primitive).grid(row=num_processes+3, column=1)
        button3 = tk.Button(self.root, text="Shortest Job First (Non-Primitive)", command=self.apply_sjf_non_primitive).grid(row=num_processes+3, column=2)
        button4 = tk.Button(self.root, text="Round Robin RR scheduling", command=self.apply_round_robin).grid(row=num_processes+3, column=3)
        # Grid
        self.result_box = tk.Text(self.root, height=10, width=50)
        self.result_box.grid(row=num_processes+4, column=0, columnspan=4)
    ##############################################################################################   
    def get_process_details(self):
        self.processes = []
        for process_entry in self.process_entries:
            process_id = int(process_entry[0].get())
            burst_time = int(process_entry[1].get())
            arrival_time = int(process_entry[2].get())
            process = Process(process_id, burst_time, arrival_time)
            self.processes.append(process)
    ##############################################################################################
    def apply_fcfs(self):
        self.get_process_details()
        self.processes.sort(key=lambda x: x.arrival_time)
        waiting_time, turnaround_time = self.fcfs(self.processes) 
        for i in range(len(self.processes)):
            self.processes[i].waiting_time = waiting_time[i]
            self.processes[i].turnaround_time = turnaround_time[i]
        self.display_results()
        
    def fcfs(self, processes):
        ct = []
        burst_time = [process.burst_time for process in processes]
        arrival_time = [process.arrival_time for process in processes]
        waiting_time =[]
        turnaround_time = []
        top = 0
        for i in range(len(processes)):
            if i == 0 : 
                top = top + burst_time[i]
                ct.append(top)
            elif i > 0 :
                if top < arrival_time[i]:
                    top = arrival_time[i] + burst_time[i]
                    ct.append(top)
                else:
                    top = top + burst_time[i]
                    ct.append(top)
        for i in range(len(processes)):
            var = ct[i] - arrival_time[i]
            turnaround_time.append(var)
            var = turnaround_time[i] - burst_time[i]
            waiting_time.append(var)
        return waiting_time , turnaround_time
    ##############################################################################################
    def apply_sjf_non_primitive(self):
        self.get_process_details()
        self.processes.sort(key=lambda x: x.arrival_time)
        waiting_time, turnaround_time = self.sjf_non_preemptive(self.processes) 
        for i in range(len(self.processes)):
            self.processes[i].waiting_time = waiting_time[i]
            self.processes[i].turnaround_time = turnaround_time[i]
        self.display_results()
    
    def sjf_non_preemptive(self , processes):
        n = len(processes)  
        burst_time = [process.burst_time for process in processes] 
        waiting_time = [0] * n 
        turnaround_time = [0] * n  
        complete = 0 
        time = 0 
        while complete < n :
            short = -1 
            mn = 10000000000
            for i in range(n):
                if(processes[i].arrival_time <= time and burst_time[i] < mn and burst_time[i] > -1):
                    mn = burst_time[i] 
                    short = i
            time += burst_time[short]
            burst_time[short] = -1
            waiting_time[short] = time - processes[short].burst_time - processes[short].arrival_time
            turnaround_time[short] = time - processes[short].arrival_time
            complete = complete + 1
        return waiting_time, turnaround_time
    ##############################################################################################
    def apply_sjf_primitive(self):
        self.get_process_details()
        self.processes.sort(key=lambda x: x.arrival_time)
        waiting_time, turnaround_time = self.sjf_primitive(self.processes) 
        for i in range(len(self.processes)):
            self.processes[i].waiting_time = waiting_time[i]
            self.processes[i].turnaround_time = turnaround_time[i]
        self.display_results()

    def sjf_primitive(self , processes):
        n = len(processes)  
        burst_remaining = [process.burst_time for process in processes]  
        waiting_time = [0] * n  
        turnaround_time = [0] * n  
        complete = 0  
        time = 0   
        while complete != n:
            shortest = -1 
            mn = 10000000000
            for i in range(n):
                if(processes[i].arrival_time <= time and burst_remaining[i] < mn and burst_remaining[i] > -1):
                    mn = burst_remaining[i] 
                    shortest = i
            if shortest == -1 : 
                time = time + 1
                continue 
            burst_remaining[shortest] -= 1 
            time += 1
            if burst_remaining[shortest] == 0:
                complete += 1
                finish_time = time
                burst_remaining[shortest] = -1
                waiting_time[shortest] = finish_time - processes[shortest].burst_time - processes[shortest].arrival_time
                turnaround_time[shortest] = finish_time - processes[shortest].arrival_time
        return waiting_time, turnaround_time
    ##############################################################################################
    def apply_round_robin(self):
        self.get_process_details()
        self.quantum = int(self.quantumValue.get())
        self.processes.sort(key=lambda x: x.arrival_time)
        waiting_time, turnaround_time = self.round_robin(self.processes) 
        for i in range(len(self.processes)):
            self.processes[i].waiting_time = waiting_time[i]
            self.processes[i].turnaround_time = turnaround_time[i]
        self.display_results()
    
    def round_robin(self , processes):
        n = len(processes)  
        burst_time = [process.burst_time for process in processes]  
        waiting_time = [0] * n  
        turnaround_time = [0] * n  
        complete = 0  
        time = 0
        while True:
            all_done = True
            for i in range(n):
                if burst_time[i] > 0:
                    all_done = False
                    if burst_time[i] > self.quantum:
                        time += self.quantum
                        burst_time[i] -= self.quantum
                    else:
                        time += burst_time[i]
                        waiting_time[i] = time - processes[i].burst_time - processes[i].arrival_time
                        burst_time[i] = 0
                        turnaround_time[i] = waiting_time[i] + processes[i].burst_time
            if all_done:
                break
        return waiting_time, turnaround_time
    ##############################################################################################
    def display_results(self):
        self.result_box.delete(1.0, tk.END)
        # Display results in the grid box
        self.result_box.insert(tk.END, "{:<10} {:<10} {:<10} {:<10}\n".format(
            "Process ID", "Burst Time", "Waiting Time", "Turnaround Time"))
        for process in self.processes:
            self.result_box.insert(tk.END, "{:<10} {:<10} {:<10} {:<10}\n".format(
                f"P{process.process_id}", process.burst_time, process.waiting_time, process.turnaround_time))
        # Calculate average waiting time and average turnaround time
        avg_waiting_time = sum(process.waiting_time for process in self.processes) / len(self.processes)
        avg_turnaround_time = sum(process.turnaround_time for process in self.processes) / len(self.processes)
        self.result_box.insert(tk.END, "\nAverage Waiting Time: {:.2f}\n".format(avg_waiting_time))
        self.result_box.insert(tk.END, "Average Turnaround Time: {:.2f}".format(avg_turnaround_time))
    ##############################################################################################    
if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulingGUI(root)
    root.mainloop()