import time, sys, getopt

CPU_STATS = [
                'yld_cnt', 'legacy', 'sched_cnt', 'sched_goidle',
                'ttwu_cnt', 'ttwu_local', 'sched_run', 'sched_delay',
                'sched_slice'
            ]

CSV_HEADER = "timestamp,vmname,id,delta_ms," + ",".join(CPU_STATS) + "\n"

def static_delta_to_csv(timestamp_ms : int, host_name : str, cpuid : str, delta_ms : int, delta_as_dict : dict):
    if delta_ms is None:
        delta_ms = ''
    csv_line = str(round(timestamp_ms/1000)) +  "," + host_name + "," + cpuid + "," + str(delta_ms)
    for value in delta_as_dict.values():
        csv_line+= "," + str(value)
    return csv_line + "\n"

class SchedCPU:

    def __init__(self, cpuid):
        self.cpuid = cpuid

        self.old_raw_values = dict()
        self.delta_stats = dict()
        self.delta_ms = 0

        self.timestamp_ms = 0
        self.init = True

    def parse_values(self, raw_values : dict, timestamp_ms : int):
        if (not self.init):
            self.delta_ms = timestamp_ms - self.timestamp_ms
            self.delta_stats = dict() # clear old data
            for item, value in raw_values.items():
                self.delta_stats[item] = int(raw_values[item]) - int(self.old_raw_values[item])
        # Update for next call
        self.timestamp_ms = timestamp_ms
        self.old_raw_values = raw_values

    def delta_to_csv(self, host_name : str):
        if(self.init):
            return ""
        return static_delta_to_csv(timestamp_ms=self.timestamp_ms,
            host_name=host_name,
            cpuid=self.cpuid, 
            delta_ms=self.delta_ms, 
            delta_as_dict=self.delta_stats)

    def delta_to_dict(self, sum_dict : dict):
        if(self.init):
            self.init = False
            return sum_dict
        for item, value in self.delta_stats.items():
            if item not in sum_dict:
                sum_dict[item] = 0
            sum_dict[item]+= value
        return self.delta_ms

def parse(cpu_dict : dict, timestamp_ms : int):

    for line in open("/proc/schedstat"):
        tokens = line.split()

        if tokens[0].startswith('cpu'):
            if tokens[0] in cpu_dict:
                currentCPU = cpu_dict[tokens[0]]
            else:
                currentCPU = cpu_dict[tokens[0]] = SchedCPU(tokens[0])

            values = tokens[1:]
            assert len(CPU_STATS) == len(values)
            currentCPU.parse_values(dict(zip(CPU_STATS, values)), timestamp_ms)

if __name__ == '__main__':
    
    short_options = "n:d:o:h"
    long_options = ["name=","delay=","output","help"]

    host_name = None
    delay = 60000 # 60s
    output = "schedstat"

    cpu_dict = dict()

    try:
        arguments, values = getopt.getopt(sys.argv[1:], short_options, long_options)
    except getopt.error as err:
        print (str(err)) # Output error, and return with an error code
        sys.exit(2)
    for current_argument, current_value in arguments:
        if current_argument in ("-h", "--help"):
            print(long_options)
            sys.exit(0)
        if current_argument in ("-n", "--name"):
            host_name = current_value
        if current_argument in ("-d", "--delay"):
            delay = int(current_value)
        if current_argument in ("-o", "--output"):
            output = current_value
    
    if host_name is None:
        print("VM name must be set")
        sys.exit(-1)
        
    output+= "-" + str(delay) + "ms.csv"
    
    # Init output folder
    with open(output, "w") as output_file: # open in append mode
        output_file.write(CSV_HEADER)

    # Main loop
    while True:
        ms_begin = time.time_ns() // 1_000_000
        ## Treatement
        parse(cpu_dict, ms_begin)
        ## Append iteration
        with open(output, "a") as output_file: # open in append mode
            sum_dict = dict()
            for cpu in cpu_dict.values():
                output_file.write(cpu.delta_to_csv(host_name)) 
                delta_ms = cpu.delta_to_dict(sum_dict) # delta is identical through cpu
            if sum_dict:
                output_file.write(static_delta_to_csv(timestamp_ms=ms_begin, 
                    host_name=host_name, 
                    cpuid='overall', 
                    delta_ms=delta_ms, 
                    delta_as_dict=sum_dict))
        ## Iteration management
        ms_end = time.time_ns() // 1_000_000
        sleep_duration_ms = delay - (ms_end - ms_begin)
        if sleep_duration_ms>0:
            time.sleep(sleep_duration_ms/1000)