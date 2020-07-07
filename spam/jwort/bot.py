#im literally gonna copy and paste this into every python project i do
def save_import(module, **kwargs):

    attribute = kwargs.get("attribute", None)
    name = kwargs.get("name", None)


    if not attribute:
        print("[*] Loading " + module + " library",end="")
    else:
        print("[*] Loading " + attribute + " from " + module + " library",end="")
    
    if name:
        print(" as " + name, end="")
    print("... ", end="")

    try:
        
        if not attribute:
            import_string = "import " + module
        else:
            import_string = "from " + module + " import " + attribute
        if name:
            import_string += " as " + name
        
        exec(import_string, globals())
        print("Done")
    except ModuleNotFoundError:
        print("Failed")
        print("[!] " + module + " library not found.")
        print("[*] Installing " + module + " library...\n")
        version = sys_version[:sys_version.find(".", sys_version.find(".") + 1)]
        system("py -" + version + " -m pip install " + module)
        print("")
        try:
            exec(import_string, globals())
        except ModuleNotFoundError:
            print("[!] Could not load " + module + " library. Try to install it manually.")
            exit()





import string

from sys import version as sys_version
from os import system
from time import sleep
from random import randint
from _thread import start_new_thread

###replace these with save_imports (might add more in the future). These are here so vs code works.

#import requests
#import keyboard

save_import("requests")
save_import("keyboard")

DEFAULT_WORD = "Schabernack"
DEFAULT_THREADS = 5
DEFAULT_WAIT = True

#Capping this out here, im not sure what would happen if you change it.
MAX_THREADS = 100

NO_INTERNET_TIMEOUT = 30 #seconds

print("")

word = ""
threads = 0
count = 0
focused_thread = 0



wait = True


#stolen from the interwebZ
def flush_input():
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        import sys, termios
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)

def string_is_ascii_or_letter_only(istring):
    for c in istring:
        if c not in string.ascii_letters and c not in string.digits:
            return False
    return True

#recursion go
def get_word():
    print("[*] Enter word to submit (or press enter to use \"" + DEFAULT_WORD + "\"):")
    while True:
        word = input("[*] word >> ")
        if word == "":
            return DEFAULT_WORD

        if not string_is_ascii_or_letter_only(word):
            print("[!] The word you entered contains characters that aren't letters or numbers.")
            print("[!] Do you want to change it (y/n)?")
            retry = False
            while True:
                response = input("[!] (y/n) >> ")

                if response.lower() == "y":
                    retry = True
                    break
                elif response.lower() == "n":
                    break
                else:
                    print("[!] Not a valid answer.")
            if retry:
                retry = False
                continue
        return word

def get_threads():
    print("[*] How many threads (simultaneous processes) do you want to run?")
    print("[*] Press enter to use the default of " + str(DEFAULT_THREADS) + ".")
    while True:
        threads = input("[*] threads >> ")
        if threads == "":
            return DEFAULT_THREADS
        try:
            threads = int(threads)
            if threads < 1 or threads > MAX_THREADS:
                print("[!] Thread count not in the allowed range of 1-" + str(MAX_THREADS) + ".")
                continue
            return threads
        except:
            print("[!] Invalid input. Did you enter a number?")
            continue

def get_wait():
    print("[*] Should the script wait a little between each request (enter = yes)?")
    while True:
        answ = input("[*] (y/n) >> ")
        if answ == "":
            return DEFAULT_WAIT
        if answ.lower() == "y":
            return True
        elif answ.lower() == "n":
            return False
        else:
            print("[!] Not a valid answer.")


#print thread id plus text if thread id is focused. If no text, print empty line. Then print menu instructions.
def running_print(thread_id, text, **kwargs):
    if not thread_id == focused_thread:
        return
    if text == "":
            print("")
    else:

        text = str(thread_id + 1) + "|: " + text
        if kwargs.get("end", None):
            print(text,end=kwargs.get("end", None))
        else:
            print(text)

