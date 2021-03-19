import requests as r
import os
import time


def getAllMedia(username):
    id = getUserId(username)
    current_path = os.getcwd()
    try: 
        os.mkdir(current_path + "\\"+id)
        os.mkdir(current_path + "\\"+id+"\\"+'img'+"\\")
        os.mkdir(current_path + "\\"+id+"\\"+'vid'+"\\")
    except:
        pass

    check = True
    after = ''
    while(check!=False):
        imglink = []
        nextLink = f'https://www.instagram.com/graphql/query/?query_hash=003056d32c2554def87228bc3fd9668a&variables={{"id":{id},"first":12,"after":"{after}"}}'
        try:
            res = r.get(nextLink,headers=headers).json()
        except:
            try: 
                s = r.Session()
                res = s.get(nextLink,headers=headers,cookies=cookies).json()
            except:
                return -1
        edges = res['data']['user']['edge_owner_to_timeline_media']['edges']
        lt = getLastTime(id)
        c = 0
        if(lt == ''): lt = 0
        for e in edges:
            if(e['node']['taken_at_timestamp'] > int(lt)):
                c = c + downloadNode(id,e['node'])
            else: 
                setLastTime(id)
                print(c)
                return True
        after = res['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
        check = res['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
        if(check == False): break
    setLastTime(id)
    print(c)
    return True
def getUserId(username):
    s = r.Session()
    res = s.get('https://www.instagram.com/'+ username,headers=headers,cookies=cookies).text    
    st = res.find('profilePage_') 
    e = res.find('","show_suggested_profiles')
    id = res[st+12:e]
    return id
def getLastTime(id):
    with open(id + '/log.txt', 'a') as fp: 
        fp.close()
    with open(id + '/log.txt','r') as file:
        l = file.read()
        file.close()
        return l
def setLastTime(id):
    with open(id + '/log.txt',"w") as file:
        file.write(str(int(time.time())))
        file.close()
def downloadNode(id,node):
    linkimg = []
    lingvid = []
    is_video = node['is_video']
    if(is_video is False):
        linkimg.append(node['display_url'])
    else:
        lingvid.append(node['video_url'])
    if "edge_sidecar_to_children" in node:
        n = node['edge_sidecar_to_children']['edges']
        for e in n:
            downloadNode(id,e['node'])
    downloadOne(linkimg,id,0)
    downloadOne(lingvid,id,1)
    return 1
def downloadOne(link,id,s):
    for l in link:
        file_name = str(l).split('/')[-1].split('?')[0]
        if(s): path = id + '/vid' 
        else: path = id + '/img' 
        with open(path+'/'+ file_name, "wb") as file:
                response = r.get(l)
                file.write(response.content)
                file.close()
def parsecookie(cookies):
    cookies = dict()
    temp = rawcookies.split(';')
    for i in temp:
        k,v = i.split('=')
        cookies[k] = v
    return cookies
if __name__ == "__main__":
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Mobile Safari/537.36',"accept": "*/*","accept": "*/*","accept-language": "en,vi;q=0.9,en-US;q=0.8","content-type": "application/x-www-form-urlencoded","sec-fetch-dest": "empty","sec-fetch-mode": "cors","sec-fetch-site": "same-origin","sec-gpc": "1","x-csrftoken": "LTnLQ32xkzpAWA11CVspGeuC4GAJHIbG","x-ig-app-id": "936619743392459","x-ig-www-claim": "hmac.AR3EW2rG4PIT7TdEQo5JEIZ0CyKghONMvjcHeM1yXhP7p9oS","x-instagram-ajax": "db4941e96d11","x-requested-with": "XMLHttpRequest"}
    rawcookies = 'ig_did=57EA43E9-92C2-4E2A-8910-4519B94EFC96; mid=YFLNQwALAAHAlD6sFLKxpAWYPAS3; ig_nrcb=1; csrftoken=Mg67dMuXrspyGmdrrWPyTuzrmfSGtlaZ; ds_user_id=3423384139; sessionid=3423384139%3AR1mE2IpTwx9zaU%3A24; shbid=3750; shbts=1616039309.9263468; rur=PRN'
    cookies = parsecookie(rawcookies)
    username='you_r_love'
    getAllMedia(username)
    



