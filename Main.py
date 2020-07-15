from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from time import sleep
from bs4 import BeautifulSoup as BS
from html_params import *
import support_functions as SP
from chrome_options import chrome_opt

FB_USER = ""
FB_pas = ""

class Facebook(webdriver.Chrome):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print('opening "http://www.facebook.com"')
        self.get("http://www.facebook.com")
        
    def FB_login (self, user, pas):
        username = self.find_element_by_xpath('//*[@id="email"]')
        pasword = self.find_element_by_xpath('//*[@id="pass"]')
        submit   = self.find_element_by_xpath('//*[@id="u_0_b"]')
        username.send_keys(user)
        pasword.send_keys(pas)
        submit.click()
        sleep(5)
        return None

    def get_chat(self): 
    #TODO: scroll up to get more messeges
        self.last_msg_owner = None
        
        def get_msg_owner(block):
            try:
            # extract My name
                msg_owner = block.find('h5')['aria-label']
            except TypeError:
            # extract friend's name
                try:
                    msg_owner = block.find_all('div',class_='_4ldz _1t_r _p')[0]['data-tooltip-content']
                except Exception:
                    print('Unable to find message owner, loads the last message owner name..')
                    msg_owner = self.last_msg_owner
            self.last_msg_owner = msg_owner
            return  msg_owner
            
        def get_time_list(block, class_nms):
            """block : html msgs block (BS4)
           class_nms : list of str or a str of class name on html"""
            time_list = []
            if isinstance(class_nms, list): 
                for class_nm in class_nms:
                    time_list = time_list + block.find_all('div', class_nm)
            elif isinstance(class_nms, str):
                time_list = time_list + block.find_all('div', class_nms)
            time_list = [str(i['data-tooltip-content']) for i in time_list]
            time_list = [SP.parse_date_str_to_num(i) for i in time_list]
            return sorted(time_list)
        
        sleep(5)    
        chat_json = []
        source = self.page_source
        soup = BS(source, 'html.parser')
        msgs_list = soup.find_all("div", class_= messeges_class)[0]
        msgs_blocks = msgs_list.find_all('div', class_=block_msgs_class) #_1t_p clearfix
        for block in msgs_blocks:
            block_msg_list = block.find_all('span', class_=msgs_class)
            my_time_list = get_time_list(block, my_msgs_class_list)
            friend_time_list = get_time_list(block, friend_msgs_class_list)
            msg_owner = get_msg_owner(block)
            time_list_to_render = my_time_list if len(my_time_list) > len(friend_time_list) \
                                                                else friend_time_list 
            print(msg_owner)
            block_json = {'owner' : msg_owner,
                                'messages' : []}
            for i, msg in enumerate(block_msg_list):
                print(time_list_to_render[i])
                block_json['messages']. append({'time' : time_list_to_render[i]})
                print(msg.text)
                block_json['messages'][-1]['message'] = msg.text
              
            chat_json.append(block_json)
            print('-_-_-_-_') #clocks seperator
        return chat_json
        
    def currentFrame(self):
        return SP.currentFrame(self)
        
    def start_chat_with(self, user_id= None):
        url_chat = "https://www.facebook.com/messages/t/" \
                        +user_id
        print("Loading FB Messengar")
        self.get(url_chat)
        print("Succeed")
        self.switch_to.frame(0)
        print("frame changed")
        sleep(5)
        
    def send_msg(self,  msg_str):
        i1 = '//*[@id="placeholder-7dp2n"]'
        # '//*[@id="cch_f959efea265e54"]/div[2]/div[2]'
        #'//*[@id="cch_f959efea265e54"]/div[2]/div[2]/div[2]/div'
        # //*[@id="cch_ff0e2a155ffd44"]/div[2]/div[2]/div[2]/div/div[4]/div/div/div[1]/div/div/div
        # 
        print("getting input..")
        wait = WebDriverWait(self, 20)
        input = wait.until(EC.visibility_of_element_located((By.XPATH, i1)))
        # input = self.find_element_by_xpath('//*[@id="placeholder-9q0jo"]')
        print("located")
        input.send_keys(msg_str)
        return None
            


if __name__ == '__main__' :     
    fb = Facebook(chrome_options=chrome_opt)
    fb.FB_login(FB_USER, FB_pas)
    # fb.strt_msngr()
    fb.start_chat_with("100009438849393") #100009438849393
    fb.send_msg("DDDDD")
    # sleep(10)
    # print(fb.get_chat())


    input("press enter to finish")
    fb.close()

