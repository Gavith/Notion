from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
import ollama
import os
import re

# --- Chrome setup ---
chrome_options = Options()
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

driver.get("https://apluseducation.lk/login")
driver.maximize_window()

wait = WebDriverWait(driver, 30)

# --- Login ---
phone = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'Phone') or contains(@type, 'tel') or contains(@name, 'mobile')]")))
password = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']")))
login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Login') or contains(., 'Sign In')]")))

phone.send_keys("YOUR_NUMBER")  # your number
password.send_keys("YOUR_PASSWORD")
login_btn.click()
print("✅ Logged in successfully")

# --- Wait for courses and click Combined Mathematics ---
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[data-cy='course-card']")))
courses = driver.find_elements(By.CSS_SELECTOR, "a[data-cy='course-card']")
for course in courses:
    if "Combined Mathematics - 2026 All Island" in course.text:
        driver.execute_script("arguments[0].click();", course)
        print("✅ Opened Combined Mathematics course")
        break

# --- Wait for month buttons and click September ---
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button[data-cy='lesson-month-btn']")))
months = driver.find_elements(By.CSS_SELECTOR, "button[data-cy='lesson-month-btn']")
for month in months:
    if "Sep" in month.text:
        driver.execute_script("arguments[0].click();", month)
        print("✅ Clicked September month")
        break

time.sleep(2)

# --- Scroll to load all lessons (React lazy load handling) ---
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # wait for new content to load
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break  # no more new content
    last_height = new_height

time.sleep(2)  # extra wait just in case

# --- Get page source and parse with BeautifulSoup ---
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()

# --- Find lesson names ---
names = soup.find_all('h4', class_='text-black font-semibold text-base mb-4')

# Filter recordings
recordings = []
for name in names:
    text = name.text.strip()
    if text.startswith("Morning Sum Discussion") or text.lower().endswith("pdf") or text.lower().startswith("payment"):
        continue
    recordings.append(text)

# --- Pre-sort lessons by day number if exists ---
def extract_day_num(lesson_name):
    match = re.search(r'(\d+)', lesson_name)
    return int(match.group(1)) if match else 0

recordings.sort(key=extract_day_num)

print(f"✅ Total recordings found: {len(recordings)}")

# --- Setup Ollama Deepseek AI ---
def deepseek_sort(message):
    response = ollama.chat(
        model='deepseek-v3.1:671b-cloud',
        messages=[{'role': 'user', 'content': message}]
    )
    return response.message.content

# --- Prepare prompt ---
prompt = f"""
{recordings}

Task:
1. Group all lessons that belong to the same topic (for example, all lessons starting with or related to “සරල රේඛාව” should go together).
2. Detect topic names written in Sinhala such as:
   - සරල රේඛාව
   - බලය
   - අවකලනය
   - ප්‍රක්ශිප්ත
   - ප්‍රවේගකාල ප්‍රස්තාර
   - Any others like that lesson name.
3. Inside each topic, sort lessons in logical or numerical order (like Day 01, 02, 03… or 01, 02, 03…).
4. Renumber each group starting from 1.
5. If any lesson doesn’t clearly belong to a main topic, put it under:
   Topic: Miscellaneous
6. Do not skip any lesson. Include all lessons exactly as listed, even if similar numbers exist.
7. Output the result in this format:

Topic: [Topic Name]
1. [Lesson name]
2. [Lesson name]
...
"""

# --- Call Deepseek ---
print("🧠 Summarizing recordings with AI...")
sort_rec = deepseek_sort(prompt)

# --- Save to file ---
with open('Recording.txt', 'w', encoding='utf-8') as file:
    file.write(sort_rec)

print("✅ Recordings saved to Recording.txt")
os.system('notepad Recording.txt')
