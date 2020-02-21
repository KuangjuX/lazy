from selenium import webdriver
import time
import threading

# get login url
browser=webdriver.Chrome("")
browser.get("https://passport.zhihuishu.com/login?service=http://online.zhihuishu.com/onlineSchool/")


def login(number,password):
    phone_number=browser.find_element_by_id('lUsername')  # select by id
    pwd=browser.find_element_by_id('lPassword')
    login_btn=browser.find_element_by_class_name('wall-sub-btn')

    phone_number.send_keys(number)  # input the message
    pwd.send_keys(password)
    login_btn.click()  # click the button


def to_course(key):

    time.sleep(5)
    current = browser.current_window_handle  # jump to the current handle
    key = browser.find_element_by_link_text(key)  # find the course
    key.click()
    time.sleep(1)    # wait for the course load

    # jump to the new window
    handles=browser.window_handles
    for handle in handles:
        if handle!=current:
            browser.driver.switch_to_window(handle)

    time.sleep(10)
    try:
        video=browser.find_element_by_id("mediaplayer")  # 定位视频窗口
        video.click()  # 点击播放

    except:
        pass


# 判断是否有答题窗口弹出
def is_exist():
    while True:
        try:
            browser.switch_to.default_content()
            browser.switch_to.frame('tmDialog_iframe')  # 答题窗口在另一个frame里,要切换
            box=browser.find_element_by_class_name('answerOption')  # 答题列表
            radio=box[0].find_element_by_tag_name('input')  # 找到第一个选项
            radio.click()  # 选择
            browser.switch_to.default_content()
            browser.find_element_by_link_text("关闭").click()  # 关闭答题窗口
        except:
            browser.switch_to.parent_frame()  # 没有弹出，切换回本来的frame
        time.sleep(5)

# 判断当前视频是否结束
def is_end():
    while True:
        try:
            video=browser.find_element_by_id("mediaplayer")  # 定位视频窗口
            # 获取当前播放的进度
            current_time=video.find_element_by_class_name("currentTime").get_attribute("textContent")
            # 该视频的总时间
            total_time=video.find_element_by_class_name("duration").get_attribute("textContent")
            print(current_time,total_time)
            if current_time==total_time:
                #  当前视频播放结束，点击下一节
                js="document.ElementById('nextBtn')"  # js脚本
                browser.execute_script(js)

            time.sleep(10)  # 10秒检测一次
        except:
            current_time='00:00'
            total_time='00:01'


if __name__=='__main__':

    number=""
    password=""
    login(number,password)

    # 开两个线程

    t1=threading.Thread(target=is_exist)
    t2=threading.Thread(target=is_end)
    t2.start()
    time.sleep(3)
    time.sleep()
    t1.start()
    t2.join()
    t1.join()