def spam(thread_id):
    global count

    # wait for all threads to launch (aesthetic purposes)
    sleep(1)
    while True:
        #create session
        session = requests.Session()
        
        running_print(thread_id, "[*] Faking survey visit...")

        #extract survey_data
        try:
            page = session.get("https://www.surveymonkey.com/r/7JZRVLJ?embedded=1")
        except requests.RequestException:
            running_print(thread_id, "[!] Can't connect to host. Do you have an existing internet connection?")
            sleep(NO_INTERNET_TIMEOUT)
            continue

        running_print(thread_id, "[*] Extracting \"survey_data\" parameter...")
        survey_data_offset = page.text.find("survey_data\" value=\"") + 20

        if survey_data_offset == 19:
            running_print(thread_id, "[!] Failed to extract survey data. Please report this bug.")
            running_print(thread_id, "[!] Writing http response to debug file...")
            with open("debug_log.txt","w") as f:
                f.write(page.request.method+"\n")
                f.write('request headers:\n\n\n')
                f.write(str(page.request.headers) + "\n\n\n\n")

                f.write(str(page.status_code)+"\n")
                f.write('response headers:\n\n\n')
                f.write(str(page.headers) + "\n\n")
                f.write('\n\nresponse content:\n\n\n')
                f.write(str(page.content.decode()))
            exit()

        #python probably has a built in thing but i dont give a shit
        survey_data = ""
        #shit code
        for i in range(survey_data_offset,len(page.text)):
            if page.text[i] == "\"":
                break
            survey_data += page.text[i]

        running_print(thread_id, "[*] Debug info: Status code: " + str(page.status_code) + ", \"survey_data\" parameter length: " + str(len(survey_data)))
        if wait:
            wait_time = randint(0,5000) / 1000
            running_print(thread_id, "[*] Waiting " + str(wait_time) + "s...")
            sleep(wait_time)
        
        post_data = {

            "463803414": (None, "3067519628"),
            "463803684": (None, word),
            "483089934[]": (None,"3189794655"),
            "survey_data": (None,survey_data),
            'response_quality_data': (None,'{"question_info":{"qid_463803414":{"number":1,"type":"dropdown","option_count":5,"has_other":false,"other_selected":null,"relative_position":[[2,0]],"dimensions":[5,1],"input_method":null,"is_hybrid":false},"qid_463803684":{"number":2,"type":"open_ended","option_count":null,"has_other":false,"other_selected":null,"relative_position":null,"dimensions":null,"input_method":"text_typed","is_hybrid":true},"qid_483089934":{"number":3,"type":"multiple_choice_vertical","option_count":1,"has_other":false,"other_selected":null,"relative_position":[[0,0]],"dimensions":[1,1],"input_method":null,"is_hybrid":false}},"start_time":1593393913312,"end_time":1593393973805,"time_spent":60493,"previous_clicked":false,"has_backtracked":false,"bi_voice":{}}')

        }
        #sneak 100 (shouldve used webdriver dammit)
        headers_2 = {

            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'de,de-DE;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'cache-control': 'max-age=0',
            #Chrome User agent but no chrome for boundaries (shhhhh dont tell em) 'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryxwtjXVOdBvKFA4h4'
            'origin': 'https://www.surveymonkey.com',
            'referer': 'https://www.surveymonkey.com/r/7JZRVLJ?embedded=1',
            'sec-fetch-dest': 'iframe',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36 Edg/83.0.478.54'

        }

        running_print(thread_id, "[*] Submitting survey with word \""+ word + "\"...")
        try:
            response = session.post("https://www.surveymonkey.com/r/7JZRVLJ?embedded=1", headers=headers_2, files=post_data)
            count += 1
        except requests.RequestException:
            running_print(thread_id, "[!] Can't connect to host. Do you have an existing internet connection?")
            sleep(NO_INTERNET_TIMEOUT)
            continue

        
        running_print(thread_id, "[*] Debug info: Status code: " + str(response.status_code))

        if response.status_code != 200:
            running_print(thread_id, "[!] Failed to submit survey. Please report this bug.")
            running_print(thread_id, "[!] Writing http response to debug file...")
            with open("debug_log.txt","w") as f:
                f.write(response.request.method+"\n")
                f.write('request headers:\n\n\n')
                f.write(str(response.request.headers)+"\n\n")
                f.write('\n\nrequest content:\n\n\n')
                f.write(str(response.request.body.decode())+"\n\n\n\n")

                f.write(str(response.status_code)+"\n")
                f.write('response headers:\n\n\n')
                f.write(str(response.headers)+"\n\n")
                f.write('\n\nresponse content:\n\n\n')
                f.write(str(response.content.decode()))
            exit()
        running_print(thread_id, "[*] Sumbitted survey " + str(count) + " time" + int(count -1 > 0) * "s" + " so far.")
        running_print(thread_id, "")

word = get_word()
threads = get_threads()
wait = get_wait()



print("[*] Commencing spam...")
print("[*] TIP: You can switch the focused thread by pressing s or t.")
print("\n")
#launch all threads

for i in range(threads):
    print("[*] Launching thread " + str(i+1) + " ...")
    start_new_thread(spam, (i,))

print("")

while True:

    try:
        if keyboard.is_pressed('s') or keyboard.is_pressed('t'):
            focused_thread = -1
            sleep(0.5)
            flush_input()
            print("\n\n")
            print("[*] Which thread do you want to focus on?")
            while True:
                thread = input("[*] thread (1-" + str(threads) + ") >> ")
                try:
                    thread = int(thread)
                    if thread < 1 or thread > threads:
                        print("[!] Value not in the allowed range of 1-" + str(threads) + ".")
                        continue
                    focused_thread = thread - 1
                    break
                except:
                    print("[!] Invalid input. Did you enter a number?")
                    continue
            print("\n\n")
    except:
        pass
    sleep(0.05)
