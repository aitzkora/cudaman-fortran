#!/usr/bin/python
from bs4.element import NavigableString
from bs4 import BeautifulSoup
import re
from datetime import date
import os
import requests

def open_file():
  url = "https://docs.nvidia.com/hpc-sdk/compilers/cuda-fortran-prog-guide/index.html"
  html_text = requests.get(url).text
  soup = BeautifulSoup(html_text, "html.parser")
  return soup 

def find_functions(soup):
  name_functions = {}
  for p in soup.find_all("div", class_="section-link"):
      pat=re.compile("^#\D{2}-\D*")
      ref = p.contents[0].get("href")
      if pat.match(ref) != None:
          strs = p.contents[0].string.split()
          index = strs[0]
          pat2 = re.compile("\d{1}\.\d+\.\d+")
          if pat2.match(index) != None:
              name_functions[strs[1]] = ref[1:]
  return name_functions

def textFun(soup, fun):
    resInter = soup.find_all(id=fun)
    if resInter != None:
       z = [] 
       s = resInter[0].find_all(class_="body conbody")[0].contents
       for i in range(len(s)):
           if s[i].__class__ != NavigableString:
               z.append(s[i].get_text())
       return z 

if __name__ == '__main__':
   soup = open_file()
   funs = find_functions(soup)
   texts = {}
   output_dir = "man8"
   man_section_no = 8
   i = 0
   for nameFunc in funs.keys():
       texts[nameFunc] = textFun(soup, funs[nameFunc])
       os.system("mkdir -p %s"%output_dir)
       with open("%s/%s.html"%(output_dir, nameFunc), "w") as f:
            f.write("<h1>NAME</h1>\n%s\n\n" % nameFunc)
            f.write("<h1>SYNTAX</h1>\n%s\n" % texts[nameFunc][0])
            f.write("<h1>DESCRIPTION</h1>\n")
            f.write(texts[nameFunc][1])
            if len(funs[nameFunc])> 2 :
              f.write("<h1>NOTE</h1>\n")
              for i in range(len(texts[nameFunc])):
                  if i >= 2 :
                      f.write(texts[nameFunc][i])
       template_file = "./template.man"
      
       variables = {"man_title":nameFunc,
                    "date":date.today().strftime("%d/%m/%y"),
                    "man_lfooter":"NVIDIA CUDA FORTRAN",
                    }
       cmd_var = " ".join(["-V '%s:%s'"%(k,v) for k,v in variables.items()])

       os.system("pandoc -t man -f html %s/%s.html -o %s/%s.%d --template=%s %s"%
              (output_dir, nameFunc, output_dir, nameFunc,
               man_section_no, template_file, cmd_var))
       os.system("rm %s/%s.html"%(output_dir, nameFunc))
