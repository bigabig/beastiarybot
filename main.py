import random
import threading
import time

import pyautogui
from pynput.keyboard import Key, Listener

POE_INSTANCE = 0


def random_ease():
    i = random.randint(0, 4)
    if i == 0:
        return pyautogui.easeInQuad
    if i == 1:
        return pyautogui.easeOutQuad
    if i == 2:
        return pyautogui.easeInOutQuad
    if i == 3:
        return pyautogui.easeInBounce
    if i == 4:
        return pyautogui.easeOutBounce
    if i == 5:
        return pyautogui.easeInOutBounce
    if i == 6:
        return pyautogui.easeInElastic
    if i == 7:
        return pyautogui.easeOutElastic
    if i == 8:
        return pyautogui.easeInOutElastic


def random_time():
    return 0.1 + 0.3 * random.random()


def sleep():
    time.sleep(random_time())


def click_inventory(x, y, t, right=False):
    top_x = 577
    top_y = 429
    width = 436
    height = 181
    step_x = width / 12
    step_y = height / 5
    start_x = top_x + int(step_x / 2)
    start_y = top_y + int(step_y / 2)
    variation = 6
    click_random_in_area(int(start_x + x * step_x - variation),
                         int(start_y + y * step_y - variation),
                         2 * variation,
                         2 * variation,
                         t,
                         right)


def click_random_in_area(start_x, start_y, width, height, t, right=False):
    x = random.randint(start_x, start_x + width)
    y = random.randint(start_y, start_y + height)
    if t > 0:
        pyautogui.moveTo(x, y, t, random_ease())
    if right:
        pyautogui.click(x, y, button='right')
    else:
        pyautogui.click(x, y)


def focus_poe():
    emulator = pyautogui.getWindowsWithTitle('Path of Exile')

    # emulator is not started
    if emulator is None or len(emulator) == 0:
        print('ERROR: PoE is not running!')
        exit()

    # focus
    emulator[POE_INSTANCE].activate()


def open_beastiary():
    pyautogui.press('h')  # press the Enter key
    sleep()
    click_random_in_area(302, 101, 46, 14, random_time())
    sleep()
    click_random_in_area(413, 470, 21, 30, random_time())


def open_inventory():
    pyautogui.press('i')  # press the Enter key


def select_beast_orb(i):
    click_inventory(0, int(i / 10), random_time(), True)


def select_beast():
    click_random_in_area(76, 204, 45, 40, random_time())


def itemize_beasts():
    i = 0
    for x in range(12):
        for y in range(5):
            select_beast_orb(i)
            sleep()
            select_beast()
            sleep()
            click_inventory(11 - x, y, random_time())
            sleep()
            i = i + 1


def trade_inventory():
    pyautogui.keyDown('ctrl')
    for x in range(12):
        for y in range(5):
            click_inventory(x, y, 0, right=False)
    pyautogui.keyUp('ctrl')
    click_random_in_area(67, 593, 84, 12, random_time())


def accept_trade():
    while True:
        position = pyautogui.locateCenterOnScreen('img/accept_trade.png', grayscale=True, confidence=0.8)
        if position is not None:
            click_random_in_area(position.x - 120, position.y - 5, 90, 10, 0)
        time.sleep(1)


def main():
    x = threading.Thread(target=accept_trade, daemon=True)
    x.start()

    # Collect events until released
    with Listener(
            on_release=on_release) as listener:
        listener.join()


def on_release(key):
    print('{0} release'.format(
        key))
    if key == Key.f8:
        # Stop listener
        return False

    if key == Key.f5:
        open_beastiary()
        sleep()
        open_inventory()
        sleep()
        itemize_beasts()

    if key == Key.f6:
        trade_inventory()


if __name__ == '__main__':
    main()
