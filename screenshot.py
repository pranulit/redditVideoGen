from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
import time
import os

screenshotDir = "Screenshots"
screenWidth = 400
screenHeight = 800

def getPostScreenshots(filePrefix, script):
    print("Taking screenshots...")
    driver, wait = __setupDriver(script.url)
    
    # Capture the main post
    script.titleSCFile = __takeScreenshot(filePrefix, driver, wait, "Post")
    
    voiceover_dir = "Voiceovers"
    for commentFrame in script.frames:
        voiceover_file = os.path.join(voiceover_dir, f"{filePrefix}-{commentFrame.commentId}.mp3")
        commentFrame.isRead = os.path.exists(voiceover_file)

    # Take screenshots only for comments that have been read
    for commentFrame in script.frames:
        if commentFrame.isRead:
            print(f"Processing comment: {commentFrame.commentId}")
            commentFrame.screenShotFile = __takeScreenshot(filePrefix, driver, wait, commentFrame.commentId)
        else:
            print(f"Skipping comment: {commentFrame.commentId} (no voiceover found)")
    
    driver.quit()

def __takeScreenshot(filePrefix, driver, wait, handle="Post"):
    """
    Capture a screenshot for the post or a specific comment.
    """
    if handle == "Post":
        selector = "shreddit-post"
    else:
        selector = f"div[id='t1_{handle}-comment-rtjson-content']"

    # Try multiple attempts to find the comment, scrolling and clicking 'More Comments' if needed.
    max_attempts = 5
    for attempt in range(max_attempts):
        try:
            print(f"Attempt {attempt+1}/{max_attempts}: Waiting for element with selector: {selector}")
            # Use visibility_of_element_located instead of presence_of_element_located
            search = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
            print(f"Element found: {selector}")
            
            # Scroll to the element
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", search)
            time.sleep(1)  # Allow time for the element to come into view
            
            # Take screenshot
            fileName = f"{screenshotDir}/{filePrefix}-{handle}.png"
            with open(fileName, "wb") as fp:
                fp.write(search.screenshot_as_png)
            return fileName
        except TimeoutException:
            print(f"Timeout: Unable to locate element with selector: {selector} on attempt {attempt+1}.")
            # Before next attempt, try to load more comments and scroll down
            __loadMoreComments(driver)
            __scrollPage(driver)

    # If all attempts fail, return None
    print(f"Failed to find element after {max_attempts} attempts.")
    return None

def __loadMoreComments(driver):
    """
    Tries to click any 'More Comments' or 'Continue this thread' links to load more comments.
    """
    # Common selectors on Reddit for loading more comments
    more_comments_selectors = [
        "button[data-testid='more-comments']",
        "a[data-click-id='comments']"  # some older page styles or 'continue this thread' links
    ]
    
    for sel in more_comments_selectors:
        elements = driver.find_elements(By.CSS_SELECTOR, sel)
        for elem in elements:
            try:
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", elem)
                time.sleep(1)
                elem.click()
                print("Clicked a 'More Comments' or 'Continue' button.")
                time.sleep(2)  # wait a bit for content to load
            except (ElementClickInterceptedException, Exception):
                pass

def __scrollPage(driver, times=3):
    """Scrolls the page down multiple times to load more content."""
    for _ in range(times):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)


def __setupDriver(url: str):
    options = webdriver.FirefoxOptions()
    options.headless = False
    driver = webdriver.Firefox(options=options)
    wait = WebDriverWait(driver, 45)  # Increase wait time if needed

    driver.set_window_size(width=screenWidth, height=screenHeight)
    driver.get(url)

    # Handle terms and conditions popup if present
    try:
        popup_accept_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-testid='accept-button']"))
        )
        popup_accept_button.click()
        print("Accepted terms and conditions popup.")
    except TimeoutException:
        print("No terms and conditions popup found.")

    # Handle cookie banner popup if present
    try:
        accept_cookies_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "shreddit-interactable-element[id='accept-all-cookies-button'] button"))
        )
        accept_cookies_button.click()
        print("Accepted cookie popup.")
    except TimeoutException:
        print("No cookie popup found.")

    # Wait for the main post
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "shreddit-post")))
        print("Page fully loaded.")
    except TimeoutException:
        print("Timeout while waiting for the page to load.")

    # Initial scroll to load comments
    __scrollPage(driver, times=10)

    return driver, wait
