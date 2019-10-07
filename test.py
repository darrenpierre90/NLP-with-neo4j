from neo4j import GraphDatabase
from py2neo import Graph, Node, Relationship
db = Graph("bolt://localhost:7687",auth=('neo4j', 'Basketball77'))
import newspaper

from newspaper import ArticleException


uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "Basketball77"))


class URL:
       def __init__(self, urlString):
            try:
                  url=newspaper.Article(url=urlString, language='en')
                  self.urlString=urlString
                  url.download()
                  url.parse()
                  self.authors=url.authors
                  self.title=url.title
                  url.nlp()
                  self.keywords=tuple(url.keywords)
                  self.urlString=urlString
            except ArticleException:
                  print("Could not create object for" + urlString)


def graphDb(url):
      try :
            node = Node("Article", title=url.title, urlString=url.urlString)
            for keyword in url.keywords:
                  kw=Node("Keyword",word=keyword)
                  relation=Relationship(node, "KEYWORD IS", kw)
                  db.create(relation)

            for author in url. authors:
                  kw=Node("Author",author=author)
                  relation=Relationship(node, "AUTHOR IS", kw)
                  db.create(relation)
      except:
            print("could not process" + url)

def getArticlesFromJson():

      import json 
      import re 
      exp='(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})'
      with open('articles.json') as file:
            datastore = json.load(file)
            messages= datastore['messages']
            listOfLinks= list()
            
            for msg in messages:
                  links = re.findall(exp, msg['text'])
                  if len(links) > 0 :
                        listOfLinks+=links
                        
            return listOfLinks



def main():
      links= getArticlesFromJson()
      for link in links:
            graphDb(URL(link))

      
      
      
      
main()



