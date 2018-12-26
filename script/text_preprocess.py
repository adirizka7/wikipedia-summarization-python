import wikipedia
import re
p = wikipedia.page("christian bautista")
content = p.content.split('References')[0]
content = content.split('See also')[0]
content = re.sub(r'[=]*[a-zA-Z ü]*[=]+', '', content)
content = re.sub(r'[\n]+', ' ', content)
content = re.sub(r'[–:<>+=_`~!@#$%^&*;,\'()/.\"0-9-]+', ' ', content)
content = re.sub(r'[ ]+', ' ', content)
print(content)
