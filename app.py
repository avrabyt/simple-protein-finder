import streamlit as st
from Bio import Entrez
from Bio import SeqIO
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Set the database to search and the return type to 'fasta'
Entrez.email = 'your_email@example.com'
search_criteria = 'Type 1 GPCR  AND Human [Organism] NOT olfactory'
search_text = st.text_area("Enter Search Criteria",value = search_criteria, help="For logic check : https://biochem.slu.edu/bchm628/handouts/2013/Entrez_boolian_searches.pdf")

if len(search_text) == 0:
    st.warning("Enter Search keywords.")
else:
    search_handle = Entrez.esearch(db='protein', term = search_text, rettype='fasta', retmax=1000)
    search_result = Entrez.read(search_handle)
    max_pub = search_result["Count"]
    st.sidebar.info("Total available proetin in database: "+ str(max_pub))
    if int(max_pub) > 0 :
        inval = int(max_pub)/2
        s_limit = st.sidebar.number_input("Number of Protein to Load",value=int(inval),
                                    max_value = int(max_pub),
                                    help="Initial value is half of max. available searches.")
        if int(s_limit) > 0 :     
            if st.sidebar.checkbox("Load Protein"):
                handle = Entrez.esearch(db='protein', term = search_text, rettype='fasta', retmax=s_limit)
                searchResult = Entrez.read(handle)
                ids = searchResult["IdList"]
                handle = Entrez.efetch(db="protein", id=ids, rettype="fasta", retmode="text")
                record = handle.read()
                st.write(record.rstrip('\n'))
                st.sidebar.download_button('Download', record.rstrip('\n'))



