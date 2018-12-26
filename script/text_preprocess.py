import wikipedia
import re
p = wikipedia.page("adolf hitler")
content = p.content.split('References')[0]
content = content.split('See also')[0]
content = re.sub(r'[=]*[a-zA-Z ü]*[=]+', '', content)
content = re.sub(r'[\n]+', '', content)
print(content)
