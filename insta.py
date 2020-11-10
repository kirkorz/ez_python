import requests as r
import os
#"id":"4499737748"
id = '3762891297'
current_path = os.getcwd()
try: os.mkdir(current_path + "\\"+id+"\\")
except:pass

linkStart = 'https://www.instagram.com/graphql/query/?query_hash=003056d32c2554def87228bc3fd9668a&variables={"id":"'+id+'","first":12,"after":""}'  
print(linkStart)
nextLink= ''
firstres = r.get(linkStart).json()
check = firstres['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
end = firstres['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
# while(check != False):
link = []
while(check != False):
    nextLink = 'https://www.instagram.com/graphql/query/?query_hash=003056d32c2554def87228bc3fd9668a&variables={"id":"'+id+'","first":12,"after":"'+end+'"}'
    print()
    res = r.get(nextLink).json()
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
    end = res['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
    check = res['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
    print(len(link))
    for l in link:
        file_name = str(l).split('/')[-1].split('?')[0]
        with open(id+'/'+ file_name, "wb") as file:
                response = r.get(l)
                file.write(response.content)
                file.close()
    link = []
    if(check == False): break

