## Scrapybara: Research Report and Python Cookbook for Podplay and Persistent Computer Use Agents

Scrapybara represents a major advancement in orchestrating large-scale, persistent, and agentic computer use workflows, particularly for scenarios requiring virtual desktops, browser automation, and seamless integration with LLMs like OpenAI and Claude. Below is a comprehensive research report and practical Python-focused cookbook tailored for leveraging Scrapybara in "podplay" (persistent, multi-agent, multi-LLM environments), with a focus on solving the kinds of issues you faced with NixOS code-server and Oracle.

---

## **1. Overview: What is Scrapybara?**

Scrapybara is a platform and SDK for spinning up cloud-based virtual desktop instances (Ubuntu, Windows, browser) in milliseconds, giving agents full access to the desktop, browser, filesystem, and shell. It is designed for deep, persistent, and scalable computer use by AI agents, enabling:

- Instant deployment of hundreds of desktop instances
- Real-time orchestration and monitoring
- Integration with LLMs (OpenAI, Claude, etc.) for agentic workflows
- Persistent sessions (including authenticated browser states)
- Structured, multi-turn conversations and tool use[1][2]

Scrapybara’s infrastructure is ideal for persistent podplay, where multiple agents and LLMs interact continuously, maintaining context and state across sessions.

---

## **2. Key Features and Use Cases**

**Features:**

- **Lightning-fast instance spin-up:** Start Ubuntu/Windows/browser desktops in under a second[1][2].
- **Unified API/SDK:** Python and TypeScript SDKs for agent orchestration[1][4].
- **Integrated toolset:** ComputerTool, BashTool, EditTool for shell, code, and browser automation[1].
- **Persistent, authenticated sessions:** Save/load browser auth, pause/resume, and stateful workflows[2].
- **Scalable orchestration:** Run hundreds of concurrent agents with real-time control and monitoring[1].
- **Structured outputs and multi-turn conversations:** Ideal for LLM-driven agents that need to reason and act in sequence[2].

**Use Cases:**

- Automated web scraping, data extraction, and transformation at scale
- Browser automation (including login, navigation, and scraping of authenticated sites)
- Persistent research agents (e.g., for YC company analysis, as in the cookbook)
- Full-stack automation: code execution, file manipulation, and desktop actions
- Podplay: persistent, multi-agent LLM environments with long-term context retention[1][2][5]

---

## **3. Python Cookbook: Getting Started and Advanced Usage**

### **A. Installation and Setup**

```python
pip install scrapybara
```

Set your API key as an environment variable:

```bash
export SCRAPYBARA_API_KEY="your_api_key_here"
```

### **B. Spinning Up a Desktop Instance and Using Tools**

```python
from scrapybara import Scrapybara
from scrapybara.openai import OpenAI
from scrapybara.tools import ComputerTool, BashTool, EditTool

client = Scrapybara()
instance = client.start_ubuntu()  # or .start_windows(), .start_browser()

response = client.act(
    tools=[
        ComputerTool(instance),
        BashTool(instance),
        EditTool(instance)
    ],
    model=OpenAI(),
    system="You are a webscraping agent",
    prompt="Scrape all YC W25 companies"
)

messages = response.messages
print(messages)
```
This code launches an Ubuntu desktop in the cloud, attaches tools, and lets an LLM agent interact with the desktop, browser, and shell in a persistent, multi-turn workflow[1][2].

### **C. Persistent Authenticated Sessions**

- Save and reuse browser authentication states across sessions for scraping authenticated sites.
- Pause and resume desktop instances, maintaining full state.

### **D. Parallelized, Batch Workflows**

Scrapybara supports running multiple agents/instances in parallel for high-throughput tasks, e.g., contacting companies scraped from a directory, each in its own sandboxed session[2][5].

### **E. Cookbook Examples**

