import requests as r
import os
import time

def downloadimg(link,id):
    for l in link:
        file_name = str(l).split('/')[-1].split('?')[0]
        with open(id+'/'+ file_name, "wb") as file:
                response = r.get(l)
                file.write(response.content)
                file.close()
def getimglink(res):
    link = []
    edges = res['data']['user']['edge_owner_to_timeline_media']['edges']
    for e in edges:
        is_video = e['node']['is_video']
        if(is_video is False):
            link.append(e['node']['display_url'])
        if "edge_sidecar_to_children" in e['node']:
            ne = e['node']['edge_sidecar_to_children']['edges']
            for nee in ne:
                is_video = nee['node']['is_video']
                if(is_video is False):
                    link.append(nee['node']['display_url'])
    after = res['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
    check = res['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
    return (link,after,check)
def downloadallimg(username,headers,cookies):
    s = r.Session()
    rid = s.get('https://www.instagram.com/'+ username,headers=headers,cookies=cookies).text
    st = rid.find('profilePage_') 
    e = rid.find('","show_suggested_profiles')
    id = rid[st+12:e]
    print(id)
    current_path = os.getcwd()
    try: os.mkdir(current_path + "\\"+id+"\\")
    except:pass

    check = True
    after = ''
    count = 0
    while(check!=False):
        imglink = []
        nextLink = f'https://www.instagram.com/graphql/query/?query_hash=003056d32c2554def87228bc3fd9668a&variables={{"id":{id},"first":12,"after":"{after}"}}'
        res = s.get(nextLink,headers=headers,cookies=cookies).json()
        imglink,after,check = getimglink(res)
        downloadimg(imglink,id)
        count = count + len(imglink)
        print(count)
        if(check == False): break
if __name__ == "__main__":
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'}
    cookies={'ig_did':'C8BA62CD-E241-4A03-91FD-1C8B673D34FA','mid':'YEgxiQALAAFRj1I2obsNVXJmSPaD','ig_nrcb':'1','csrftoken':'QjZLwOu1TuBWsIFdWn2xxXMVFaP4cvQr','ds_user_id':'46244324767','sessionid':'46244324767:otqfgaqfcKhd2e:8','rur':'PRN'}
    username = 'trang.zee18'
    downloadallimg(username,headers,cookies)

    



