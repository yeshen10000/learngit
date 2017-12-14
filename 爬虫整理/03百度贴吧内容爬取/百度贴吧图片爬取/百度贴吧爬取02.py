import requests
import re
import os



class Tools:
    removeImg = re.compile('<img.*?>')
    removeAddr = re.compile('<a.*?>|</a>')
    replaceLine = re.compile('<tr>|<div>|</div>|</p>|<br>')
    replaceTd = re.compile('<td>')
    replacePara = re.compile('<p.*?>')
    replaceExtraTag = re.compile('<.*?>')


    def remove(self,te):
        te = re.sub(self.removeImg,'',te)
        te = re.sub(self.removeAddr,'',te)
        te = re.sub(self.replaceLine,'\n',te)
        te = re.sub(self.replaceTd,'\t',te)
        te = re.sub(self.replacePara,'\n  ',te)
        te = re.sub(self.replaceExtraTag,'',te)
        return  te.strip()


class BDTB:
	def __init__(self, url, see_lz, floor):
		self.url = url
		self.see_lz = '?see_lz=' + str(see_lz)
		self.floor = '&pn='+str(floor)
		self.tool = Tools()


	def getHTML(self):
		base_url = self.url + self.see_lz + self.floor
		try:
			r = requests.get(base_url)
			r.raise_for_status()
			r.encoding = r.apparent_encoding
			return r.text
		except:
			return ""


	def getTitle(self):
		pattern = re.compile('<h3 class="core_title_txt.*?>(.*?)</h3>',re.S)
		result = re.search(pattern,self.getHTML())
		
		if result:
			
			return result.group(1).strip()
		else:
			return ""

	def getPageNum(self):
		pattern = re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>',re.S)
		result = pattern.search(self.getHTML())
		if result:
			
			return result.group(1).strip()
		else:
			return ""

	def getContent(self):
		pattern = re.compile('<div id="post_content_.*?>(.*?)</div>')
		result = pattern.findall(self.getHTML())

		contents = []
		for item in result:
			content = '\n' + self.tool.remove(item)+'\n'
			contents.append(content)

		return contents

	def fileIn(self):
		with open(os.getcwd()+'/'+self.getTitle()+'.txt','w+') as f:
			for item in self.getContent():
				f.write(item)
		
	def start(self):
		print("该帖子的名字叫："+self.getTitle())
		print("该帖子共有"+str(self.getPageNum())+"页")

		self.fileIn()
		print("success")


def main():
	url ="https://tieba.baidu.com/p/3138733512"
	see_lz = 1
	floor = 1
	bdtb = BDTB(url,see_lz,floor)
	bdtb.start()

main()