The [Scrapybara Cookbook](https://github.com/scrapybara/scrapybara-cookbook) provides self-contained Python and TypeScript projects, including:

- Scraping YC companies and finding contact info in parallel
- Transforming and exporting web data
- Persistent session management and advanced orchestration

Each example is ready to run with your API key and is designed for local or cloud execution[5].

---

## **4. Podplay and Persistent Multi-Agent Chat**

Scrapybara’s design is particularly suited for “podplay”:

- **Each agent or LLM gets its own persistent desktop environment.**
- **Session state (including browser, filesystem, and conversation context) is maintained across restarts and model switches.**
- **Multiple LLMs (OpenAI, Claude, etc.) can be orchestrated in parallel, each with its own desktop or browser instance.**
- **Ideal for users needing long-term context retention and seamless switching between agents/models (e.g., for neurodiverse users or research workflows).**

---

## **5. Integration with NixOS, Code-Server, and Oracle**

Scrapybara abstracts away many of the headaches associated with managing persistent desktop environments on platforms like NixOS or Oracle Cloud:

- No need to manually manage VMs or containers—Scrapybara handles orchestration, scaling, and session persistence.
- Compatible with code-server and browser-based IDEs for in-browser coding and debugging.
- Real-time monitoring, pause/resume, and multi-instance management are built-in[1][2].

---

## **6. Pricing and Access**

- Free tier: 10 compute hours, 100 agent credits, 5 concurrent instances
- Paid plans scale up to 100 concurrent instances and 500+ compute hours/month
- Credits are consumed per agent action; you can use your own OpenAI API key for LLM calls[1].

---

## **7. Community, Support, and Further Resources**

- **Cookbook and Example Gallery:** [scrapybara-cookbook on GitHub][5]
- **Dashboard and API Management:** Manage keys and instances on the Scrapybara dashboard[2].
- **Support:** Active Discord and X (Twitter) communities for help and updates[2].
- **Playground:** Try out workflows interactively (see new Next.js backend for latest playground)[6].

---

## **Summary Table: Scrapybara vs. Traditional Approaches**

| Feature                  | Scrapybara                                    | Traditional VM/Cloud Setup          |
|--------------------------|-----------------------------------------------|-------------------------------------|
| Instance Startup Time    | < 1 second                                    | Minutes                             |
| Persistent Sessions      | Yes (pause/resume, save state)                | Manual snapshot/restore             |
| LLM Integration          | Built-in (OpenAI, Claude, etc.)               | Manual API integration              |
| Parallelization          | 100s of instances, API-driven                 | Complex orchestration               |
| Authenticated Browsing   | Save/load auth, reuse across sessions         | Manual browser profile management   |
| Pricing                  | Usage-based, free tier available              | Pay-per-VM/hour                     |

---

## **Conclusion**

Scrapybara is a breakthrough for persistent, agentic, and LLM-driven computer use at scale. For podplay and persistent multi-agent chat, it provides the infrastructure and SDKs needed to create robust, stateful, and highly personalized AI workflows—solving many of the pain points of traditional VM and cloud setups, especially in NixOS/code-server/Oracle environments.

For hands-on code and more advanced recipes, see the [Scrapybara Cookbook][5] and [official docs][2]. If you want to build persistent, multi-LLM, multimodal chat environments with full desktop and browser access, Scrapybara is a proven foundation.

---
## Scrapybara: Full Instruction Manual & Copy Scraper Guide for Doc Site → mem0 Database

This manual provides a comprehensive, step-by-step guide to using Scrapybara for spinning up computer-use agents, scraping documentation sites (using the "copy scraper" feature), and uploading data to your mem0 database. It synthesizes official docs, API references, and cookbook examples for a robust, production-grade workflow.

---

## **1. Getting Started**

**Installation**

```bash
pip install scrapybara
```
Set your API key:
```bash
export SCRAPYBARA_API_KEY="your_api_key"
```


---

## **2. Core Concepts**

- **Instance:** A cloud-hosted Ubuntu, Windows, or Browser session with full desktop, shell, and browser access.
- **Tools:** Modular interfaces (ComputerTool, BashTool, EditTool) for interacting with the instance.
- **Act SDK:** Orchestrates multi-turn, LLM-driven actions using tools.
- **Auth States:** Persist and reuse browser authentication for scraping logged-in content.
- **Conversations:** Structured, multi-step agent workflows.
- **Copy Scraper (Copycapy):** Automated doc-site scraper, outputs structured data.

---

## **3. Spinning Up Instances**

**Python Example: Start Ubuntu Desktop**

```python
from scrapybara import Scrapybara
client = Scrapybara()
instance = client.start_ubuntu()
```


**API Reference:**  
- `/start` endpoint for instance creation (supports `instance_type`, `timeout_hours`, etc.)[2]
- `/get-instances` to list running instances

---

## **4. Using Tools**

Attach tools for agent actions:

```python
from scrapybara.tools import ComputerTool, BashTool, EditTool

tools = [
    ComputerTool(instance),
    BashTool(instance),
    EditTool(instance)
]
```


---

## **5. Agent Actions: Act SDK**

Let an LLM agent control the instance:

```python
from scrapybara.openai import OpenAI

response = client.act(
    tools=tools,
    model=OpenAI(),
    system="You are a doc-site scraper",
    prompt="Scrape the documentation at https://example.com/docs"
)
print(response.messages)
```


---

## **6. Browser Automation & Auth States**

- **Start browser:** `client.start_browser()`
- **Save/load auth:** Use `/browser/save-auth` and `/browser/authenticate` endpoints for persistent login[6]
- **Get/set current URL:** `/browser/get-current-url`
- **Pause/resume:** `/instance/pause` and `/instance/resume` to persist session state

---

## **7. The Copy Scraper (Copycapy) Feature**

**Purpose:** Scrape structured content from documentation sites, preserving hierarchy and metadata.

### **Using the Copycapy Cookbook**

- Official example: [copycapy in scrapybara-cookbook][13]
- Supports scraping docs, exporting as JSON/Markdown, and further processing

**Python Example:**

```python
from scrapybara.cookbook.copycapy import run_copycapy

# Scrape docs and save as JSON
run_copycapy(
    url="https://docs.example.com",
    output_path="scraped_docs.json"
)
```


**Features:**
- Handles navigation, content extraction, and structure
- Can be customized for different doc-site layouts

---

## **8. Uploading to mem0 Database**

Assuming mem0 exposes an API or supports direct Python integration:

```python
import requests
import json

with open("scraped_docs.json") as f:
    docs = json.load(f)

for doc in docs:
    requests.post("https://your-mem0-endpoint/upload", json=doc)
```
*Replace with your actual mem0 upload logic.*

---

## **9. Best Practices**

- **Use Auth States** for authenticated scraping[6]
- **Pause/Resume** long-running sessions to save credits
- **Monitor** with `/get-instances` and `/instance/screenshot` for debugging
- **Batch & Parallelize**: Run multiple agents for high-throughput scraping
- **Use Conversations** for multi-step, multi-turn scraping and data post-processing[7]

---

## **10. CLI and Advanced Features**

- **scrapybara-cli:** Command-line interface for quick tasks and automation[17]
- **Computer Use Playground:** Experiment interactively with agent workflows[19]
- **Wide Research:** For broad, multi-site research/scraping[15][16]
- **Notebook API:** Run code and manage Jupyter-like notebooks inside instances

---

## **11. Reference: Key Endpoints & SDK Methods**

| Feature            | SDK/Endpoint Example                           | Description                                        |
|--------------------|-----------------------------------------------|----------------------------------------------------|
| Start Instance     | `client.start_ubuntu()` / `/start`            | Launch desktop/browser instance                     |
| Pause/Resume       | `/instance/pause`, `/instance/resume`         | Save/restore session state                          |
| Auth State         | `/browser/save-auth`, `/browser/authenticate` | Save/load browser login state                       |
| Computer Actions   | `/instance/computer`, `/instance/bash`        | Run shell, code, or edit files                      |
| File Upload        | `/instance/upload`                            | Upload files to instance                            |
| Notebook           | `/notebook/create`, `/notebook/execute`       | Manage and run code notebooks                       |
| Screenshot         | `/instance/screenshot`                        | Capture desktop/browser screenshots                 |
| Copy Scraper       | `run_copycapy()` (cookbook)                   | Scrape doc sites, output structured content         |

---

## **12. Example: Full Doc Site Scraper to mem0**

```python
from scrapybara import Scrapybara
from scrapybara.cookbook.copycapy import run_copycapy
import requests
import json

# 1. Scrape docs
run_copycapy(
    url="https://docs.example.com",
    output_path="scraped_docs.json"
)

# 2. Upload to mem0
with open("scraped_docs.json") as f:
    docs = json.load(f)

for doc in docs:
    requests.post("https://your-mem0-endpoint/upload", json=doc)
```


---

## **13. Resources**

- [Scrapybara Features][1]
- [API Reference][2]
- [Copycapy Cookbook][13]
- [Best Practices][5]
- [Auth States][6]
- [Conversations][7]
- [CLI Guide][17]
- [Wide Research][15][16]
- [Computer Use Playground][19]

---

## **Summary**

Scrapybara enables you to automate doc-site scraping at scale, persist browser sessions, and upload structured data to your database, all with a Pythonic, LLM-driven workflow. For the copy scraper, use the Copycapy cookbook, and for robust orchestration, leverage the Act SDK and best practices outlined above.

**For further customization, consult the [Scrapybara documentation](https://docs.scrapybara.com/) and [cookbook](https://docs.scrapybara.com/cookbook).**
Yes, you can adapt your Scrapybara-based workflow to use Gemini 2.5 as the LLM backend. Google’s Gemini 2.5 models—including "gemini-2.5-pro-preview-03-25"—are available via both the direct Gemini API and through Vertex AI, and can be integrated into your Python applications similarly to earlier Gemini versions[1].

---

## How to Adapt for Gemini 2.5

**1. Model Name Update:**  
The main change is to specify the correct model name for Gemini 2.5 in your API calls. For Gemini 2.5 Pro Preview, use:
- `"gemini-2.5-pro-preview-03-25"`

**2. API Access Methods:**  
You can use either:
- **Direct Gemini API** (via `google-generativeai` Python package)
- **Vertex AI** (via `google-cloud-aiplatform` and `vertexai.generativemodels` packages)

**3. Example: Using Gemini 2.5 with the Direct API**

```python
import os
import google.generativeai as genai

os.environ["GEMINI_API_KEY"] = "your-api-key"
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-2.5-pro-preview-03-25")
response = model.generate_content("Your prompt here")
print(response.text)
```


**4. Example: Using Gemini 2.5 with Vertex AI**

```python
import os
from google.cloud import aiplatform
from vertexai.generativemodels import GenerativeModel

os.environ["GOOGLE_CLOUD_PROJECT"] = "your-project-id"
os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path-to-your-service-account.json"

aiplatform.init(project=os.environ["GOOGLE_CLOUD_PROJECT"], location=os.environ["GOOGLE_CLOUD_LOCATION"])

model = GenerativeModel("gemini-2.5-pro-preview-03-25")
response = model.start_chat().send_message("Your prompt here")
print(response.text)
```


**5. Integration with Scrapybara**
- Replace the model initialization and response generation in your Scrapybara agent code with the above logic, ensuring you pass the correct model name.
- If your workflow or SDK expects a model name parameter, simply supply `"gemini-2.5-pro-preview-03-25"`.

**6. Notes**
- Ensure your Google Cloud project has access to Gemini 2.5 (some models may be in preview or require allow-listing).
- For advanced features (multimodality, function calling, etc.), refer to the latest Gemini and Vertex AI documentation[1][2].

---

**Summary Table: Key Gemini 2.5 Model Names**

| Model Name                 | API Code/ID                       | Capabilities                |
|----------------------------|-----------------------------------|-----------------------------|
| Gemini 2.5 Pro Preview     | gemini-2.5-pro-preview-03-25      | Advanced reasoning, coding  |
| Gemini 2.0 Flash           | gemini-2.0-flash                  | Real-time streaming         |

---

**Conclusion:**  
You can use Gemini 2.5 by updating your model selection logic and API calls to reference the new model identifier. The integration pattern (prompting, chat history, multimodal support) remains the same as with previous Gemini versions[1].

[1] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_bd9d41a1-4e62-40ae-b957-3bc5634177f6/49a8435d-1cc2-42f7-9686-1577c400c485/Vertex-and-gemini-guide.txt
[2] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_bd9d41a1-4e62-40ae-b957-3bc5634177f6/06adf0c9-de56-489f-ac27-9d4924928fc0/research-multimodel-2.txt
[3] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_bd9d41a1-4e62-40ae-b957-3bc5634177f6/f884b014-b47b-4f1a-962b-e2ea517935ea/GEMIN-API-SUPER-GUIDE.txt
[4] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_bd9d41a1-4e62-40ae-b957-3bc5634177f6/7d356496-389a-4d1a-84c4-3cb4ba24ba17/Pasted-Talk-with-AI-live-Interact-with-AI-models-using-text-code-images-audio-or-upload-files-Model-1744231659957.txt
[5] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_bd9d41a1-4e62-40ae-b957-3bc5634177f6/5fb0ad98-380e-4519-88f1-b93f7d5455df/GEMINI-API-GUIDE.txt
[6] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_bd9d41a1-4e62-40ae-b957-3bc5634177f6/3282e7df-05bb-4798-83ab-3e5cb48c77e0/Copy-of-Persistent-Multimodal-AI-Chat-via-API.txt
[7] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_bd9d41a1-4e62-40ae-b957-3bc5634177f6/0ac52e87-e29c-4d67-8605-69d1781dcf35/LiveAPIGuide.txt
[8] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_bd9d41a1-4e62-40ae-b957-3bc5634177f6/90666cc1-086a-4d3f-ac77-5dee66502f11/Pasted-PostgreSQL-database-connected-successfully-Talk-with-AI-live-Interact-with-Gemini-using-text-c-1744227817739.txt
---

**References:**  
[1]: scrapybara.com/#features  
[2]: docs.scrapybara.com/api-reference/start  
[5]: docs.scrapybara.com/best-practices  
[6]: docs.scrapybara.com/auth-states  
[7]: docs.scrapybara.com/conversations  
[13]: docs.scrapybara.com/cookbook/copycapy  
[15]: docs.scrapybara.com/cookbook/wide-research  
[16]: docs.scrapybara.com/cookbook/wide-research  
[17]: docs.scrapybara.com/cookbook/scrapybara-cli  
[19]: docs.scrapybara.com/cookbook/computer-use-playground  
: docs.scrapybara.com/api-reference/notebook/create  
: docs.scrapybara.com/api-reference/notebook/execute  
: docs.scrapybara.com/api-reference/notebook/execute-cell

[1] https://scrapybara.com
[2] https://docs.scrapybara.com/api-reference/start
[3] https://docs.scrapybara.com/quickstart
[4] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_bd9d41a1-4e62-40ae-b957-3bc5634177f6/13372524-9c00-4322-bb10-1f1b92786e98/docs_roocode_com_docs.txt
[5] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_bd9d41a1-4e62-40ae-b957-3bc5634177f6/4b835b0b-f062-488a-b829-878934ccb27a/all_docs.txt
[6] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_bd9d41a1-4e62-40ae-b957-3bc5634177f6/33810352-ac5d-4771-bf5a-baef5faadb11/docs_roocode_com_docs.json
[7] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_bd9d41a1-4e62-40ae-b957-3bc5634177f6/da9e38e2-77f2-4622-8c46-2705f86cfda9/docs_cline_bot_docs.json
[8] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_bd9d41a1-4e62-40ae-b957-3bc5634177f6/6c5802d9-7cf9-4cb8-a6bb-c348765ad478/docs_cline_bot_docs.txt
[9] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_bd9d41a1-4e62-40ae-b957-3bc5634177f6/e6a62052-1125-4413-834e-8f66b00db283/vertex.txt
[10] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_bd9d41a1-4e62-40ae-b957-3bc5634177f6/14dd85fa-fb80-4821-95ba-0d3be9d1d6b4/cloud_google_com_docs.json
[11] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_bd9d41a1-4e62-40ae-b957-3bc5634177f6/3282e7df-05bb-4798-83ab-3e5cb48c77e0/Copy-of-Persistent-Multimodal-AI-Chat-via-API.txt
[12] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_bd9d41a1-4e62-40ae-b957-3bc5634177f6/06adf0c9-de56-489f-ac27-9d4924928fc0/research-multimodel-2.txt
[13] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_bd9d41a1-4e62-40ae-b957-3bc5634177f6/0ac52e87-e29c-4d67-8605-69d1781dcf35/LiveAPIGuide.txt
[14] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_bd9d41a1-4e62-40ae-b957-3bc5634177f6/0f38180e-8d45-469f-a05b-ab8b5fef29d4/My-AI-Studio-research-links.txt
[15] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_bd9d41a1-4e62-40ae-b957-3bc5634177f6/ba4e0e2f-8468-4f26-834f-97680350e0c9/firebase_google_com_docs.json
[16] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_bd9d41a1-4e62-40ae-b957-3bc5634177f6/51f24ccc-56b8-4263-b5ce-b13f066e9d4d/Pasted-RESOURCES-Libraries-Python-SDK-Copy-page-Conversational-AI-SDK-deploy-customized-interac-1744261428405.txt
[17] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_bd9d41a1-4e62-40ae-b957-3bc5634177f6/58994b25-5326-4273-8786-135fb08b8bfb/LiveGuide.txt
[18] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_bd9d41a1-4e62-40ae-b957-3bc5634177f6/7973d38e-e6bd-422c-9d28-049b90d17c80/firebase_google_com_docs.txt
[19] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_bd9d41a1-4e62-40ae-b957-3bc5634177f6/2f69d49d-e605-4ca4-8670-511bddc52ad4/api-info-and-env.txt
[20] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_bd9d41a1-4e62-40ae-b957-3bc5634177f6/416428e8-a59b-473a-8916-5974a0b7ff4f/cloud_google_com_docs.txt
[21] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_bd9d41a1-4e62-40ae-b957-3bc5634177f6/49a8435d-1cc2-42f7-9686-1577c400c485/Vertex-and-gemini-guide.txt
[22] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_bd9d41a1-4e62-40ae-b957-3bc5634177f6/7373f471-e7a0-4718-83b2-6cbf9614ad5a/research-multimodel-1.txt
[23] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_bd9d41a1-4e62-40ae-b957-3bc5634177f6/f884b014-b47b-4f1a-962b-e2ea517935ea/GEMIN-API-SUPER-GUIDE.txt
[24] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_bd9d41a1-4e62-40ae-b957-3bc5634177f6/63a51855-39e3-460e-b245-191a56d404ce/Perplex.txt

**References:**  
[1]: scrapybara.com  
[2]: docs.scrapybara.com  
[4]: github.com/Scrapybara  
[5]: github.com/scrapybara/scrapybara-cookbook  
[6]: github.com/scrapybara/scrapybara-playground

[1] https://scrapybara.com
[2] https://docs.scrapybara.com
[3] https://github.com/jgrevich/scrapybara
[4] https://github.com/Scrapybara
[5] https://github.com/scrapybara/scrapybara-cookbook
[6] https://github.com/scrapybara/scrapybara-playground
[7] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_bd9d41a1-4e62-40ae-b957-3bc5634177f6/3282e7df-05bb-4798-83ab-3e5cb48c77e0/Copy-of-Persistent-Multimodal-AI-Chat-via-API.txt
[8] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_bd9d41a1-4e62-40ae-b957-3bc5634177f6/58994b25-5326-4273-8786-135fb08b8bfb/LiveGuide.txt
[9] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_bd9d41a1-4e62-40ae-b957-3bc5634177f6/51f24ccc-56b8-4263-b5ce-b13f066e9d4d/Pasted-RESOURCES-Libraries-Python-SDK-Copy-page-Conversational-AI-SDK-deploy-customized-interac-1744261428405.txt
[10] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_bd9d41a1-4e62-40ae-b957-3bc5634177f6/7373f471-e7a0-4718-83b2-6cbf9614ad5a/research-multimodel-1.txt
[11] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_bd9d41a1-4e62-40ae-b957-3bc5634177f6/63a51855-39e3-460e-b245-191a56d404ce/Perplex.txt
[12] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_bd9d41a1-4e62-40ae-b957-3bc5634177f6/0ac52e87-e29c-4d67-8605-69d1781dcf35/LiveAPIGuide.txt
[13] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_bd9d41a1-4e62-40ae-b957-3bc5634177f6/f884b014-b47b-4f1a-962b-e2ea517935ea/GEMIN-API-SUPER-GUIDE.txt
[14] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_bd9d41a1-4e62-40ae-b957-3bc5634177f6/06adf0c9-de56-489f-ac27-9d4924928fc0/research-multimodel-2.txt
[15] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_bd9d41a1-4e62-40ae-b957-3bc5634177f6/da9e38e2-77f2-4622-8c46-2705f86cfda9/docs_cline_bot_docs.json
[16] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_bd9d41a1-4e62-40ae-b957-3bc5634177f6/6c5802d9-7cf9-4cb8-a6bb-c348765ad478/docs_cline_bot_docs.txt
[17] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_bd9d41a1-4e62-40ae-b957-3bc5634177f6/33810352-ac5d-4771-bf5a-baef5faadb11/docs_roocode_com_docs.json
[18] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_bd9d41a1-4e62-40ae-b957-3bc5634177f6/4b835b0b-f062-488a-b829-878934ccb27a/all_docs.txt
[19] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_bd9d41a1-4e62-40ae-b957-3bc5634177f6/13372524-9c00-4322-bb10-1f1b92786e98/docs_roocode_com_docs.txt
[20] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_bd9d41a1-4e62-40ae-b957-3bc5634177f6/5909b378-e9df-47a4-9d15-9c6d69ff2a62/camera-calibration-beta-51a46d9d1055.json
[21] https://www.ycombinator.com/companies/scrapybara
[22] https://github.com/Scrapybara/scrapybara-python
[23] https://github.com/justinsunyt
[24] https://gist.github.com/jlia0/db0a9695b3ca7609c9b1a08dcbf872c9
[25] https://www.reddit.com/r/aww/comments/10df5ua/scratching_a_capybara/
[26] https://github.com/scrapybara/scrapybara-demos
[27] https://www.reddit.com/r/OpenAI/comments/1i89lt0/openai_launches_operatoran_agent_that_can_use_a/
[28] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_bd9d41a1-4e62-40ae-b957-3bc5634177f6/49a8435d-1cc2-42f7-9686-1577c400c485/Vertex-and-gemini-guide.txt
[29] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_bd9d41a1-4e62-40ae-b957-3bc5634177f6/5fb0ad98-380e-4519-88f1-b93f7d5455df/GEMINI-API-GUIDE.txt
[30] https://pypi.org/project/scrapybara/
[31] https://www.aibase.com/tool/37497
[32] https://github.com/Scrapybara/scrapybara-mcp
[33] https://www.linkedin.com/posts/fondohq_founderjournal-scrapybara-launches-a-computer-activity-7265089058689736705-NBeh
[34] https://www.linkedin.com/posts/nsemwal_come-join-our-discord-httpslnkdinec5dm2pb-activity-7264700202656182272-d1wN
[35] https://www.linkedin.com/company/scrapybara
[36] https://www.technologyreview.com/2025/01/23/1110484/openai-launches-operator-an-agent-that-can-use-a-computer-for-you/