### Item 52 use `subprocess` to manage child process

The best choice to manage child processes is the `subprocess` module

```
import subprocess

result = subprocess.run(
    ['echo', 'Hello from the child!'],
    capture_output=True,
    encoding='utf-8'
)

result.check_returncode()  # No args on this means no errors
print(result.stdout)

>>> Hello from the child!
```

I can use `Popen` to periodically poll child processes's status while Python does some other thing

``` 
proc = subprocess.Popen(['sleep', '1'])
while proc.poll() is None:
    print("Working...")

# Some other time-consuming stuff going on here
print('Exit status', proc.poll())

>>> Working ...
Working ...
Exit status 0
```

I can decouple Child Process from Parent

```
import time
start = time.time()
sleep_procs = []
for _ in range(10):
    proc = subprocess.Popen(['sleep', '1'])
    sleep_procs.append(proc)

for proc in sleep_procs:
    proc.communicate()

end = time.time()
delta = end - start
print(f"Finished in {delta:.3} seconds")

>>> Finished in 1.02 seconds
```

If these processes would have run in sequence if would have taken ~10 secs (1 sec per sleep proc) whereas with decoupling it took ~1 sec 

I can terminate a process that somehow was blocked or is causing a block by passing the `timeout` parameter

```
proc = subprocess.Popen(['sleep', '10'])
try:
    proc.communicate(timeout=0.1)
except subprocess.TimeoutExpired:
    proc.terminate()
    proc.wait()

print("Exit status", proc.poll())

>>> Exit status -15
```

### Things to Remember

- Use `subprocess` module to run child processes and manage their I/O Streams
- Child processes run in parallel with the Python interpreter
- Use `run` for simple usage, use `Popen` for advanced usage
- Use `timeout` parameter to avoid deadlocks.


### Item 53 Use Threads for Blocking I/O, Avoid for Parallelism
