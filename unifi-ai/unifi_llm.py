from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import Document, SummaryIndex, VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.readers.json import JSONReader
import matplotlib.pyplot as plt
import unifi
import json
from pylatexenc.latex2text import LatexNodes2Text
from sympy import init_printing
init_printing()

# Initialize Gemma as the LLM 
Settings.llm = Ollama(
            model="gemma4", 
                request_timeout=360.0, 
                    thinking=True # Enables built-in step-by-step reasoning on supported models
                    )

Settings.embed_model = OllamaEmbedding(model_name="embeddinggemma")

hostid = unifi.get_id()
siteid = unifi.get_site_id(hostid)
host_info = json.dumps(unifi.get_host_by_id(hostid))
clients = json.dumps(unifi.get_clients(siteid, hostid))
json_str = json.dumps(unifi.get_devices(hostid))
acls = json.dumps(unifi.get_acls(siteid, hostid))
fw_policies = json.dumps(unifi.get_firewall_policies(siteid, hostid))
traffic_lists = json.dumps(unifi.get_traffic_matching_lists(siteid, hostid))
wifi_broadcasts = json.dumps(unifi.get_wifi_broadcasts(siteid, hostid))
reader = JSONReader()
documents = [
    Document(
        text=str(host_info), 
        metadata={"source_type": "External API - Host"}
    ),
    Document(
        text=str(json_str), 
        metadata={"source_type": "External API - Devices"}
    ),
    Document(
        text=str(clients), 
        metadata={"source_type": "External API - Clients"}
    ),
    Document(
        text=str(acls), 
        metadata={"source_type": "External API - ACLs"}
    ),
    Document(
        text=str(fw_policies), 
        metadata={"source_type": "External API - Firewall Rules"}
    ),
    Document(
        text=str(traffic_lists), 
        metadata={"source_type": "External API - Firewall Rules"}
    ),
    Document(
        text=str(wifi_broadcasts), 
        metadata={"source_type": "External API - Wifi Broadcasts"}
    )
]

def save_latex_as_png(latex_str, filename):
    # Create a figure with no axes
    fig = plt.figure(figsize=(3, 1))
    #fig.text(0.5, 0.5, f'${latex_str}$', size=30, va='center', ha='center')
    fig.text(0.5, 0.5, f'${latex_str}$', size=30)
    
    # Save the figure, trimming whitespace
    plt.savefig(filename, bbox_inches='tight', pad_inches=0.1, transparent=True)
    plt.close()

index = SummaryIndex.from_documents(documents)
query_engine = index.as_query_engine()

#response = query_engine.query("What was the status returned by the API?")
#response = query_engine.query("What is your detailed summary of the response from both APIs?")
#print(response)
#response = query_engine.query("Plrase create a diagram of the network topology showing how all these devices are connected.")
#print(response)
#response = query_engine.query("Should I update the crontrollers?")
#print(response)
#response = query_engine.query("Evaluate the effectiveness of the access control lists (ACLs) and make any recommendations for new ACL rules.")
#print(response)
#response = query_engine.query("Evaluate the effectiveness of the firewall policies and make any recommendations for new firewall rules to improve security.")
#print(response)
#response = query_engine.query("List all clients from most active to least active.")
#print(response)

response = query_engine.query("You are a network engineer and project manager. Please summarize all the data you have seen about this network and provide any recommendations you think would make it better and more efficient. Provide a comprehensive review of the firewall rules. Identify each service allowed in and the destination. Identify and security weaknesses with existing rules.")
print(response)
