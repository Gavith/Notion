from bs4 import BeautifulSoup
import os

# html content
with open("index.html", "r", encoding='utf-8') as html_file:
   html_content = html_file.read()
    
soup = BeautifulSoup(html_content, 'html.parser')

# Find ALL lesson names (use find_all instead of find)
names = soup.find_all('h4', class_='text-black font-semibold text-base mb-4')

# count varialble
count = 1

# print the lesson names
for name in names:  
    with open('Recording.txt', 'a', encoding='utf-8') as file: # add file name recording file
        # ignore the Morning Sum and Payment only
        if name.text[:22] == 'Morning Sum Discussion' or name.text.strip().lower()[-3:] == 'pdf' or name.text.strip().lower()[:7] == 'payment': 
            continue
        else:
            # append name
            file.write(f"{count}. {name.text} \n")
        
    # increase count
    count += 1

print("Get all lessong successfully.....") # print successfull  massage

# opent file
print('Opening Recording....')
os.system('notepad Recording.txt')
os.system('exit')
