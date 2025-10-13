from bs4 import BeautifulSoup
import os
import ollama

# html content
with open("index.html", "r", encoding='utf-8') as html_file:
   html_content = html_file.read()
    
soup = BeautifulSoup(html_content, 'html.parser')

# Find ALL lesson names (use find_all instead of find)
names = soup.find_all('h4', class_='text-black font-semibold text-base mb-4')

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------

# # count varialble
# count = 1

# # print the lesson names
# for name in names:  
#     with open('Recording.txt', 'a', encoding='utf-8') as file: # add file name recording file
#         # ignore the Morning Sum and Payment only
#         if name.text[:22] == 'Morning Sum Discussion' or name.text.strip().lower()[-3:] == 'pdf' or name.text.strip().lower()[:7] == 'payment': 
#             continue
#         else:
#             # append name
#             file.write(f"{count}. {name.text} \n")
        
#     # increase count
#     count += 1

# print("Get all lessong successfully.....") # print successfull  massage


#------------------------------------------------------ --------------------------------------------------------------------------------------------------------------------------

recording = []

for name in names:
    if name.text[:22] == 'Morning Sum Discussion' or name.text.strip().lower()[-3:] == 'pdf' or name.text.strip().lower()[:7] == 'payment':
        continue
    else:
        recording.append(name.text)



# setup ollama Deepseek ai

def deepseek_sort(message):
    response = ollama.chat(
        model='deepseek-v3.1:671b-cloud',
        messages=[{'role': 'user', 'content': message}]
        )
    return response.message.content

# call the deepseek function
print(f'Suf of recording (∑) ==> {len(recording)}')
print('Summarizing recordings....')
sort_rec = deepseek_sort(f'''

    {recording}

    Task:
1. Group all lessons that belong to the same topic (for example, all lessons starting with or related to “සරල රේඛාව” should go together).
2. Detect topic names written in Sinhala such as:
   - සරල රේඛාව
   - බලය
   - අවකලනය
   - ප්‍රක්ශිප්ත
   - ප්‍රවේගකාල ප්‍රස්තාර
   - Any others like that lesson name .
3. Inside each topic, sort lessons in logical or numerical order (like Day 01, 02, 03… or 01, 02, 03…).
4. Renumber each group starting from 1.
5. If any lesson doesn’t clearly belong to a main topic, put it under:
   Topic: Miscellaneous
6. Output the result in this format:

Topic: [Topic Name]
1. [Lesson name]
2. [Lesson name]
3. [Lesson name]
...


    ''')


with open('Recording.txt', 'w', encoding='utf-8') as file:
    file.write(sort_rec)

# opent file
print('Opening Recording....')
os.system('notepad Recording.txt')
