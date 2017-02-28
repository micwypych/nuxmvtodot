import sys
import re
import copy as cp

def parse(strings):
   lines = strings.readlines()
   
   states = []
   simulation = 0
   step = 0
   for next_line in lines: 
     next_line = next_line.strip()
     state_header = re.compile(r'-> State: (\d{1,10})\.(\d{1,10}) <-')
     matcher = state_header.match(next_line)
     if matcher:
       simulation = int(matcher.group(1))
       step = int(matcher.group(2))
       states.append((simulation,step,{}))
       continue
     state_change = re.compile(r'(\w+) = (.+)')
     new_matcher = state_change.match(next_line)
     if new_matcher:
       var = new_matcher.group(1)
       value = new_matcher.group(2)
       states[-1][2].update({var: value})
       continue
   return states
   
def accumulate_states(states):
   processed_states = [states[0]]
   for i in range(len(states)-1):
     tmp = cp.deepcopy(processed_states[i])
     tmp[2].update(states[i+1][2])
     processed_states.append(tmp)
   return processed_states
   
def state_str(state):      
   return str(sorted(state[2].items()))
   
def link_str(state1,state2):
   return '"'+state_str(state1)+'"'+' -> '+'"'+state_str(state2)+'"'
   
def to_dia(states):
   print('digraph structs {')
   for i in range(len(states)-1):
      s = link_str(states[i],states[i+1])
      print(s+';')
   print('}')

def process_file(file_name):
   states = parse(open(file_name))
   processed_states = accumulate_states(states)
   to_dia(processed_states)

def main(argv):
    for arg in argv:
        process_file(arg)
        
    
        
if __name__ == "__main__":
    main(sys.argv[1:])
