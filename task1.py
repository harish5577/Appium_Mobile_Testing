from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
import time

# ---------------------------
# Driver setup
# ---------------------------
options = UiAutomator2Options()
options.platform_name = "Android"
options.device_name = "Android"
options.automation_name = "UiAutomator2"

driver = webdriver.Remote("http://localhost:4723", options=options)
wait = WebDriverWait(driver, 20)


print("Connected to device")

# ---------------------------
# Swipe up to unlock
# ---------------------------
w, h = driver.get_window_size().values()
driver.swipe(w // 2, int(h * 0.8), w // 2, int(h * 0.3), 800)

print("Swipe done")

# ---------------------------
# Enter PIN: 7 1 0 1
# ---------------------------
for digit in "7101":
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, f"//*[@text='{digit}']")
    )).click()
    time.sleep(0.3)

print("PIN entered")

# ---------------------------
# Click Enter button
# ---------------------------
wait.until(EC.element_to_be_clickable(
    ("accessibility id", "Enter")
)).click()

print("Enter clicked")

# ---------------------------
# Screen size
# ---------------------------
size = driver.get_window_size()
width = size["width"]
height = size["height"]

center_x = width // 2

# ---------------------------
# Step 1: Swipe from TOP to open Notification Bar
# ---------------------------
driver.swipe(
    center_x,
    int(height * 0.01),   # top edge
    center_x,
    int(height * 0.4),    # 40% down
    600
)

print("Notification bar opened")
time.sleep(1)

# ---------------------------
# Step 2: Swipe from 40% to expand Quick Settings
# ---------------------------
driver.swipe(
    center_x,
    int(height * 0.4),    # start from middle
    center_x,
    int(height * 0.85),   # swipe down
    600
)

print("Quick settings expanded")
time.sleep(2)
# ---------------------------
# Wifi-Toggle actions
# ---------------------------
wifi_toggle = wait.until(
    EC.element_to_be_clickable((
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().descriptionContains("Wi")'
    ))
)

# Enable Wi-Fi
wifi_toggle.click()
print("Wi-Fi enabled")
time.sleep(2)

# Disable Wi-Fi
wifi_toggle = wait.until(
    EC.element_to_be_clickable((
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().descriptionContains("Wi")'
    ))
)
wifi_toggle.click()
print("Wi-Fi disabled")
time.sleep(2)
# ---------------------------
# Torch-Toggle actions
# ---------------------------
torch_toggle = wait.until(
    EC.element_to_be_clickable((
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().descriptionContains("Torch")'
    ))
)

# Enable Torch
torch_toggle.click()
print("Torch enabled")
time.sleep(2)

# Disable Torch
torch_toggle = wait.until(
    EC.element_to_be_clickable((
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().descriptionContains("Torch")'
    ))
)
torch_toggle.click()
print("Torch disabled")
time.sleep(2)


# ---------------------------
# Brightness Control
# ---------------------------
print("Starting brightness control")

# Wait for brightness slider (SeekBar)
brightness_slider = wait.until(
    EC.presence_of_element_located((
        AppiumBy.CLASS_NAME,
        "android.widget.SeekBar"
    ))
)

# Get slider bounds
rect = brightness_slider.rect
x_start = rect["x"]
y_center = rect["y"] + rect["height"] // 2
slider_width = rect["width"]

# Calculate min & max positions
min_x = x_start + 10
max_x = x_start + slider_width - 10

# ---------------------------
# Step 1: Set brightness to MIN
# ---------------------------
driver.swipe(
    max_x, y_center,
    min_x, y_center,
    1000
)
print("Brightness set to minimum")
time.sleep(1)

# ---------------------------
# Step 2: Increase brightness step-by-step
# ---------------------------
steps = 10  # increase resolution (more steps = smoother)
step_size = (max_x - min_x) // steps
current_x = min_x

for i in range(steps):
    next_x = current_x + step_size
    driver.swipe(
        current_x, y_center,
        next_x, y_center,
        900
    )
    current_x = next_x
    print(f"Brightness increased to step {i + 1}")
    time.sleep(0.6)

# ---------------------------
# Step 3: Set brightness to MAX
# ---------------------------
driver.swipe(
    current_x, y_center,
    max_x, y_center,
    1000
)
print("Brightness set to maximum")
time.sleep(1)

# ---------------------------
# Step 4: Decrease brightness step-by-step
# ---------------------------
steps = 10  # smoother decrease
step_size = (max_x - min_x) // steps
current_x = max_x

for i in range(steps):
    next_x = current_x - step_size
    driver.swipe(
        current_x, y_center,
        next_x, y_center,
        900
    )
    current_x = next_x
    print(f"Brightness decreased to step {i + 1}")
    time.sleep(1)

# ---------------------------
# Step 5: Set brightness to MIN
# ---------------------------
driver.swipe(
    current_x, y_center,
    min_x, y_center,
    1000
)
print("Brightness set to minimum")

# ---------------------------
# Go to Home Screen
# ---------------------------
driver.press_keycode(3)   # KEYCODE_HOME
print("Navigated to Home screen")
time.sleep(1)   

# ---------------------------
# Step 1: Open Camera App
# ---------------------------
wait.until(
    EC.element_to_be_clickable((
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().textContains("Camera")'
    ))
).click()

print("Camera app opened")
time.sleep(3)   # HARD WAIT REQUIRED

# ---------------------------
# Step 2: Capture Photo (ABSOLUTE SAFE METHOD)
# ---------------------------
print("Attempting to capture photo")

time.sleep(2)  # Let camera fully stabilize

size = driver.get_window_size()
width = size["width"]
height = size["height"]

shutter_x = width // 2
shutter_y = int(height * 0.85)

for i in range(10):
    driver.execute_script("mobile: clickGesture", {
        "x": shutter_x,
        "y": shutter_y
    })
    print(f"Photo capture click {i + 1}")
    time.sleep(6)   # IMPORTANT: camera needs time between shots
# ---------------------------
# Go to Home Screen
# ---------------------------
driver.press_keycode(3)   # KEYCODE_HOME
print("Navigated to Home screen")
time.sleep(1)    

# ---------------------------
# Cleanup
# ---------------------------
driver.quit()
print("Test completed")
