import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# ✅ Set up Selenium WebDriver
options = Options()
options.add_argument("--headless")  # Remove this if you want to see the browser
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")

# ✅ Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# ✅ Open YouTube Trending Page
url = "https://www.youtube.com/feed/trending"
driver.get(url)

# ✅ Wait for page to load
time.sleep(5)

# ✅ Scroll down to load more videos
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(3)

# ✅ Extract video titles
videos = driver.find_elements(By.CSS_SELECTOR, "h3.style-scope.ytd-video-renderer")

video_data = []
for video in videos[:20]:  # Fetch top 20 trending videos
    title = video.text
    video_data.append(title)

driver.quit()  # Close browser

# ✅ Save data to CSV
df = pd.DataFrame(video_data, columns=["Title"])
df.to_csv("trending_videos.csv", index=False)

# ✅ Display extracted data
print(df.head())

# ✅ Create a WordCloud for trending words in video titles
text = " ".join(df["Title"])
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)

# ✅ Show WordCloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Trending YouTube Titles WordCloud")
plt.show()
