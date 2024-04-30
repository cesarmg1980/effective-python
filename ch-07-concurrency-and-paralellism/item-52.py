import subprocess

print("### `subprocess` example ###")
result = subprocess.run(
    ['echo', 'Hello from the child!'],
    capture_output=True,
    encoding='utf-8'
)

result.check_returncode()  # No args on this means no errors
print(result.stdout)

print()
print("### `Popen` example ###")
proc = subprocess.Popen(['sleep', '1'])
while proc.poll() is None:
    print("Working...")

# Some other time-consuming stuff going on here
print('Exit status', proc.poll())

print()
print("### Decoupling Child Process from Parent")
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

print()
print("### Example of `timeout` parameter")
proc = subprocess.Popen(['sleep', '10'])
try:
    proc.communicate(timeout=0.1)
except subprocess.TimeoutExpired:
    proc.terminate()
    proc.wait()

print("Exit status", proc.poll())
