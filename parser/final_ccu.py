import lin, ran, threading, sys,os


if __name__ == '__main__':
    #url = input('Input the URL: ')
    #try:
    #    os.system("./reset_env.sh")
    #except:
    #    notrhing = 0
    log = open('weblist.txt','w')
    log.close()
    log = open('sensitive_data_of_phone.txt','w')
    log.close()
    log = open('sensitive_data_of_id.txt','w')
    log.close()
    maxn = input('Input the size: ') 
    url = input('Input the URL: ') #'http://osl.cs.ccu.edu.tw/'
    num = 1
    t = threading.Thread(target=ran.retrieve_data , args = (url,num,maxn))
    t.start()
    
