## workorder natural language processing
# Permissions
This was a script written for internal use by the manufacturing analytics team at Insulet Corporation. It has been reproduced for a personal repository with permission from Insulet Coroporation. 
# Rationale 
The manufacturing plant engineers and technicians use work orders to note down significant information regarding plant. While most information is numeric and easily parsable, 
there is space in the work orders for free text. This script was written as a starting off point to analyze this free text in the work order. 
# Notes
The script as it stands is fairly rudimentary. It was my first time using NLTK and a good way to familiarize myself with the package. In the future, the default nltk parsing tags would need to be modified to
better serve the specific needs of the plant, or there would need be some sort of additional filter after the parts of speech tagging. 
