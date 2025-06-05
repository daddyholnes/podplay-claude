# Welcome to Scrapybara

> Scrapybara hosts remote desktop instances for computer use agents

Introduction


  Setup Scrapybara and deploy your first computer use agent in minutes


## What is Scrapybara?

Scrapybara provides powerful virtual desktop infrastructure for computer use agents with:

* **Lightning speed**: Instantly spin up multiple [Ubuntu](/ubuntu) and [Browser](/browser) instances under 1 second.

* **Flexible deployments**: Easily deploy and manage remote instances with our [API](/api-reference), [SDKs](/sdk-reference), and [dashboard](https://scrapybara.com/dashboard). Configure instance types and timeouts to match your needs.

* **Unified integration**: Seamlessly connect your instances to models like [OpenAI CUA](/openai) and [Claude Computer Use](/anthropic) and execute powerful agentic workflows with [structured outputs](/act-sdk), [multi-turn conversations](/conversations), and [custom tools](/tools).

* **Granular control**: Get complete remote desktop access with all the tools your agents need, including [Browser](/protocols/browser), [Code Execution](/protocols/code), [Environment Variables](/protocols/env), and [Filesystem](/protocols/file).

* **Authenticated sessions**: Save and reuse browser [auth states](/auth-states) across instances.

## Explore our guides


  
    Take action with computer use models and custom tools with one line of code
  

  
    Save and reuse browser authentication states across instances
  


## Get inspired


  } href="/cookbook/copycapy">
    Scrape and transform websites into capybara-themed versions with Scrapybara Act SDK and Playwright.

    


    `TypeScript` `Act SDK` `Playwright`
  

  } href="/cookbook/wide-research">
    Deep Research but wide. Scrape YC W25 companies and find the best way to contact each company in parallel batches.

    


    `Python` `Act SDK` `Structured Outputs`
  


## Dashboard

Get your API key and manage your instances on the [dashboard](https://scrapybara.com/dashboard).

Dashboard

## Get support

Need help or want to stay up to date? Reach out to us on Discord or X.


  
    Join our Discord community
  

  
    Follow us on X
  



# Quickstart

> Deploy your first instance

## Deploy your first instance


  
    
      
        Sign up on our [dashboard](https://scrapybara.com/dashboard). An API key will be generated for you automatically.
      

      
        Install the Python SDK with pip.

        ```bash
        pip install scrapybara
        ```
      

      
        Configure the client with your API key.

        ```python
        from scrapybara import Scrapybara

        client = Scrapybara(api_key="your_api_key")
        ```
      

      
        Start an instance with your desired configuration. You can choose from Ubuntu, Browser, and Windows instances. We recommend using Ubuntu for most tasks.

        ```python
        instance = client.start_ubuntu(
            timeout_hours=1,
        )

        # browser_instance = client.start_browser(
        #     timeout_hours=1,
        # )
        ```
      

      
        Get the stream URL to view and interact with the instance manually.

        ```python
        stream_url = instance.get_stream_url().stream_url
        ```
      

      
        Interact with the instance with `computer` and `bash`.

        ```python Move the mouse
        instance.computer(
            action="move_mouse",
            coordinates=[200, 100]
        )
        ```

        ```python Left click
        instance.computer(
            action="click_mouse",
            button="left"
        )
        ```

        ```python Type hello
        instance.computer(
            action="type_text",
            text="Hello, world!"
        )
        ```

        ```python Run a bash command
        result = instance.bash(
            command="ls -la"
        )
        ```
      

      
        Connect to the browser with Playwright to enable programmatic browser control and authenticated browser sessions. Learn more [here](/browser).

        ```python Connect to Playwright
        from playwright.sync_api import sync_playwright

        cdp_url = instance.browser.start().cdp_url
        playwright = sync_playwright().start()
        browser = playwright.chromium.connect_over_cdp(cdp_url)
        ```

        ```python Save the auth state
        auth_state_id = instance.browser.save_auth(name="default").auth_state_id
        ```

        ```python Reuse the auth state on other instances
        instance.browser.authenticate(auth_state_id=auth_state_id)
        ```
      

      
        Build your first agent with the Act SDK to control your Scrapybara instance with `BashTool`, `ComputerTool`, `EditTool`. Learn more [here](/act-sdk).

        ```python
        from scrapybara.tools import BashTool, ComputerTool, EditTool
        from scrapybara.openai import OpenAI, UBUNTU_SYSTEM_PROMPT

        response = client.act(
            model=OpenAI(),
            tools=[
                BashTool(instance),
                ComputerTool(instance),
                EditTool(instance),
            ],
            system=UBUNTU_SYSTEM_PROMPT,
            prompt="Go to the top link on Hacker News",
            on_step=lambda step: print(step.text),
        )
        ```
      

      
        Stop the instance when you're done. This will delete all data stored during the session.

        ```python
        instance.stop()
        ```
      
    
  

  
    
      
        Sign up on our [dashboard](https://scrapybara.com/dashboard). An API key will be generated for you automatically.
      

      
        Install the TypeScript SDK with npm, yarn, or pnpm.

        ```bash
        npm install scrapybara
        yarn add scrapybara
        pnpm add scrapybara
        ```
      

      
        Configure the client with your API key.

        ```typescript
        import { ScrapybaraClient } from "scrapybara";

        const client = new ScrapybaraClient({ apiKey: "your_api_key" });
        ```
      

      
        Start an instance with your desired configuration. You can choose from Ubuntu, Browser, and Windows instances. We recommend using Ubuntu for most tasks.

        ```typescript
        const instance = await client.startUbuntu({
            timeoutHours: 1,
        });

        // const browserInstance = await client.startBrowser({
        //     timeoutHours: 1,
        // });
        ```
      

      
        Get the stream URL to view and interact with the instance manually.

        ```typescript
        const streamUrl = await instance.getStreamUrl().streamUrl;
        ```
      

      
        Interact with the instance with `computer` and `bash`.

        ```typescript Move the mouse
        await instance.computer({
            action: "move_mouse",
            coordinates: [200, 100]
        });
        ```

        ```typescript Left click
        await instance.computer({
            action: "click_mouse",
            button: "left"
        });
        ```

        ```typescript Type hello
        await instance.computer({
            action: "type_text",
            text: "Hello, world!"
        });
        ```

        ```typescript Run a bash command
        const result = await instance.bash({
            command: "ls -la"
        });
        ```
      

      
        Connect to the browser with Playwright to enable programmatic browser control and authenticated browser sessions. Learn more [here](/browser).

        ```typescript Connect to Playwright
        import { chromium } from "playwright";

        const cdpUrl = await instance.browser.start().cdpUrl;
        const browser = await chromium.connectOverCDP(cdpUrl);
        ```

        ```typescript Save the auth state
        const authStateId = await instance.browser.saveAuth({ name: "default" }).authStateId;
        ```

        ```typescript Reuse the auth state on other instances
        await instance.browser.authenticate({ authStateId });
        ```
      

      
        Build your first agent with the Act SDK to control your Scrapybara instance with `BashTool`, `ComputerTool`, `EditTool`. Learn more [here](/act-sdk).

        ```typescript
        import { bashTool, computerTool, editTool } from "scrapybara/tools";
        import { openai, UBUNTU_SYSTEM_PROMPT } from "scrapybara/openai";

        const { messages, steps, text, usage } = await client.act({
          tools: [
            bashTool(instance),
            computerTool(instance),
            editTool(instance),
          ],
          model: openai(),
          system: UBUNTU_SYSTEM_PROMPT,
          prompt: "Go to the top link on Hacker News",
          onStep: (step) => console.log(step.text),
        });
        ```
      

      
        Stop the instance when you're done. This will delete all data stored during the session.

        ```typescript
        await instance.stop();
        ```
      
    
  


## Start building

Be sure to check out our other resources to learn more. Happy building! ₍ᐢ•(ܫ)•ᐢ₎


  
    Take action with computer use agents
  

  
    Check out our API reference docs
  

  
    Learn about the UbuntuInstance
  

  
    Learn about the BrowserInstance
  



# Best Practices

> Best practices for using Scrapybara

## Manage instance usage

Instances are billed per usage. When launching an instance, you can specify its timeout before it is automatically terminated (default is 1 hour).


  
    ```python
    instance = client.start_ubuntu(timeout=3) # 3 hours
    ```
  

  
    ```typescript
    const instance = await client.startUbuntu({ timeout: 3 }); // 3 hours
    ```
  


To save costs, pause the instance to resume it later, or stop the instance once you no longer need to control the desktop environment and access its stored data.


  
    ```python Pause/resume
    instance.pause()
    instance.resume()
    ```

    ```python Stop
    instance.stop()
    ```
  

  
    ```typescript Pause/resume
    await instance.pause();
    await instance.resume();
    ```

    ```typescript Stop
    await instance.stop();
    ```
  


## Take actions programmatically

When possible, take actions programmatically rather than relying on the agent to do so. For example, using `instance.bash` provides a faster way to launch apps compared to having the model use mouse/keyboard interactions. If you know the agent's workflow will happen on a specific application, you can launch it before prompting the agent to take actions. The same applies for browser automation: it is often easier to manipulate the browser programmatically with `instance.browser` and Playwright than relying on the agent itself.

## Initialize the browser

For agents requiring programmatic browser interaction, initialize and configure the browser immediately after instance creation. This ensures the browser environment is ready before any browser tool calls are made.


  
    ```python
    instance = client.start_ubuntu()
    instance.browser.start()
    instance.browser.authenticate(auth_state_id="auth_state_id")
    ```
  

  
    ```typescript
    const instance = await client.startUbuntu();
    await instance.browser.start();
    await instance.browser.authenticate(auth_state_id="auth_state_id");
    ```
  


## Optimize your prompt

Each model (OpenAI and Anthropic) has its own specialized system prompt optimized for computer use tasks. We recommend using these model-specific prompts for best results.


  
    ```python OpenAI
    from scrapybara.openai import OpenAI, UBUNTU_SYSTEM_PROMPT as OPENAI_UBUNTU_PROMPT

    client.act(
        model=OpenAI(),
        system=OPENAI_UBUNTU_PROMPT,
        # ...
    )
    ```

    ```python Anthropic
    from scrapybara.anthropic import Anthropic, UBUNTU_SYSTEM_PROMPT as ANTHROPIC_UBUNTU_PROMPT

    client.act(
        model=Anthropic(),
        system=ANTHROPIC_UBUNTU_PROMPT,
        # ...
    )
    ```
  

  
    ```typescript OpenAI
    import { openai, UBUNTU_SYSTEM_PROMPT as OPENAI_UBUNTU_PROMPT } from "scrapybara/openai";

    await client.act({
      model: openai(),
      system: OPENAI_UBUNTU_PROMPT,
      // ...
    });
    ```

    ```typescript Anthropic
    import { anthropic, UBUNTU_SYSTEM_PROMPT as ANTHROPIC_UBUNTU_PROMPT } from "scrapybara/anthropic";

    await client.act({
      model: anthropic(),
      system: ANTHROPIC_UBUNTU_PROMPT,
      // ...
    });
    ```
  


For more complex tasks, you can extend the model-specific system prompt by defining additional task requirements:


  
    ```python
    # Use the appropriate system prompt for your chosen model
    system = f"""{UBUNTU_SYSTEM_PROMPT}

    
    {task}
    """
    ```
  

  
    ```typescript
    // Use the appropriate system prompt for your chosen model
    const system = `${UBUNTU_SYSTEM_PROMPT}

    
    ${task}
    `;
    ```
  


Here are some tips from [Anthropic](https://docs.anthropic.com/en/docs/build-with-claude/computer-use) to improve the agent's performance:

1. Specify simple, well-defined tasks and provide explicit instructions for each step.
2. Models sometimes assume outcomes of their actions without explicitly checking their results. To prevent this you can prompt the model with `After each step, take a screenshot and carefully evaluate if you have achieved the right outcome. Explicitly show your thinking: "I have evaluated step X..." If not correct, try again. Only when you confirm a step was executed correctly should you move on to the next one.`
3. Some UI elements (like dropdowns and scrollbars) might be tricky for models to manipulate using mouse movements. If you experience this, try prompting the model to use keyboard shortcuts.
4. For repeatable tasks or UI interactions, include example screenshots and tool calls of successful outcomes in your prompt.
5. If you need the model to log in, provide it with the username and password in your prompt inside xml tags like ``. Using computer use within applications that require login increases the risk of bad outcomes as a result of prompt injection.


# Act SDK

> Build computer use agents with one unified SDK — any model, any tool

## What is the Act SDK?

The Act SDK is a unified SDK for building computer use agents with Python and TypeScript. It provides a simple interface for executing looping agentic actions with support for many models and tools. Build production-ready computer use agents with pre-built tools to connect to Scrapybara instances.

## How it works

`act` initiates an interaction loop that continues until the agent achieves its objective. Each iteration of the loop is called a `step`, which consists of the agent's text response, the agent's tool calls, and the results of those tool calls. The loop terminates when the agent returns a message without invoking any tools, and returns `messages`, `steps`, `text`, `output` (if `schema` is provided), and `usage` after the agent's execution.


  
    ```python
    response = client.act(
        model=OpenAI(),
        tools=[
            BashTool(instance),
            ComputerTool(instance),
            EditTool(instance),
        ],
        system=UBUNTU_SYSTEM_PROMPT,
        prompt="Go to the top link on Hacker News",
        on_step=lambda step: print(step.text),
    )
    messages = response.messages
    steps = response.steps
    text = response.text
    usage = response.usage
    ```
  

  
    ```typescript
    const { messages, steps, text, usage } = await client.act({
      model: openai(),
      tools: [
        bashTool(instance),
        computerTool(instance),
        editTool(instance),
      ],
      system: UBUNTU_SYSTEM_PROMPT,
      prompt: "Go to the top link on Hacker News",
      onStep: (step) => console.log(step.text),
    });
    ```
  


An `act` call consists of 3 core components:

### Model

The model specifies the base LLM for the agent. At each step, the model examines the previous messages, the current state of the computer, and uses tools to take action. Each step will cost an amount of agent credits depending on the model. You can also bring your own API key to bill model charges directly.


  
    ```python
    from scrapybara.openai import OpenAI

    model = OpenAI()

    # Use your own API key
    model = OpenAI(api_key="your_api_key")
    ```
  

  
    ```typescript
    import { openai } from "scrapybara/openai";

    const model = openai();

    // Use your own API key
    const model = openai({ apiKey: "your_api_key" });
    ```
  


### Tools

Tools are functions that enable agents to interact with the computer. Each tool is defined by a `name`, `description`, and how it can be executed with `parameters` and an execution function. A tool can take in a Scrapybara instance to interact with it directly. Learn more about pre-built tools and how to define custom tools [here](/tools).


  
    ```python
    from scrapybara import Scrapybara
    from scrapybara.tools import BashTool, ComputerTool, EditTool

    client = Scrapybara()
    instance = client.start_ubuntu()

    tools = [
        BashTool(instance),
        ComputerTool(instance),
        EditTool(instance),
    ]
    ```
  

  
    ```typescript
    import { ScrapybaraClient } from "scrapybara";
    import { bashTool, computerTool, editTool } from "scrapybara/tools";

    const client = new ScrapybaraClient();
    const instance = await client.startUbuntu();

    const tools = [
      bashTool(instance),
      computerTool(instance),
      editTool(instance),
    ];
    ```
  


### Prompt

The prompt is split into two parts, the `system` prompt and a user `prompt`. `system` defines the general behavior of the agent, such as its capabilities and constraints. You can use our provided `UBUNTU_SYSTEM_PROMPT`, `BROWSER_SYSTEM_PROMPT`, and `WINDOWS_SYSTEM_PROMPT` to get started, or define your own. `prompt` should denote the agent's current objective. Alternatively, you can provide `messages` instead of `prompt` to start the agent with a history of messages. `act` conveniently returns `messages` after the agent's execution, so you can reuse it in another `act` call.


  
    ```python
    from scrapybara.prompts import UBUNTU_SYSTEM_PROMPT

    system = UBUNTU_SYSTEM_PROMPT
    prompt = "Go to the top link on Hacker News"
    ```
  

  
    ```typescript
    import { UBUNTU_SYSTEM_PROMPT } from "scrapybara/prompts";

    const system = UBUNTU_SYSTEM_PROMPT;
    const prompt = "Go to the top link on Hacker News";
    ```
  


## Structured output

Use the `schema` parameter to define a desired structured output. The response's `output` field will contain the typed data returned by the model. This is particularly useful when scraping or collecting structured data from websites.

Under the hood, we pass in a `StructuredOutputTool` to enforce and parse the schema.


  
    ```python
    from pydantic import BaseModel
    from typing import List

    class HNSchema(BaseModel):
        class Post(BaseModel):
            title: str
            url: str 
            points: int
        
        posts: List[Post]

    response = client.act(
        model=OpenAI(),
        tools=[
            ComputerTool(instance),
        ],
        schema=HNSchema,
        system=UBUNTU_SYSTEM_PROMPT,
        prompt="Get the top 10 posts on Hacker News",
    )

    posts = response.output.posts
    ```
  

  
    ```typescript
    import { z } from "zod";

    const { output } = await client.act({
      model: openai(),
      tools: [
        computerTool(instance),
      ],
      schema: z.object({
        posts: z.array(
          z.object({
            title: z.string(),
            url: z.string(),
            points: z.number(),
          })
        ),
      }),
      system: UBUNTU_SYSTEM_PROMPT,
      prompt: "Get the top 10 posts on Hacker News",
    });

    const posts = output?.posts;
    ```
  


## Agent credits

Consume agent credits or bring your own API key. Without an API key, each step consumes 1 [agent credit](https://scrapybara.com/#pricing). With your own API key, model charges are billed directly to your provider API key.

## Full example

Here is how you can build a computer use agent that can output structured data.


  
    ```python
    from scrapybara import Scrapybara
    from scrapybara.openai import OpenAI
    from scrapybara.prompts import UBUNTU_SYSTEM_PROMPT
    from scrapybara.tools import ComputerTool
    from pydantic import BaseModel
    from typing import List

    client = Scrapybara()
    instance = client.start_ubuntu()

    class HNSchema(BaseModel):
        class Post(BaseModel):
            title: str
            url: str 
            points: int
        
        posts: List[Post]

    response = client.act(
        model=OpenAI(),
        tools=[
            ComputerTool(instance),
        ],
        system=UBUNTU_SYSTEM_PROMPT,
        prompt="Get the top 10 posts on Hacker News",
        schema=HNSchema,
        on_step=lambda step: print(step.text),
    )

    posts = response.output.posts
    print(posts)

    instance.stop()
    ```
  

  
    ```typescript
    import { ScrapybaraClient } from "scrapybara";
    import { openai } from "scrapybara/openai";
    import { UBUNTU_SYSTEM_PROMPT } from "scrapybara/prompts";
    import { computerTool } from "scrapybara/tools";
    import { z } from "zod";

    const client = new ScrapybaraClient();
    const instance = await client.startUbuntu();

    const { output } = await client.act({
      model: openai(),
      tools: [
        computerTool(instance),
      ],
      system: UBUNTU_SYSTEM_PROMPT,
      prompt: "Get the top 10 posts on Hacker News",
      schema: z.object({
        posts: z.array(
          z.object({
            title: z.string(),
            url: z.string(),
            points: z.number(),
          })
        ),
      }),
      onStep: (step) => console.log(step.text),
    });

    const posts = output?.posts;
    console.log(posts);

    await instance.browser.stop();
    await instance.stop();
    ```
  



# Auth States

> Save and load browser auth states

## What are auth states?

Auth states in Scrapybara allow you to capture, save, and reuse website authentication data across browser sessions. This feature is extremely useful for:

* Automating login flows
* Persisting authentication between browser instances
* Avoiding repetitive login procedures in your automation scripts
* Testing authenticated features without manual intervention

Auth states capture cookies, local storage, session storage, and other browser-based authentication data.

## Save auth state

When you've successfully authenticated with a website in the browser, you can save the authentication state for future use. Each auth state is identified by a unique ID and an optional name (defaults to "default" if not specified).


  
    ```python
    # First, create a browser instance
    instance = client.start_browser()

    # Open the stream, navigate to the login page, and log in
    webbrowser.open(instance.get_stream_url().stream_url)
    ```

    Once you've logged in, you can save the auth state with a name:

    ```python
    # Now save the auth state with a name
    auth_state_id = instance.save_auth(name="example_site").auth_state_id
    print(f"Saved auth state ID: {auth_state_id}")
    ```
  

  
    ```typescript
    // First, create a browser instance
    const instance = await client.startBrowser();

    // Open the stream, navigate to the login page, and log in
    window.open(instance.getStreamUrl().streamUrl, "_blank");
    ```

    Once you've logged in, you can save the auth state with a name:

    ```typescript
    // Now save the auth state with a name
    const authStateId = await instance.saveAuth({name: "example_site"}).authStateId;
    console.log(`Saved auth state ID: ${authStateId}`);
    ```
  


## Modify auth state

If you have an existing auth state that you want to update with new authentication data, you can use the `modify_auth` functionality. This is useful when credentials have changed or when an existing auth state needs to be refreshed.


  
    ```python
    # First, create a browser instance
    instance = client.start_browser()

    # Open the stream, navigate to the login page, and log in with new credentials
    webbrowser.open(instance.get_stream_url().stream_url)
    ```

    Once you've logged in, you can modify the auth state with a new name:

    ```python
    # Update an existing auth state with the new credentials
    # You can optionally provide a new name
    instance.modify_auth(auth_state_id="your_existing_auth_state_id", name="renamed_auth_state")
    ```
  

  
    ```typescript
    // First, create a browser instance
    const instance = await client.startBrowser();

    // Open the stream, navigate to the login page, and log in with new credentials
    window.open(instance.getStreamUrl().streamUrl, "_blank");
    ```

    Once you've logged in, you can modify the auth state with a new name:

    ```typescript
    // Update an existing auth state with the new credentials
    // You can optionally provide a new name
    await instance.modifyAuth({
      authStateId: "your_existing_auth_state_id", 
      name: "renamed_auth_state"
    });
    ```
  


## Load auth state

Once you've saved an auth state, you can use it to authenticate future browser sessions without going through the login process again:


  
    ```python
    # Create a new browser instance
    instance = client.start_browser()

    # Authenticate using a previously saved auth state
    instance.authenticate(auth_state_id="your_auth_state_id")
    ```
  

  
    ```typescript
    // Create a new browser instance
    const instance = await client.startBrowser();

    // Authenticate using a previously saved auth state
    await instance.authenticate({authStateId: "your_auth_state_id"});
    ```
  


## Using auth states in the playground

The Scrapybara Playground provides a visual interface for managing auth states:

1. **Create an auth state**:
   * Head to the Scrapybara [auth](https://scrapybara.com/auth) page
   * Click on the "Create auth state" button
   * Log in to the website and save the auth state

2. **Use an existing auth state**:
   * Click the fingerprint icon next to the instance dropdown menu
   * Choose your saved auth state from the dropdown
   * When you start the instance, it will automatically apply the authentication data

## Best practices

Here are some best practices for working with auth states:

1. **Use descriptive names**: Name your auth states clearly (e.g., "github\_login" or "shopify\_admin") for easy identification.

2. **Refresh regularly**: Authentication tokens can expire. Consider updating your auth states periodically using the `modify_auth` functionality.

3. **Test before use**: Always verify that your auth state is still valid before relying on it for critical automation.

4. **Multiple auth states**: Maintain separate auth states for different environments (e.g., production, staging, development).


# Conversations

> Build stateful agents with persistent conversations

## Understanding multi-turn conversations

Multi-turn conversations in Scrapybara enable your agents to maintain context and state across multiple interactions.
The Act SDK provides a structured way to manage these conversations through its message architecture.

## Message architecture

The Act SDK uses a structured message system with three primary message types and five different part types. Understanding these components is crucial for building sophisticated multi-turn agents.

### Message types

```python
# Message types
class UserMessage:
    role: str = "user"  # Always "user"
    content: List[Union[TextPart, ImagePart]]  # What the user sends

class AssistantMessage:
    role: str = "assistant"  # Always "assistant"
    content: List[Union[TextPart, ToolCallPart, ReasoningPart]]  # The agent's response
    response_id: Optional[str] = None  # Unique identifier for the response

class ToolMessage:
    role: str = "tool"  # Always "tool"
    content: List[ToolResultPart]  # Results from tool operations

Message = Union[UserMessage, AssistantMessage, ToolMessage]
```

### Message part types

Each message type contains various "parts" that serve different purposes:

```python
# Message part types
class TextPart:
    type: str = "text"  # Always "text"
    text: str  # Plain text content

class ImagePart:
    type: str = "image"  # Always "image"
    image: str  # Base64 encoded image or URL
    mime_type: Optional[str] = None  # e.g., "image/png", "image/jpeg"

class ToolCallPart:
    type: str = "tool-call"  # Always "tool-call"
    id: Optional[str] = None  # Unique identifier for the tool call
    tool_call_id: str  # ID matching the tool result
    tool_name: str  # Name of the tool being called
    args: dict[str, Any]  # Arguments passed to the tool

class ToolResultPart:
    type: str = "tool-result"  # Always "tool-result"
    tool_call_id: str  # ID matching the original tool call
    tool_name: str  # Name of the tool that was called
    result: Any  # Result returned by the tool
    is_error: Optional[bool] = False  # Whether the tool execution resulted in an error

class ReasoningPart:
    type: str = "reasoning"  # Always "reasoning"
    id: Optional[str] = None  # Unique identifier for the reasoning part
    reasoning: str  # The agent's internal reasoning
    signature: Optional[str] = None  # Cryptographic signature for verification
    instructions: Optional[str] = None  # Additional context about the reasoning
```

## Building multi-turn conversations

Instead of providing a single `prompt`, you can pass a complete message history using the `messages` parameter. This allows you to maintain the full conversation context.
The Act SDK returns a `messages` field in the response that contains the complete conversation history. You can reuse this directly in your next `act` call.


  
    ```python
    from scrapybara import Scrapybara
    from scrapybara.anthropic import Anthropic
    from scrapybara.prompts import UBUNTU_SYSTEM_PROMPT
    from scrapybara.tools import BashTool, ComputerTool, EditTool

    client = Scrapybara()
    instance = client.start_ubuntu()

    # Initial conversation
    response = client.act(
        model=Anthropic(),
        tools=[
            BashTool(instance),
            ComputerTool(instance),
            EditTool(instance),
        ],
        on_step=lambda step: print(step.text),
        system=UBUNTU_SYSTEM_PROMPT,
        prompt="Create a file called hello.py that prints 'Hello, World!'",
    )

    print('--------------------------------')

    # Continue the conversation with the previous messages
    follow_up_response = client.act(
        model=Anthropic(),
        tools=[
            BashTool(instance),
            ComputerTool(instance),
            EditTool(instance),
        ],
        on_step=lambda step: print(step.text),
        system=UBUNTU_SYSTEM_PROMPT,
        messages=response.messages + [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Now modify the file to accept a name as a command line argument and print 'Hello, {name}!'"
                    }
                ]
            }
        ]
    )

    instance.stop()
    ```
  

  
    ```typescript
    import { ScrapybaraClient } from "scrapybara";
    import { anthropic } from "scrapybara/anthropic";
    import { UBUNTU_SYSTEM_PROMPT } from "scrapybara/prompts";
    import { bashTool, computerTool, editTool } from "scrapybara/tools";

    const client = new ScrapybaraClient();
    const instance = await client.startUbuntu();

    // Initial conversation
    const response = await client.act({
      model: anthropic(),
      tools: [
        bashTool(instance),
        computerTool(instance),
        editTool(instance),
      ],
      onStep: (step) => console.log(step.text),
      system: UBUNTU_SYSTEM_PROMPT,
      prompt: "Create a file called hello.py that prints 'Hello, World!'",
    });

    console.log('--------------------------------')

    // Continue the conversation with the previous messages
    const followUpResponse = await client.act({
      model: anthropic(),
      tools: [
        bashTool(instance),
        computerTool(instance),
        editTool(instance),
      ],
      onStep: (step) => console.log(step.text),
      system: UBUNTU_SYSTEM_PROMPT,
      messages: [
        ...response.messages,
        {
          role: "user",
          content: [
            {
              type: "text",
              text: "Now modify the file to accept a name as a command line argument and print 'Hello, {name}!'"
            }
          ]
        }
      ]
    });

    await instance.stop();
    ```
  


## Including screenshots in messages

Screenshots are a powerful way to provide visual context to your agent. You can include them in user messages using the `ImagePart` type.


  
    ```python
    from scrapybara import Scrapybara
    from scrapybara.anthropic import Anthropic
    from scrapybara.prompts import UBUNTU_SYSTEM_PROMPT

    client = Scrapybara()
    instance = client.start_ubuntu()

    # Take a screenshot
    screenshot = instance.screenshot().base_64_image

    # Send the screenshot to the agent
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "What do you see in this screenshot? Describe the desktop environment."
                },
                {
                    "type": "image",
                    "image": 'data:image/png;base64,' + screenshot,
                    "mime_type": "image/png"
                }
            ]
        }
    ]

    response = client.act(
        model=Anthropic(),
        system=UBUNTU_SYSTEM_PROMPT,
        messages=messages,
    )

    print(response.text)
    instance.stop()
    ```
  

  
    ```typescript
    import { ScrapybaraClient } from "scrapybara";
    import { anthropic } from "scrapybara/anthropic";
    import { UBUNTU_SYSTEM_PROMPT } from "scrapybara/prompts";

    const client = new ScrapybaraClient();
    const instance = await client.startUbuntu();

    // Take a screenshot
    const screenshotResult = await instance.screenshot();
    const screenshot = screenshotResult.base64Image;

    // Send the screenshot to the agent
    const messages = [
      {
        role: "user",
        content: [
          {
            type: "text",
            text: "What do you see in this screenshot? Describe the desktop environment."
          },
          {
            type: "image",
            image: 'data:image/png;base64,' + screenshot,
            mime_type: "image/png"
          }
        ]
      }
    ];

    const response = await client.act({
      model: anthropic(),
      system: UBUNTU_SYSTEM_PROMPT,
      messages: messages,
    });

    console.log(response.text);
    await instance.stop();
    ```
  


## Working with tools and reasoning

The Act SDK captures both tool calls and agent reasoning in its message architecture. Here's how you can access and work with this information:

### Examining tool calls and results


  
    ```python
    from scrapybara import Scrapybara
    from scrapybara.anthropic import Anthropic
    from scrapybara.prompts import UBUNTU_SYSTEM_PROMPT
    from scrapybara.tools import BashTool

    client = Scrapybara()
    instance = client.start_ubuntu()

    response = client.act(
        model=Anthropic(),
        tools=[BashTool(instance)],
        system=UBUNTU_SYSTEM_PROMPT,
        prompt="Show me the current directory structure",
    )

    # Analyze the conversation steps
    for message in response.messages:
        if message.role == "assistant":
            for part in message.content:
                if part.type == "tool-call":
                    print(f"Tool called: {part.tool_name}")
                    print(f"Arguments: {part.args}")
        elif message.role == "tool":
            for part in message.content:
                print(f"Tool result from {part.tool_name}: {part.result}")

    instance.stop()
    ```
  

  
    ```typescript
    import { ScrapybaraClient } from "scrapybara";
    import { anthropic } from "scrapybara/anthropic";
    import { UBUNTU_SYSTEM_PROMPT } from "scrapybara/prompts";
    import { bashTool } from "scrapybara/tools";

    const client = new ScrapybaraClient();
    const instance = await client.startUbuntu();

    const response = await client.act({
      model: anthropic(),
      tools: [bashTool(instance)],
      system: UBUNTU_SYSTEM_PROMPT,
      prompt: "Show me the current directory structure",
    });

    // Analyze the conversation steps
    for (const message of response.messages) {
      if (message.role === "assistant") {
        for (const part of message.content) {
          if (part.type === "tool-call") {
            console.log(`Tool called: ${part.tool_name}`);
            console.log(`Arguments: ${JSON.stringify(part.args)}`);
          }
        }
      } else if (message.role === "tool") {
        for (const part of message.content) {
          console.log(`Tool result from ${part.tool_name}: ${JSON.stringify(part.result)}`);
        }
      }
    }

    await instance.stop();
    ```
  


### Accessing agent reasoning


  
    ```python
    from scrapybara import Scrapybara
    from scrapybara.anthropic import Anthropic
    from scrapybara.prompts import UBUNTU_SYSTEM_PROMPT
    from scrapybara.tools import BashTool, ComputerTool

    client = Scrapybara()
    instance = client.start_ubuntu()

    response = client.act(
        model=Anthropic(name="claude-3-7-sonnet-20250219-thinking"),
        tools=[
            BashTool(instance),
            ComputerTool(instance),
        ],
        system=UBUNTU_SYSTEM_PROMPT,
        prompt="Open Firefox and navigate to scrapybara.com",
    )

    # Extract reasoning parts from assistant messages
    for message in response.messages:
        if message.role == "assistant":
            for part in message.content:
                if part.type == "reasoning":
                    print("Agent reasoning:")
                    print(part.reasoning)

    # Or access reasoning directly from steps
    for step in response.steps:
        if step.reasoning_parts:
            print(f"Step reasoning: {step.reasoning_parts}")

    instance.stop()
    ```
  

  
    ```typescript
    import { ScrapybaraClient } from "scrapybara";
    import { anthropic } from "scrapybara/anthropic";
    import { UBUNTU_SYSTEM_PROMPT } from "scrapybara/prompts";
    import { bashTool, computerTool } from "scrapybara/tools";

    const client = new ScrapybaraClient();
    const instance = await client.startUbuntu();

    const response = await client.act({
      model: anthropic({ name: "claude-3-7-sonnet-20250219-thinking" }),
      tools: [
        bashTool(instance),
        computerTool(instance),
      ],
      system: UBUNTU_SYSTEM_PROMPT,
      prompt: "Open Firefox and navigate to scrapybara.com",
    });

    // Extract reasoning parts from assistant messages
    for (const message of response.messages) {
      if (message.role === "assistant") {
        for (const part of message.content) {
          if (part.type === "reasoning") {
            console.log("Agent reasoning:");
            console.log(part.reasoning);
          }
        }
      }
    }

    // Or access reasoning directly from steps
    for (const step of response.steps) {
      if (step.reasoning_parts) {
        console.log(`Step reasoning: ${step.reasoning_parts}`);
      }
    }

    await instance.stop();
    ```
  


## Best practices for multi-turn conversations

1. **Maintain message history**: Always use the returned `messages` from each call to maintain conversation context.

2. **Clear instructions**: Provide clear, specific instructions in each new user message.

3. **Handle context length**: For very long conversations, consider summarizing or truncating older messages to avoid exceeding model context limits.

4. **Include visual context**: Use screenshots when appropriate to provide additional context to the agent.

5. **Monitor token usage**: Track token usage through the `usage` field to prevent exceeding quotas or limits.

6. **Process message parts**: Parse and handle different message parts appropriately based on their type.

## Simple multi-turn example

Here's an interactive Read-Eval-Print Loop (REPL) implementation that allows you to have ongoing conversations with your agent:


  
    ```python
    from scrapybara import Scrapybara
    from scrapybara.anthropic import Anthropic
    from scrapybara.prompts import UBUNTU_SYSTEM_PROMPT
    from scrapybara.tools import BashTool, ComputerTool, EditTool

    def agent_repl():
        client = Scrapybara()
        instance = client.start_ubuntu()
        tools = [BashTool(instance), ComputerTool(instance), EditTool(instance)]
        messages = []

        print("Scrapybara REPL started. Type 'exit' to quit")

        try:
            while True:
                # Get user input
                user_input = input("\n> ")

                # Exit command
                if user_input.lower() == 'exit':
                    break

                # Regular text command
                messages.append({
                    "role": "user",
                    "content": [{"type": "text", "text": user_input}]
                })

                # Process with agent
                print("Processing...")
                response = client.act(
                    model=Anthropic(),
                    tools=tools,
                    system=UBUNTU_SYSTEM_PROMPT,
                    on_step=lambda step: print(step.text),
                    messages=messages
                )

                # Update conversation history
                messages = response.messages
        finally:
            instance.stop()
            print("Session ended.")

    if __name__ == "__main__":
        agent_repl()
    ```
  

  
    ```typescript
    import * as readline from 'readline';
    import { ScrapybaraClient } from "scrapybara";
    import { anthropic } from "scrapybara/anthropic";
    import { UBUNTU_SYSTEM_PROMPT } from "scrapybara/prompts";
    import { bashTool, computerTool, editTool } from "scrapybara/tools";

    async function agent_repl() {
      const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
      });
      const client = new ScrapybaraClient();
      const instance = await client.startUbuntu();
      const tools = [bashTool(instance), computerTool(instance), editTool(instance)];
      let messages: any[] = [];

      console.log("Scrapybara REPL started. Type 'exit' to quit");

      const getInput = (): Promise => new Promise(resolve => rl.question("\n> ", resolve));

      try {
        while (true) {
          // Get user input
          const userInput = await getInput();

          // Exit command
          if (userInput.toLowerCase() === 'exit') {
            break;
          }

          // Regular text command
          messages.push({
            role: "user",
            content: [{type: "text", text: userInput}]
          });

          // Process with agent
          console.log("Processing...");
          const response = await client.act({
            model: anthropic(),
            tools: tools,
            system: UBUNTU_SYSTEM_PROMPT,
            onStep: (step) => console.log(step.text),
            messages: messages
          });

          // Update conversation history
          messages = response.messages;
        }
      } finally {
        await instance.stop();
        rl.close();
        console.log("Session ended.");
      }
    }

    agent_repl().catch(console.error);
    ```
  



# Tools

> Pre-built Scrapybara tools and how to define custom tools

## Scrapybara tools

### BashTool, ComputerTool, EditTool

`BashTool`, `ComputerTool`, and `EditTool` follow the same interface as the instance `bash`, `computer`, and `edit` methods. They each take in an `instance` parameter to interact with the instance.

* `ComputerTool` allows the agent to allows the agent to control mouse and keyboard. Supported for Ubuntu, Browser, and Windows instances.
* `BashTool` allows the agent to run bash commands. Supported only for Ubuntu instances.
* `EditTool` allows the agent to view, create, and edit files. Supported only for Ubuntu instances.


  
    ```python
    from scrapybara import Scrapybara
    from scrapybara.tools import BashTool, ComputerTool, EditTool

    client = Scrapybara()
    instance = client.start_ubuntu()

    tools = [
      BashTool(instance),
      ComputerTool(instance),
      EditTool(instance),
    ]
    ```
  

  
    ```typescript
    import { ScrapybaraClient } from "scrapybara";
    import { bashTool, computerTool, editTool } from "scrapybara/tools";

    const client = new ScrapybaraClient();
    const instance = await client.startUbuntu();

    const tools = [
      bashTool(instance),
      computerTool(instance),
      editTool(instance),
    ];
    ```
  


## Define custom tools

You can define custom tools. A tool needs a `name`, `description`, `parameters` (Pydantic model for Python, Zod object for TS), and an execute function (`__call__` for Python, `execute` for TS).


  
    ```python
    from scrapybara.client import UbuntuInstance
    from scrapybara.tools import Tool
    from pydantic import BaseModel

    class CapyParameters(BaseModel):
        # Define your parameters here
        pass

    class CapyTool(Tool):
        _instance: UbuntuInstance

        def __init__(self, instance: UbuntuInstance) -> None:
            super().__init__(
                name="capy",
                description="Use a capybara",
                parameters=CapyParameters,
            )
            self._instance = instance

        def __call__(self, **kwargs: Any) -> Any:
            # Implement your tool logic here
            pass
    ```
  

  
    ```typescript
    import { UbuntuInstance } from "scrapybara";
    import { tool } from "scrapybara/tools";
    import { z } from "zod";

    export function capyTool(instance: UbuntuInstance) {
        return tool({
            name: "capy",
            description: "Use a capybara",
            parameters: z.object({}), // Define your parameters here
            execute: async () => {
                // Implement your tool logic here
            },
        });
    }
    ```
  


### BrowserTool

`BrowserTool` allows the agent to interact with a browser using Playwright.


  Custom tools like BrowserTool may degrade model performance, as the models have not been trained on custom tools. For browser automation, we recommend sticking to ComputerTool.



  The BrowserTool requires the browser to be started first.



  
    ```python
    from playwright.sync_api import sync_playwright

    class BrowserToolParameters(BaseModel):
    """Parameters for browser interaction commands."""

    command: Literal[
        "go_to",  # Navigate to a URL
        "get_html",  # Get current page HTML
        "evaluate",  # Run JavaScript code
        "click",  # Click on an element
        "type",  # Type into an element
        "screenshot",  # Take a screenshot
        "get_text",  # Get text content of element
        "get_attribute",  # Get attribute of element
    ] = Field(
        description="The browser command to execute. Required parameters per command:\n"
        "- go_to: requires 'url'\n"
        "- evaluate: requires 'code'\n"
        "- click: requires 'selector'\n"
        "- type: requires 'selector' and 'text'\n"
        "- get_text: requires 'selector'\n"
        "- get_attribute: requires 'selector' and 'attribute'\n"
        "- get_html: no additional parameters\n"
        "- screenshot: no additional parameters"
    )
    url: Optional[str] = Field(
        None, description="URL for go_to command (required for go_to)"
    )
    selector: Optional[str] = Field(
        None,
        description="CSS selector for element operations (required for click, type, get_text, get_attribute)",
    )
    code: Optional[str] = Field(
        None, description="JavaScript code for evaluate command (required for evaluate)"
    )
    text: Optional[str] = Field(
        None, description="Text to type for type command (required for type)"
    )
    timeout: Optional[int] = Field(
        30000, description="Timeout in milliseconds for operations"
    )
    attribute: Optional[str] = Field(
        None,
        description="Attribute name for get_attribute command (required for get_attribute)",
    )


    class BrowserTool(Tool):
    """A browser interaction tool that allows the agent to interact with a browser."""

    _instance: Union[UbuntuInstance, BrowserInstance]

    def __init__(self, instance: Union[UbuntuInstance, BrowserInstance]) -> None:
        super().__init__(
            name="browser",
            description="Interact with a browser for web scraping and automation",
            parameters=BrowserToolParameters,
        )
        self._instance = instance

    def __call__(self, **kwargs: Any) -> Any:
        params = BrowserToolParameters.model_validate(kwargs)
        command = params.command
        url = params.url
        selector = params.selector
        code = params.code
        text = params.text
        timeout = params.timeout or 30000
        attribute = params.attribute

        cdp_url = self._instance.browser.get_cdp_url().cdp_url
        if cdp_url is None:
            raise ValueError("CDP URL is not available, start the browser first")

        with sync_playwright() as playwright:
            browser = playwright.chromium.connect_over_cdp(cdp_url)
            context = browser.contexts[0]
            if not context.pages:
                page = context.new_page()
            else:
                page = context.pages[0]

            try:
                if command == "go_to":
                    if not url:
                        raise ValueError("URL is required for go_to command")
                    page.goto(url, timeout=timeout)
                    return True

                elif command == "get_html":
                    try:
                        return page.evaluate("() => document.documentElement.outerHTML")
                    except Exception:
                        # If page is navigating, just return what we can get
                        return page.evaluate("() => document.documentElement.innerHTML")

                elif command == "evaluate":
                    if not code:
                        raise ValueError("Code is required for evaluate command")
                    return page.evaluate(code)

                elif command == "click":
                    if not selector:
                        raise ValueError("Selector is required for click command")
                    page.click(selector, timeout=timeout)
                    return True

                elif command == "type":
                    if not selector:
                        raise ValueError("Selector is required for type command")
                    if not text:
                        raise ValueError("Text is required for type command")
                    page.type(selector, text, timeout=timeout)
                    return True

                elif command == "screenshot":
                    return image_result(
                        base64.b64encode(page.screenshot(type="png")).decode("utf-8")
                    )

                elif command == "get_text":
                    if not selector:
                        raise ValueError("Selector is required for get_text command")
                    element = page.wait_for_selector(selector, timeout=timeout)
                    if element is None:
                        raise ValueError(f"Element not found: {selector}")
                    return element.text_content()

                elif command == "get_attribute":
                    if not selector:
                        raise ValueError(
                            "Selector is required for get_attribute command"
                        )
                    if not attribute:
                        raise ValueError(
                            "Attribute is required for get_attribute command"
                        )
                    element = page.wait_for_selector(selector, timeout=timeout)
                    if element is None:
                        raise ValueError(f"Element not found: {selector}")
                    return element.get_attribute(attribute)

                else:
                    raise ValueError(f"Unknown command: {command}")

            except Exception as e:
                raise ValueError(f"Browser command failed: {str(e)}")

            finally:
                browser.close()
    ```
  

  
    ```typescript
    import { chromium } from "playwright";

    export function browserTool(instance: UbuntuInstance | BrowserInstance) {
        return tool({
            name: "browser",
            description: "Interact with a browser for web scraping and automation",
            parameters: z.object({
                command: z
                    .enum(["go_to", "get_html", "evaluate", "click", "type", "screenshot", "get_text", "get_attribute"])
                    .describe(
                        "The browser command to execute. Required parameters per command:\n- go_to: requires 'url'\n- evaluate: requires 'code'\n- click: requires 'selector'\n- type: requires 'selector' and 'text'\n- get_text: requires 'selector'\n- get_attribute: requires 'selector' and 'attribute'\n- get_html: no additional parameters\n- screenshot: no additional parameters"
                    ),
                url: z.string().optional().describe("URL for go_to command (required for go_to)"),
                selector: z
                    .string()
                    .optional()
                    .describe("CSS selector for element operations (required for click, type, get_text, get_attribute)"),
                code: z.string().optional().describe("JavaScript code for evaluate command (required for evaluate)"),
                text: z.string().optional().describe("Text to type for type command (required for type)"),
                timeout: z.number().optional().default(30000).describe("Timeout in milliseconds for operations"),
                attribute: z
                    .string()
                    .optional()
                    .describe("Attribute name for get_attribute command (required for get_attribute)"),
            }),
            execute: async (params) => {
                const { command, url, selector, code, text, timeout = 30000, attribute } = params;

                const cdpUrl = await instance.browser.getCdpUrl();
                if (!cdpUrl.cdpUrl) {
                    throw new Error("CDP URL is not available, start the browser first");
                }

                const browser = await chromium.connectOverCDP(cdpUrl.cdpUrl);
                try {
                    const context = browser.contexts()[0];
                    const page = context.pages().length ? context.pages()[0] : await context.newPage();

                    try {
                        switch (command) {
                            case "go_to":
                                if (!url) throw new Error("URL is required for go_to command");
                                await page.goto(url, { timeout });
                                return true;

                            case "get_html":
                                try {
                                    return await page.evaluate("document.documentElement.outerHTML");
                                } catch {
                                    // If page is navigating, just return what we can get
                                    return await page.evaluate("document.documentElement.innerHTML");
                                }

                            case "evaluate":
                                if (!code) throw new Error("Code is required for evaluate command");
                                return await page.evaluate(code);

                            case "click":
                                if (!selector) throw new Error("Selector is required for click command");
                                await page.click(selector, { timeout });
                                return true;

                            case "type":
                                if (!selector) throw new Error("Selector is required for type command");
                                if (!text) throw new Error("Text is required for type command");
                                await page.type(selector, text, { timeout });
                                return true;

                            case "screenshot":
                                const screenshot = await page.screenshot({ type: "png" });
                                return imageResult(screenshot.toString("base64"));

                            case "get_text":
                                if (!selector) throw new Error("Selector is required for get_text command");
                                const textElement = await page.waitForSelector(selector, { timeout });
                                if (!textElement) throw new Error(`Element not found: ${selector}`);
                                return await textElement.textContent();

                            case "get_attribute":
                                if (!selector) throw new Error("Selector is required for get_attribute command");
                                if (!attribute) throw new Error("Attribute is required for get_attribute command");
                                const element = await page.waitForSelector(selector, { timeout });
                                if (!element) throw new Error(`Element not found: ${selector}`);
                                return await element.getAttribute(attribute);

                            default:
                                throw new Error(`Unknown command: ${command}`);
                        }
                    } catch (error: any) {
                        throw new Error(`Browser command failed: ${error?.message || String(error)}`);
                    }
                } finally {
                    await browser.close();
                }
            },
        });
    }
    ```
  



# OpenAI

> Build Scrapybara agents with OpenAI models

## Act SDK

Use OpenAI models with the Act SDK:

* Default: `computer-use-preview` (computer use beta)

Consume agent credits or bring your own API key. Without an API key, each step consumes 1 [agent credit](https://scrapybara.com/#pricing). With your own API key, model charges are billed directly to your OpenAI account.


  
    ```python Import model
    from scrapybara.openai import OpenAI, UBUNTU_SYSTEM_PROMPT

    # Consume agent credits
    model = OpenAI()

    # Bring your own API key
    model = OpenAI(api_key="your_api_key")
    ```

    ```python Take action
    from scrapybara import Scrapybara
    from scrapybara.tools import BashTool, ComputerTool, EditTool 

    client = Scrapybara()
    instance = client.start_ubuntu()

    client.act(
        tools=[
            BashTool(instance),
            ComputerTool(instance),
            EditTool(instance),
        ],
        model=model,
        system=UBUNTU_SYSTEM_PROMPT,
        prompt="Research Scrapybara",
    )
    ```
  

  
    ```typescript Import model
    import { openai, UBUNTU_SYSTEM_PROMPT } from "scrapybara/openai";

    // Consume agent credits
    const model = () => openai();

    // Bring your own API key
    const model = () => openai({ apiKey: "your_api_key" });
    ```

    ```typescript Take action
    import { ScrapybaraClient } from "scrapybara";
    import { bashTool, computerTool, editTool } from "scrapybara/tools";

    const client = new ScrapybaraClient();
    const instance = await client.startUbuntu();

    await client.act({
      tools: [
        bashTool(instance),
        computerTool(instance),
        editTool(instance),
      ],
      model,
      system: UBUNTU_SYSTEM_PROMPT,
      prompt: "Research Scrapybara",
    })
    ```
  



# Anthropic

> Build Scrapybara agents with Anthropic models

## Act SDK

Use Anthropic models with the Act SDK:

* Default: `claude-3-7-sonnet-20250219` (computer use beta)
* `claude-3-7-sonnet-20250219-thinking` (computer use beta and extended thinking)
* `claude-3-5-sonnet-20241022` (computer use beta)
* `claude-sonnet-4-20250514` (computer use beta)
* `claude-sonnet-4-20250514-thinking` (computer use beta and extended thinking)

Consume agent credits or bring your own API key. Without an API key, each step consumes 1 [agent credit](https://scrapybara.com/#pricing). With your own API key, model charges are billed directly to your Anthropic account.


  
    ```python Import model
    from scrapybara.anthropic import Anthropic, UBUNTU_SYSTEM_PROMPT

    # Consume agent credits
    model = Anthropic()

    # Bring your own API key
    model = Anthropic(api_key="your_api_key")

    # Use extended thinking
    model = Anthropic(name="claude-3-7-sonnet-20250219-thinking")

    # Use Claude Sonnet 4 with extended thinking
    model = Anthropic(name="claude-sonnet-4-20250514-thinking")
    ```

    ```python Take action
    from scrapybara import Scrapybara
    from scrapybara.tools import BashTool, ComputerTool, EditTool

    client = Scrapybara()
    instance = client.start_ubuntu()

    client.act(
        tools=[
            BashTool(instance),
            ComputerTool(instance),
            EditTool(instance),
        ],
        model=model,
        system=UBUNTU_SYSTEM_PROMPT,
        prompt="Research Scrapybara",
    )
    ```
  

  
    ```typescript Import model
    import { anthropic, UBUNTU_SYSTEM_PROMPT } from "scrapybara/anthropic";

    // Consume agent credits
    const model = () => anthropic();

    // Bring your own API key
    const model = () => anthropic({ apiKey: "your_api_key" });
    ```

    ```typescript Take action
    import { ScrapybaraClient } from "scrapybara";
    import { bashTool, computerTool, editTool } from "scrapybara/tools";

    const client = new ScrapybaraClient();
    const instance = await client.startUbuntu();

    await client.act({
      tools: [
        bashTool(instance),
        computerTool(instance),
        editTool(instance),
      ],
      model,
      system: UBUNTU_SYSTEM_PROMPT,
      prompt: "Research Scrapybara",
    })
    ```
  



# Ubuntu

> Deploy an Ubuntu instance

## UbuntuInstance

The `UbuntuInstance` is a Ubuntu 22.04 desktop that supports interactive streaming, computer actions, bash commands, filesystem management, built-in Jupyter notebooks, and Chromium browser support. We recommend using this instance type for most tasks.

* Fast start up time
* 1x compute cost

## Start an Ubuntu instance


  
    `python instance = client.start_ubuntu() `
  

  
    `typescript const instance = await client.startUbuntu(); `
  


## Available actions

### screenshot

Take a base64 encoded image of the current desktop


  
    `python base_64_image = instance.screenshot().base_64_image `
  

  
    `typescript const base64Image = await instance.screenshot(); `
  


### get\_stream\_url

Get the interactive stream URL


  
    `python stream_url = instance.get_stream_url().stream_url `
  

  
    `typescript const streamUrl = await instance.getStreamUrl(); `
  


### computer

Perform computer actions with the mouse and keyboard

#### `move_mouse`

Move mouse cursor to specific coordinates


  \[x, y] coordinates to move to



  List of modifier keys to hold during the action



  Whether to take a screenshot after the action



  
    ```python Move mouse
    instance.computer(action="move_mouse", coordinates=[100, 200])
    ```

    ```python Move mouse while holding shift
    instance.computer(action="move_mouse", coordinates=[100, 200], hold_keys=["shift"])
    ```

    ```python Move mouse without taking a screenshot
    instance.computer(action="move_mouse", coordinates=[100, 200], screenshot=False)
    ```
  

  
    ```typescript Move mouse
    await instance.computer({action: "move_mouse", coordinates: [100, 200]});
    ```

    ```typescript Move mouse while holding shift
    await instance.computer({action: "move_mouse", coordinates: [100, 200], holdKeys: ["shift"]});
    ```

    ```typescript Move mouse without taking a screenshot
    await instance.computer({action: "move_mouse", coordinates: [100, 200], screenshot: false});
    ```
  


#### `click_mouse`

Perform a mouse click at current position or specified coordinates


  Mouse button to click ("left", "right", "middle", "back", "forward")



  Type of click action ("down", "up", "click")



  \[x, y] coordinates to click at



  Number of clicks



  List of modifier keys to hold during the action



  Whether to take a screenshot after the action



  
    ```python Left click at current position
    instance.computer(action="click_mouse", button="left")
    ```

    ```python Right click at coordinates
    instance.computer(action="click_mouse", button="right", coordinates=[300, 400])
    ```

    ```python Mouse down
    instance.computer(action="click_mouse", button="left", click_type="down")
    ```

    ```python Double click at coordinates
    instance.computer(action="click_mouse", button="left", num_clicks=2, coordinates=[500, 300])
    ```
  

  
    ```typescript Left click at current position
    await instance.computer({action: "click_mouse", button: "left"});
    ```

    ```typescript Right click at coordinates
    await instance.computer({action: "click_mouse", button: "right", coordinates: [300, 400]});
    ```

    ```typescript Mouse down
    await instance.computer({action: "click_mouse", button: "left", clickType: "down"});
    ```

    ```typescript Double click at coordinates
    await instance.computer({action: "click_mouse", button: "left", numClicks: 2, coordinates: [500, 300]});
    ```
  


#### `drag_mouse`

Click and drag from current position to specified coordinates


  List of \[x, y] coordinate pairs defining the drag path



  List of modifier keys to hold during the action



  Whether to take a screenshot after the action



  
    ```python Drag to coordinates
    instance.computer(action="drag_mouse", path=[[100, 200], [300, 400]])
    ```
  

  
    ```typescript Drag to coordinates
    await instance.computer({action: "drag_mouse", path: [[100, 200], [300, 400]]});
    ```
  


#### `scroll`

Scroll horizontally and/or vertically


  \[x, y] coordinates to scroll at



  Horizontal scroll amount



  Vertical scroll amount



  List of modifier keys to hold during the action



  Whether to take a screenshot after the action



  
    ```python Scroll down
    instance.computer(action="scroll", coordinates=[100, 100], delta_x=0, delta_y=200)
    ```

    ```python Scroll right
    instance.computer(action="scroll", coordinates=[100, 100], delta_x=200, delta_y=0)
    ```
  

  
    ```typescript Scroll down
    await instance.computer({action: "scroll", coordinates: [100, 100], deltaX: 0, deltaY: 200});
    ```

    ```typescript Scroll right
    await instance.computer({action: "scroll", coordinates: [100, 100], deltaX: 100, deltaY: 0});
    ```
  


#### `press_key`

Press a key or combination of keys. Scrapybara supports keys defined by [X keysyms](https://github.com/D-Programming-Deimos/libX11/blob/master/c/X11/keysymdef.h). Common aliases are also supported:

* `alt` → `Alt_L`
* `ctrl`, `control` → `Control_L`
* `meta` → `Meta_L`
* `super` → `Super_L`
* `shift` → `Shift_L`


  List of keys to press



  Time to hold keys in seconds



  Whether to take a screenshot after the action



  
    ```python Press ctrl+c
    instance.computer(action="press_key", keys=["ctrl", "c"])
    ```

    ```python Hold shift for 2 seconds
    instance.computer(action="press_key", keys=["shift"], duration=2)
    ```

    ```python Press enter/return
    instance.computer(action="press_key", keys=["Return"])
    ```
  

  
    ```typescript Press ctrl+c
    await instance.computer({action: "press_key", keys: ["ctrl", "c"]});
    ```

    ```typescript Hold shift for 2 seconds
    await instance.computer({action: "press_key", keys: ["shift"], duration: 2});
    ```

    ```typescript Press enter/return
    await instance.computer({action: "press_key", keys: ["Return"]});
    ```
  


#### `type_text`

Type text into the active window


  Text to type



  List of modifier keys to hold while typing



  Whether to take a screenshot after the action



  
    ```python Type text
    instance.computer(action="type_text", text="Hello world")
    ```

    ```python Type text without taking a screenshot
    instance.computer(action="type_text", text="Hello world", screenshot=False)
    ```
  

  
    ```typescript Type text
    await instance.computer({action: "type_text", text: "Hello world"});
    ```

    ```typescript Type text without taking a screenshot
    await instance.computer({action: "type_text", text: "Hello world", screenshot: false});
    ```
  


#### `wait`

Wait for a specified duration


  Time to wait in seconds



  Whether to take a screenshot after the action



  
    ```python Wait for 3 seconds
    instance.computer(action="wait", duration=3)
    ```
  

  
    ```typescript Wait for 3 seconds
    await instance.computer({action: "wait", duration: 3});
    ```
  


#### `take_screenshot`

Take a screenshot of the desktop


  
    ```python
    screenshot = instance.computer(action="take_screenshot").base_64_image
    ```
  

  
    ```typescript
    const screenshot = await instance.computer({action: "take_screenshot"}).base64Image;
    ```
  


#### `get_cursor_position`

Get current mouse cursor coordinates


  
    ```python
    cursor_position = instance.computer(action="get_cursor_position").output
    ```
  

  
    ```typescript
    const cursorPosition = await instance.computer({action: "get_cursor_position"}).output;
    ```
  


### bash

Run a bash command

> **Note:** Bash commands time out after 10 seconds by default, but you can customize this with the `timeout` parameter. When a command times out, it will continue running in the session. To run other commands while waiting for a long-running command to complete, start them in a different session. Use `check_session` to check back on a session's status. Once a command finishes execution, the session becomes available again for new commands.


  
    ```python Run a bash command
    output = instance.bash(command="ls -la")
    ```

    ```python Run a command in a specific session
    output = instance.bash(command="ls -la", session=1)
    ```

    ```python Run a command with custom timeout
    output = instance.bash(command="sleep 30", timeout=60)
    ```

    ```python Restart a session
    instance.bash(restart=True, session=1)
    ```

    ```python List available bash sessions
    sessions = instance.bash(list_sessions=True)
    ```

    ```python Check the status of a session
    session_exists = instance.bash(check_session=1)
    ```
  

  
    ```typescript Run a bash command
    const output = await instance.bash({command: "ls -la"});
    ```

    ```typescript Run a command in a specific session
    const output = await instance.bash({command: "ls -la", session: 1});
    ```

    ```typescript Run a command with custom timeout
    const output = await instance.bash({command: "sleep 30", timeout: 60});
    ```

    ```typescript Restart a session
    await instance.bash({restart: true, session: 1});
    ```

    ```typescript List available bash sessions
    const sessions = await instance.bash({listSessions: true});
    ```

    ```typescript Check the status of a session
    const sessionExists = await instance.bash({checkSession: 1});
    ```
  


### edit

> **Deprecated:** Please use the `file` tool instead which provides more comprehensive file management capabilities.

Edit a file on the instance


  
    ```python Create a new file
    instance.edit(command="create", path="hello.txt", file_text="Hello world")
    ```

    ```python Replace text in a file
    instance.edit(command="str_replace", path="hello.txt", old_str="Hello", new_str="Hi")
    ```

    ```python Insert text at a specific line
    instance.edit(command="insert", path="hello.txt", insert_line=2, file_text="New line")
    ```
  

  
    ```typescript Create a new file
    await instance.edit({command: "create", path: "hello.txt", fileText: "Hello world"});
    ```

    ```typescript Replace text in a file
    await instance.edit({command: "str_replace", path: "hello.txt", oldStr: "Hello", newStr: "Hi"});
    ```

    ```typescript Insert text at a specific line
    await instance.edit({command: "insert", path: "hello.txt", insertLine: 2, fileText: "New line"});
    ```
  


### file

Manage files and directories on the instance

#### `read`

Read the content of a file in text or binary mode


  Path to the file to read



  Read mode: "text" or "binary"



  Text encoding when mode is "text"



  
    ```python Read text file
    content = instance.file(command="read", path="my_file.txt")
    ```

    ```python Read binary file
    binary_content = instance.file(command="read", path="image.png", mode="binary")
    ```
  

  
    ```typescript Read text file
    const content = await instance.file({command: "read", path: "my_file.txt"});
    ```

    ```typescript Read binary file
    const binaryContent = await instance.file({command: "read", path: "image.png", mode: "binary"});
    ```
  


#### `write`

Write content to a file, overwriting if it exists


  Path to the file to write



  Content to write to the file



  Write mode: "text" or "binary" (base64 encoded for binary)



  Text encoding when mode is "text"



  
    ```python Write text to file
    instance.file(command="write", path="my_file.txt", content="Hello world")
    ```
  

  
    ```typescript Write text to file
    await instance.file({command: "write", path: "my_file.txt", content: "Hello world"});
    ```
  


#### `append`

Append content to an existing file or create it if it doesn't exist


  Path to the file to append to



  Content to append to the file



  Append mode: "text" or "binary" (base64 encoded for binary)



  Text encoding when mode is "text"



  
    ```python Append text
    instance.file(command="append", path="my_file.txt", content="New content")
    ```
  

  
    ```typescript Append text
    await instance.file({command: "append", path: "my_file.txt", content: "New content"});
    ```
  


#### `exists`

Check if a path exists


  Path to check



  
    ```python Check if file exists
    exists = instance.file(command="exists", path="my_file.txt")
    ```
  

  
    ```typescript Check if file exists
    const exists = await instance.file({command: "exists", path: "my_file.txt"});
    ```
  


#### `list`

List the contents of a directory


  Path to the directory to list



  
    ```python List directory contents
    files = instance.file(command="list", path="my_directory")
    ```
  

  
    ```typescript List directory contents
    const files = await instance.file({command: "list", path: "my_directory"});
    ```
  


#### `mkdir`

Create a directory, including parent directories if needed


  Path to the directory to create



  
    ```python Create directory
    instance.file(command="mkdir", path="new_directory")
    ```
  

  
    ```typescript Create directory
    await instance.file({command: "mkdir", path: "new_directory"});
    ```
  


#### `rmdir`

Remove an empty directory


  Path to the directory to remove



  
    ```python Remove directory
    instance.file(command="rmdir", path="empty_directory")
    ```
  

  
    ```typescript Remove directory
    await instance.file({command: "rmdir", path: "empty_directory"});
    ```
  


#### `delete`

Delete a file or directory


  Path to delete



  Delete directory contents recursively



  
    ```python Delete file
    instance.file(command="delete", path="file.txt")
    ```

    ```python Delete directory recursively
    instance.file(command="delete", path="directory", recursive=True)
    ```
  

  
    ```typescript Delete file
    await instance.file({command: "delete", path: "file.txt"});
    ```

    ```typescript Delete directory recursively
    await instance.file({command: "delete", path: "directory", recursive: true});
    ```
  


#### `move`

Move or rename a file or directory


  Source path



  Destination path



  
    ```python Move or rename
    instance.file(command="move", src="old_name.txt", dst="new_name.txt")
    ```
  

  
    ```typescript Move or rename
    await instance.file({command: "move", src: "old_name.txt", dst: "new_name.txt"});
    ```
  


#### `copy`

Copy a file or directory


  Source path



  Destination path



  
    ```python Copy file or directory
    instance.file(command="copy", src="source.txt", dst="destination.txt")
    ```
  

  
    ```typescript Copy file or directory
    await instance.file({command: "copy", src: "source.txt", dst: "destination.txt"});
    ```
  


#### `view`

View file content with line numbers or list directory contents


  Path to view



  Optional \[start, end] line range to view



  
    ```python View with line numbers
    content = instance.file(command="view", path="my_file.txt")
    ```

    ```python View specific line range
    content = instance.file(command="view", path="my_file.txt", view_range=[10, 20])
    ```
  

  
    ```typescript View with line numbers
    const content = await instance.file({command: "view", path: "my_file.txt"});
    ```

    ```typescript View specific line range
    const content = await instance.file({command: "view", path: "my_file.txt", viewRange: [10, 20]});
    ```
  


#### `create`

Create a new file with the given content, failing if it already exists


  Path to the file to create



  Content to write to the new file



  Create mode: "text" or "binary" (base64 encoded for binary)



  Text encoding when mode is "text"



  
    ```python Create a new file
    instance.file(command="create", path="new_file.txt", content="New file content")
    ```
  

  
    ```typescript Create a new file
    await instance.file({command: "create", path: "new_file.txt", content: "New file content"});
    ```
  


#### `replace`

Replace a string in a file


  Path to the file



  String to replace



  Replacement string



  Replace all occurrences if true, only first occurrence if false



  
    ```python Replace first occurrence
    instance.file(command="replace", path="my_file.txt", old_str="old text", new_str="new text")
    ```

    ```python Replace all occurrences
    instance.file(command="replace", path="my_file.txt", old_str="old text", new_str="new text", all_occurrences=True)
    ```
  

  
    ```typescript Replace first occurrence
    await instance.file({command: "replace", path: "my_file.txt", oldStr: "old text", newStr: "new text"});
    ```

    ```typescript Replace all occurrences
    await instance.file({command: "replace", path: "my_file.txt", oldStr: "old text", newStr: "new text", allOccurrences: true});
    ```
  


#### `insert`

Insert text at a specific line in a file


  Path to the file



  Line number to insert at (1-based)



  Text to insert



  
    ```python Insert at line
    instance.file(command="insert", path="my_file.txt", line=2, text="New line content")
    ```
  

  
    ```typescript Insert at line
    await instance.file({command: "insert", path: "my_file.txt", line: 2, text: "New line content"});
    ```
  


#### `delete_lines`

Delete specified lines from a file


  Path to the file



  Array of line numbers to delete (1-based)



  
    ```python Delete specific lines
    instance.file(command="delete_lines", path="my_file.txt", lines=[2, 5, 10])
    ```
  

  
    ```typescript Delete specific lines
    await instance.file({command: "delete_lines", path: "my_file.txt", lines: [2, 5, 10]});
    ```
  


#### `undo`

Undo the last text editing operation on a file


  Path to the file



  
    ```python Undo last edit
    instance.file(command="undo", path="my_file.txt")
    ```
  

  
    ```typescript Undo last edit
    await instance.file({command: "undo", path: "my_file.txt"});
    ```
  


#### `grep`

Search for a pattern in a file or directory


  Regular expression pattern to search for



  Path to file or directory to search



  Whether search is case sensitive



  Search directories recursively (required for directory paths)



  Include line numbers in results



  
    ```python Search in file
    results = instance.file(command="grep", path="my_file.txt", pattern="search term")
    ```

    ```python Recursive search in directory
    results = instance.file(command="grep", path="my_directory", pattern="search term", 
                                recursive=True, case_sensitive=False)
    ```
  

  
    ```typescript Search in file
    const results = await instance.file({command: "grep", path: "my_file.txt", pattern: "search term"});
    ```

    ```typescript Recursive search in directory
    const results = await instance.file({command: "grep", path: "my_directory", pattern: "search term", 
                                            recursive: true, caseSensitive: false});
    ```
  


### `upload`

Upload a file to the instance


  The file to upload, can be a file object, bytes, or string



  Destination path on the instance



  
    ```python
    # Upload a file from local path
    with open("local_file.txt", "rb") as f:
        response = instance.upload(file=f, path="uploaded_file.txt")

    # Upload string content as a file
    instance.upload(file="Hello World", path="hello.txt")

    # Upload with explicit filename and content type
    instance.upload(
        file=("myfile.txt", "File content", "text/plain"),
        path="myfile.txt"
    )
    ```
  

  
    ```typescript
    // Upload a file
    const file = new File(["file content"], "filename.txt", { type: "text/plain" });
    const response = await instance.upload(file, { path: "uploaded_file.txt" });

    // Upload a Blob
    const blob = new Blob(["Hello World"], { type: "text/plain" });
    await instance.upload(blob, { path: "hello.txt" });
    ```
  


### `stop`

Stop the instance


  
    `python instance.stop() `
  

  
    `typescript await instance.stop(); `
  


### `pause`

Pause the instance


  
    `python instance.pause() `
  

  
    `typescript await instance.pause(); `
  


### `resume`

Resume the instance


  
    ```python Resume with default timeout
    instance.resume()
    ```

    ```python Resume with custom timeout
    instance.resume(timeout_hours=2.5)
    ```
  

  
    ```typescript Resume with default timeout
    await instance.resume();
    ```

    ```typescript Resume with custom timeout
    await instance.resume({timeoutHours: 2.5});
    ```
  


## Compatible tools

* `BashTool`
* `ComputerTool`
* `EditTool`

## Screen resolution

By default, the Ubuntu instance runs at 1024x768 resolution. You can specify a custom resolution when starting the instance:


  
    ```python
    instance = client.start_ubuntu(resolution=[1920, 1080])
    ```
  

  
    ```typescript
    const instance = await client.startUbuntu({resolution: [1920, 1080]});
    ```
  


## Additional protocols

The Ubuntu instance supports several protocols that provide additional functionality:

* [Browser](/protocols/browser) - Control the browser with Playwright
* [Code Execution](/protocols/code) - Execute code in Python and JavaScript
* [Environment Variables](/protocols/env) - Manage environment variables


# Browser

> Control a browser directly in your Scrapybara instance with Playwright


  
    
      
        ```python
        from scrapybara import Scrapybara

        client = Scrapybara(api_key="your_api_key")
        instance = client.start_ubuntu()
        ```
      

      
        ```python
        cdp_url = instance.browser.start().cdp_url
        ```
      

      
        To save the authenticated state of a browser session, use the `saveAuth` method.

        ```python
        auth_state_id = instance.browser.save_auth(name="default").auth_state_id
        ```

        Now, you can reuse the saved auth state on other instances by passing the `auth_state_id` to the `authenticate` method. The browser needs to be started first.

        ```python
        instance.browser.authenticate(auth_state_id=auth_state_id)
        ```
      

      
        ```python
        from playwright.sync_api import sync_playwright

        playwright = sync_playwright().start()
        browser = playwright.chromium.connect_over_cdp(cdp_url)
        ```
      

      
        ```python
        page = browser.new_page()
        page.goto("https://scrapybara.com")
        screenshot = page.screenshot()
        ```
      

      
        ```python
        instance.browser.stop()
        ```
      
    
  

  
    
      
        ```typescript
        import { ScrapybaraClient } from "scrapybara";

        const client = new ScrapybaraClient({ apiKey: "your_api_key" });
        const instance = await client.startUbuntu();
        ```
      

      
        ```typescript
        const cdpUrl = await instance.browser.start().cdpUrl;
        ```
      

      
        To save the authenticated state of a browser session, use the `saveAuth` method.

        ```typescript
        const authStateId = await instance.browser.saveAuth({
          name: "default",
        }).authStateId;
        ```

        Now, you can reuse the saved auth state on other instances by passing the `authStateId` to the `authenticate` method. The browser needs to be started first.

        ```typescript
        await instance.browser.authenticate({ authStateId });
        ```
      

      
        ```typescript
        import { chromium } from "playwright";

        const browser = await chromium.connectOverCDP(cdpUrl);
        ```
      

      
        ```typescript
        const page = await browser.newPage();
        await page.goto("https://scrapybara.com");
        const screenshot = await page.screenshot();
        ```
      

      
        ```typescript
        await instance.browser.stop();
        ```
      
    
  



# Code Execution

> Execute code in your Scrapybara instance


  
    
      
        ```python
        from scrapybara import Scrapybara

        client = Scrapybara(api_key="your_api_key")
        instance = client.start_ubuntu()
        ```
      

      
        ```python
        result = instance.code.execute(
            code="print('Hello from Scrapybara!')",
            kernel_name="python3"  # Optional: specify kernel
        )
        ```
      

      
        ```python
        kernels = instance.notebook.list_kernels()
        ```
      

      
        ```python
        notebook = instance.notebook.create(
            name="my_notebook",
            kernel_name="python3"
        )
        ```
      

      
        ```python
        # Add a code cell
        cell = instance.notebook.add_cell(
            notebook_id=notebook.id,
            type="code",
            content="print('Hello from Scrapybara!')"
        )

        # Execute the cell
        result = instance.notebook.execute_cell(
            notebook_id=notebook.id,
            cell_id=cell.id
        )
        ```
      

      
        ```python
        # Execute all cells in the notebook
        results = instance.notebook.execute(notebook_id=notebook.id)
        ```
      

      
        ```python
        # Delete the notebook when done
        instance.notebook.delete(notebook_id=notebook.id)
        ```
      
    
  

  
    
      
        ```typescript
        import { ScrapybaraClient } from "scrapybara";

        const client = new ScrapybaraClient({ apiKey: "your_api_key" });
        const instance = await client.startUbuntu();
        ```
      

      
        ```typescript
        const result = await instance.code.execute({
            code: "print('Hello from Scrapybara!')",
            kernelName: "python3"  // Optional: specify kernel
        });
        ```
      

      
        ```typescript
        const kernels = await instance.notebook.listKernels();
        ```
      

      
        ```typescript
        const notebook = await instance.notebook.create({
            name: "my_notebook",
            kernelName: "python3"
        });
        ```
      

      
        ```typescript
        // Add a code cell
        const cell = await instance.notebook.addCell({
            notebookId: notebook.id,
            type: "code",
            content: "print('Hello from Scrapybara!')"
        });

        // Execute the cell
        const result = await instance.notebook.executeCell({
            notebookId: notebook.id,
            cellId: cell.id
        });
        ```
      

      
        ```typescript
        // Execute all cells in the notebook
        const results = await instance.notebook.execute({
            notebookId: notebook.id
        });
        ```
      

      
        ```typescript
        // Delete the notebook when done
        await instance.notebook.delete({
            notebookId: notebook.id
        });
        ```
      
    
  



# Environment Variables

> Manage environment variables in your Scrapybara instance


  
    
      
        ```python
        from scrapybara import Scrapybara

        client = Scrapybara(api_key="your_api_key")
        instance = client.start_ubuntu()
        ```
      

      
        ```python
        # Set one or more environment variables
        instance.env.set(
            variables={
                "API_KEY": "secret_key",
                "DEBUG": "true",
                "DATABASE_URL": "postgresql://localhost:5432/db"
            }
        )
        ```
      

      
        ```python
        # Get all environment variables
        response = instance.env.get()
        env_vars = response.variables
        ```
      

      
        ```python
        # Delete specific environment variables
        instance.env.delete(
            keys=["API_KEY", "DEBUG"]
        )
        ```
      
    
  

  
    
      
        ```typescript
        import { ScrapybaraClient } from "scrapybara";

        const client = new ScrapybaraClient({ apiKey: "your_api_key" });
        const instance = await client.startUbuntu();
        ```
      

      
        ```typescript
        // Set one or more environment variables
        await instance.env.set({
            variables: {
                API_KEY: "secret_key",
                DEBUG: "true",
                DATABASE_URL: "postgresql://localhost:5432/db"
            }
        });
        ```
      

      
        ```typescript
        // Get all environment variables
        const response = await instance.env.get();
        const envVars = response.variables;
        ```
      

      
        ```typescript
        // Delete specific environment variables
        await instance.env.delete({
            keys: ["API_KEY", "DEBUG"]
        });
        ```
      
    
  



# Browser

> Deploy a Browser instance

## BrowserInstance

The `BrowserInstance` is a lightweight Chromium instance that supports interactive streaming, computer actions, Playwright CDP control, and saving/loading auth states. We recommend using this instance type if your task is constrained to the browser.

* Fastest start up time
* 1x compute cost

## Start a browser instance


  
    ```python
    instance = client.start_browser()
    ```
  

  
    ```typescript
    const instance = await client.startBrowser();
    ```
  


## Available actions

### get\_cdp\_url

Get the Playwright CDP URL


  
    ```python
    cdp_url = instance.get_cdp_url().cdp_url
    ```
  

  
    ```typescript
    const cdpUrl = await instance.getCdpUrl().cdpUrl;
    ```
  


### save\_auth

Save the browser auth state


  
    ```python
    auth_state_id = instance.browser.save_auth(name="default").auth_state_id
    ```
  

  
    ```typescript
    const authStateId = await instance.browser.saveAuth({name: "default"}).authStateId;
    ```
  


### authenticate

Authenticate the browser using a saved auth state


  
    ```python
    instance.browser.authenticate(auth_state_id=auth_state_id)
    ```
  

  
    ```typescript
    await instance.browser.authenticate({authStateId: authStateId});
    ```
  


### screenshot

Take a base64 encoded image of the current desktop


  
    ```python
    base_64_image = instance.screenshot().base_64_image
    ```
  

  
    ```typescript
    const base64Image = await instance.screenshot();
    ```
  


### get\_stream\_url

Get the interactive stream URL


  
    ```python
    stream_url = instance.get_stream_url().stream_url
    ```
  

  
    ```typescript
    const streamUrl = await instance.getStreamUrl();
    ```
  


### computer

Perform computer actions with the mouse and keyboard

#### `move_mouse`

Move mouse cursor to specific coordinates


  \[x, y] coordinates to move to



  List of modifier keys to hold during the action



  
    ```python Move mouse
    instance.computer(action="move_mouse", coordinates=[100, 200])
    ```

    ```python Move mouse while holding shift
    instance.computer(action="move_mouse", coordinates=[100, 200], hold_keys=["shift"])
    ```
  

  
    ```typescript Move mouse
    await instance.computer({action: "move_mouse", coordinates: [100, 200]});
    ```

    ```typescript Move mouse while holding shift
    await instance.computer({action: "move_mouse", coordinates: [100, 200], holdKeys: ["shift"]});
    ```
  


#### `click_mouse`

Perform a mouse click at current position or specified coordinates


  Mouse button to click ("left", "right", "middle", "back", "forward")



  Type of click action ("down", "up", "click")



  \[x, y] coordinates to click at



  Number of clicks



  List of modifier keys to hold during the action



  
    ```python Left click at current position
    instance.computer(action="click_mouse", button="left")
    ```

    ```python Right click at coordinates
    instance.computer(action="click_mouse", button="right", coordinates=[300, 400])
    ```

    ```python Mouse down
    instance.computer(action="click_mouse", button="left", click_type="down")
    ```

    ```python Double click at coordinates
    instance.computer(action="click_mouse", button="left", num_clicks=2, coordinates=[500, 300])
    ```
  

  
    ```typescript Left click at current position
    await instance.computer({action: "click_mouse", button: "left"});
    ```

    ```typescript Right click at coordinates
    await instance.computer({action: "click_mouse", button: "right", coordinates: [300, 400]});
    ```

    ```typescript Mouse down
    await instance.computer({action: "click_mouse", button: "left", clickType: "down"});
    ```

    ```typescript Double click at coordinates
    await instance.computer({action: "click_mouse", button: "left", numClicks: 2, coordinates: [500, 300]});
    ```
  


#### `drag_mouse`

Click and drag from current position to specified coordinates


  List of \[x, y] coordinate pairs defining the drag path



  List of modifier keys to hold during the action



  
    ```python Drag to coordinates
    instance.computer(action="drag_mouse", path=[[100, 200], [300, 400]])
    ```
  

  
    ```typescript Drag to coordinates
    await instance.computer({action: "drag_mouse", path: [[100, 200], [300, 400]]});
    ```
  


#### `scroll`

Scroll horizontally and/or vertically


  \[x, y] coordinates to scroll at



  Horizontal scroll amount



  Vertical scroll amount



  List of modifier keys to hold during the action



  
    ```python Scroll down
    instance.computer(action="scroll", coordinates=[100, 100], delta_x=0, delta_y=200)
    ```

    ```python Scroll right
    instance.computer(action="scroll", coordinates=[100, 100], delta_x=200, delta_y=0)
    ```
  

  
    ```typescript Scroll down
    await instance.computer({action: "scroll", coordinates: [100, 100], deltaX: 0, deltaY: 200});
    ```

    ```typescript Scroll right
    await instance.computer({action: "scroll", coordinates: [100, 100], deltaX: 100, deltaY: 0});
    ```
  


#### `press_key`

Press a key or combination of keys. Scrapybara supports keys defined by [X keysyms](https://github.com/D-Programming-Deimos/libX11/blob/master/c/X11/keysymdef.h). Common aliases are also supported:

* `alt` → `Alt_L`
* `ctrl`, `control` → `Control_L`
* `meta` → `Meta_L`
* `super` → `Super_L`
* `shift` → `Shift_L`
* `enter`, `return` → `Return`


  List of keys to press



  Time to hold keys in seconds



  
    ```python Press ctrl+c
    instance.computer(action="press_key", keys=["ctrl", "c"])
    ```

    ```python Hold shift for 2 seconds
    instance.computer(action="press_key", keys=["shift"], duration=2)
    ```

    ```python Press enter/return
    instance.computer(action="press_key", keys=["Return"])
    ```
  

  
    ```typescript Press ctrl+c
    await instance.computer({action: "press_key", keys: ["ctrl", "c"]});
    ```

    ```typescript Hold shift for 2 seconds
    await instance.computer({action: "press_key", keys: ["shift"], duration: 2});
    ```

    ```typescript Press enter/return
    await instance.computer({action: "press_key", keys: ["Return"]});
    ```
  


#### `type_text`

Type text into the active window


  Text to type



  List of modifier keys to hold while typing



  
    ```python Type text
    instance.computer(action="type_text", text="Hello world")
    ```
  

  
    ```typescript Type text
    await instance.computer({action: "type_text", text: "Hello world"});
    ```
  


#### `wait`

Wait for a specified duration


  Time to wait in seconds



  
    ```python Wait for 3 seconds
    instance.computer(action="wait", duration=3)
    ```
  

  
    ```typescript Wait for 3 seconds
    await instance.computer({action: "wait", duration: 3});
    ```
  


#### `take_screenshot`

Take a screenshot of the desktop


  
    ```python
    screenshot = instance.computer(action="take_screenshot").base64_image
    ```
  

  
    ```typescript
    const screenshot = await instance.computer({action: "take_screenshot"}).base64Image;
    ```
  


#### `get_cursor_position`

Get current mouse cursor coordinates


  
    ```python
    cursor_position = instance.computer(action="get_cursor_position").output
    ```
  

  
    ```typescript
    const cursorPosition = await instance.computer({action: "get_cursor_position"}).output;
    ```
  


### `stop`

Stop the instance


  
    ```python
    instance.stop()
    ```
  

  
    ```typescript
    await instance.stop();
    ```
  


### `pause`

Pause the instance


  
    ```python
    instance.pause()
    ```
  

  
    ```typescript
    await instance.pause();
    ```
  


### `resume`

Resume the instance


  
    ```python Resume with default timeout
    instance.resume()
    ```

    ```python Resume with custom timeout
    instance.resume(timeout_hours=2.5)
    ```
  

  
    ```typescript Resume with default timeout
    await instance.resume();
    ```

    ```typescript Resume with custom timeout
    await instance.resume({timeoutHours: 2.5});
    ```
  


## Compatible tools

* `ComputerTool`

## Screen resolution

By default, the Browser instance runs at 1024x768 resolution. You can specify a custom resolution when starting the instance:


  
    ```python
    instance = client.start_browser(resolution=[1920, 1080])
    ```
  

  
    ```typescript
    const instance = await client.startBrowser({resolution: [1920, 1080]});
    ```
  



# Windows

> Deploy a Windows instance


  Windows instances are in early access. Join our Discord to get started.


## WindowsInstance

The `WindowsInstance` is a full-fledged Windows 11 desktop that supports interactive streaming and computer actions. We recommend using this instance type if you need to interact with Windows-only applications.

* Slow start up time
* 2x compute cost

## Start a Windows instance


  
    ```python
    instance = client.start_windows()
    ```
  

  
    ```typescript
    const instance = await client.startWindows();
    ```
  


## Available actions

### screenshot

Take a base64 encoded image of the current desktop


  
    ```python
    base_64_image = instance.screenshot().base_64_image
    ```
  

  
    ```typescript
    const base64Image = await instance.screenshot();
    ```
  


### get\_stream\_url

Get the interactive stream URL


  
    ```python
    stream_url = instance.get_stream_url().stream_url
    ```
  

  
    ```typescript
    const streamUrl = await instance.getStreamUrl();
    ```
  


### computer

Perform computer actions with the mouse and keyboard

#### `move_mouse`

Move mouse cursor to specific coordinates


  \[x, y] coordinates to move to



  List of modifier keys to hold during the action



  
    ```python Move mouse
    instance.computer(action="move_mouse", coordinates=[100, 200])
    ```

    ```python Move mouse while holding shift
    instance.computer(action="move_mouse", coordinates=[100, 200], hold_keys=["shift"])
    ```
  

  
    ```typescript Move mouse
    await instance.computer({action: "move_mouse", coordinates: [100, 200]});
    ```

    ```typescript Move mouse while holding shift
    await instance.computer({action: "move_mouse", coordinates: [100, 200], holdKeys: ["shift"]});
    ```
  


#### `click_mouse`

Perform a mouse click at current position or specified coordinates


  Mouse button to click ("left", "right", "middle", "back", "forward")



  Type of click action ("down", "up", "click")



  \[x, y] coordinates to click at



  Number of clicks



  List of modifier keys to hold during the action



  
    ```python Left click at current position
    instance.computer(action="click_mouse", button="left")
    ```

    ```python Right click at coordinates
    instance.computer(action="click_mouse", button="right", coordinates=[300, 400])
    ```

    ```python Mouse down
    instance.computer(action="click_mouse", button="left", click_type="down")
    ```

    ```python Double click at coordinates
    instance.computer(action="click_mouse", button="left", num_clicks=2, coordinates=[500, 300])
    ```
  

  
    ```typescript Left click at current position
    await instance.computer({action: "click_mouse", button: "left"});
    ```

    ```typescript Right click at coordinates
    await instance.computer({action: "click_mouse", button: "right", coordinates: [300, 400]});
    ```

    ```typescript Mouse down
    await instance.computer({action: "click_mouse", button: "left", clickType: "down"});
    ```

    ```typescript Double click at coordinates
    await instance.computer({action: "click_mouse", button: "left", numClicks: 2, coordinates: [500, 300]});
    ```
  


#### `drag_mouse`

Click and drag from current position to specified coordinates


  List of \[x, y] coordinate pairs defining the drag path



  List of modifier keys to hold during the action



  
    ```python Drag to coordinates
    instance.computer(action="drag_mouse", path=[[100, 200], [300, 400]])
    ```
  

  
    ```typescript Drag to coordinates
    await instance.computer({action: "drag_mouse", path: [[100, 200], [300, 400]]});
    ```
  


#### `scroll`

Scroll horizontally and/or vertically


  \[x, y] coordinates to scroll at



  Horizontal scroll amount



  Vertical scroll amount



  List of modifier keys to hold during the action



  
    ```python Scroll down
    instance.computer(action="scroll", coordinates=[100, 100], delta_x=0, delta_y=200)
    ```

    ```python Scroll right
    instance.computer(action="scroll", coordinates=[100, 100], delta_x=200, delta_y=0)
    ```
  

  
    ```typescript Scroll down
    await instance.computer({action: "scroll", coordinates: [100, 100], deltaX: 0, deltaY: 200});
    ```

    ```typescript Scroll right
    await instance.computer({action: "scroll", coordinates: [100, 100], deltaX: 100, deltaY: 0});
    ```
  


#### `press_key`

Press a key or combination of keys. Scrapybara supports keys defined by [X keysyms](https://github.com/D-Programming-Deimos/libX11/blob/master/c/X11/keysymdef.h). Common aliases are also supported:

* `alt` → `Alt_L`
* `ctrl`, `control` → `Control_L`
* `meta` → `Meta_L`
* `super` → `Super_L`
* `shift` → `Shift_L`
* `enter`, `return` → `Return`


  List of keys to press



  Time to hold keys in seconds



  
    ```python Press ctrl+c
    instance.computer(action="press_key", keys=["ctrl", "c"])
    ```

    ```python Hold shift for 2 seconds
    instance.computer(action="press_key", keys=["shift"], duration=2)
    ```

    ```python Press enter/return
    instance.computer(action="press_key", keys=["Return"])
    ```
  

  
    ```typescript Press ctrl+c
    await instance.computer({action: "press_key", keys: ["ctrl", "c"]});
    ```

    ```typescript Hold shift for 2 seconds
    await instance.computer({action: "press_key", keys: ["shift"], duration: 2});
    ```

    ```typescript Press enter/return
    await instance.computer({action: "press_key", keys: ["Return"]});
    ```
  


#### `type_text`

Type text into the active window


  Text to type



  List of modifier keys to hold while typing



  
    ```python Type text
    instance.computer(action="type_text", text="Hello world")
    ```
  

  
    ```typescript Type text
    await instance.computer({action: "type_text", text: "Hello world"});
    ```
  


#### `wait`

Wait for a specified duration


  Time to wait in seconds



  
    ```python Wait for 3 seconds
    instance.computer(action="wait", duration=3)
    ```
  

  
    ```typescript Wait for 3 seconds
    await instance.computer({action: "wait", duration: 3});
    ```
  


#### `take_screenshot`

Take a screenshot of the desktop


  
    ```python
    screenshot = instance.computer(action="take_screenshot").base64_image
    ```
  

  
    ```typescript
    const screenshot = await instance.computer({action: "take_screenshot"}).base64Image;
    ```
  


#### `get_cursor_position`

Get current mouse cursor coordinates


  
    ```python
    cursor_position = instance.computer(action="get_cursor_position").output
    ```
  

  
    ```typescript
    const cursorPosition = await instance.computer({action: "get_cursor_position"}).output;
    ```
  


### `stop`

Stop the instance


  
    ```python
    instance.stop()
    ```
  

  
    ```typescript
    await instance.stop();
    ```
  


### `pause`

Pause the instance


  
    ```python
    instance.pause()
    ```
  

  
    ```typescript
    await instance.pause();
    ```
  


### `resume`

Resume the instance


  
    ```python Resume with default timeout
    instance.resume()
    ```

    ```python Resume with custom timeout
    instance.resume(timeout_hours=2.5)
    ```
  

  
    ```typescript Resume with default timeout
    await instance.resume();
    ```

    ```typescript Resume with custom timeout
    await instance.resume({timeoutHours: 2.5});
    ```
  


## Compatible tools

* `ComputerTool`

## Screen resolution

By default, the Windows instance runs at 1024x768 resolution.


# Starter Templates

> Templates for getting started with Scrapybara instances and the Act SDK

## Python


  View the template


## TypeScript


  View the template



# Cursor Rules

> Recommended .cursorrules for working with Cursor

## .cursorrules


  
    ```md .cursorrules
    You are working with Scrapybara, a Python SDK for deploying and managing remote desktop instances for AI agents. Use this guide to properly interact with the SDK.

    **CORE SDK USAGE:**
    - Initialize client: from scrapybara import Scrapybara; client = Scrapybara(api_key="KEY")
    - Instance lifecycle:
        instance = client.start_ubuntu(timeout_hours=1)
        instance.pause() # Pause to save resources
        instance.resume(timeout_hours=1) # Resume work
        instance.stop() # Terminate and clean up
    - Instance types:
        ubuntu_instance = client.start_ubuntu(): supports bash, computer, edit, browser
        browser_instance = client.start_browser(): supports computer, browser
        windows_instance = client.start_windows(): supports computer

    **TYPE IMPORTS:**
    - Core types:
        from scrapybara import Scrapybara
    - Instance types:
        from scrapybara.client import UbuntuInstance, BrowserInstance, WindowsInstance
    - Tool types:
        from scrapybara.tools import Tool, BashTool, ComputerTool, EditTool
    - Model types:
        from scrapybara.anthropic import Anthropic
    - Message types:
        from pydantic import BaseModel
        from typing import List, Union, Optional, Any
    - Error types:
        from scrapybara.core.api_error import ApiError

    **CORE INSTANCE OPERATIONS:**
    - Screenshots: instance.screenshot().base_64_image
    - Bash commands: instance.bash(command="ls -la")
    - Mouse control: instance.computer(action="move_mouse", coordinates=[x, y])
    - Click actions: instance.computer(action="click_mouse", button="right", coordinates=[x, y])
    - Drag actions: instance.computer(action="drag_mouse", path=[[x1, y1], [x2, y2]])
    - Scroll actions: instance.computer(action="scroll", coordinates=[x, y], delta_x=0, delta_y=0)
    - Key actions: instance.computer(action="press_key", keys=[keys])
    - Type actions: instance.computer(action="type_text", text="Hello world")
    - Wait actions: instance.computer(action="wait", duration=3)
    - Get cursor position: instance.computer(action="get_cursor_position").output
    - File operations: instance.file.read(path="/path/file"), instance.file.write(path="/path/file", content="data")

    **ACT SDK (Primary Focus):**
    - Purpose: Enables building computer use agents with unified tools and model interfaces
    - Core components:
    1. Model: Handles LLM integration (currently Anthropic)
        from scrapybara.anthropic import Anthropic
        model = Anthropic() # Or model = Anthropic(api_key="KEY") for own key
    2. Tools: Interface for computer interactions
        - BashTool: Run shell commands
        - ComputerTool: Mouse/keyboard control
        - EditTool: File operations
        tools = [
            BashTool(instance),
            ComputerTool(instance),
            EditTool(instance),
        ]
    3. Prompt:
        - system: system prompt, recommend to use UBUNTU_SYSTEM_PROMPT, BROWSER_SYSTEM_PROMPT, WINDOWS_SYSTEM_PROMPT
        - prompt: simple user prompt
        - messages: list of messages
        - Only include either prompt or messages, not both
    response = client.act(
        model=Anthropic(),
        tools=tools,
        system=UBUNTU_SYSTEM_PROMPT,
        prompt="Task",
        on_step=handle_step
    )
    messages = response.messages
    steps = response.steps
    text = response.text
    output = response.output
    usage = response.usage

    **MESSAGE HANDLING:**
    - Response Structure: Messages are structured with roles (user/assistant/tool) and typed content
    - Content Types:
    - TextPart: Simple text content
        TextPart(type="text", text="content")
    - ImagePart: Base64 or URL images
        ImagePart(type="image", image="base64...", mime_type="image/png")
    - ReasoningPart: Model reasoning content
        ReasoningPart(
            type="reasoning",
            id="id",
            reasoning="reasoning",
            signature="signature",
            instructions="instructions"
        )
    - ToolCallPart: Tool invocations
        ToolCallPart(
            type="tool-call",
            tool_call_id="id",
            tool_name="bash",
            args={"command": "ls"}
        )
    - ToolResultPart: Tool execution results
        ToolResultPart(
            type="tool-result",
            tool_call_id="id",
            tool_name="bash",
            result="output",
            is_error=False
        )

    **STEP HANDLING:**
    def handle_step(step: Step):
        if step.reasoning_parts:
            print(f"Reasoning: {step.reasoning_parts}")
        if step.text:
            print(f"Text: {step.text}")
        if step.tool_calls:
            for call in step.tool_calls:
                print(f"Tool: {call.tool_name}")
        if step.tool_results:
            for result in step.tool_results:
                print(f"Result: {result.result}")
        print(f"Tokens: {step.usage.total_tokens if step.usage else 'N/A'}")

    **STRUCTURED OUTPUT:**
    Use the schema parameter to define a desired structured output. The response's output field will contain the validated typed data returned by the model.
    class HNSchema(BaseModel):
        class Post(BaseModel):
            title: str
            url: str 
            points: int
        posts: List[Post]
    response = client.act(
        model=Anthropic(),
        tools=tools,
        schema=HNSchema,
        system=SYSTEM_PROMPT,
        prompt="Get the top 10 posts on Hacker News",
    )
    posts = response.output.posts

    **TOKEN USAGE:**
    - Track token usage through TokenUsage objects
    - Fields: prompt_tokens, completion_tokens, total_tokens
    - Available in both Step and ActResponse objects

    **EXAMPLE:**
    from scrapybara import Scrapybara
    from scrapybara.anthropic import Anthropic
    from scrapybara.prompts import UBUNTU_SYSTEM_PROMPT
    from scrapybara.tools import BashTool, ComputerTool, EditTool

    client = Scrapybara()
    instance = client.start_ubuntu()
    instance.browser.start()

    response = client.act(
        model=Anthropic(),
        tools=[
            BashTool(instance),
            ComputerTool(instance),
            EditTool(instance),
        ],
        system=UBUNTU_SYSTEM_PROMPT,
        prompt="Go to the YC website and fetch the HTML",
        on_step=lambda step: print(f"{step}\n"),
    )
    messages = response.messages
    steps = response.steps
    text = response.text
    output = response.output
    usage = response.usage

    instance.browser.stop()
    instance.stop()

    **EXECUTION PATTERNS:**
    1. Basic agent execution:
    response = client.act(
        model=Anthropic(),
        tools=tools,
        system="System context here",
        prompt="Task description"
    )
    2. Browser automation:
    cdp_url = instance.browser.start().cdp_url
    auth_state_id = instance.browser.save_auth(name="default").auth_state_id  # Save auth
    instance.browser.authenticate(auth_state_id=auth_state_id)  # Reuse auth
    3. File management:
    instance.file.write("/tmp/data.txt", "content")
    content = instance.file.read("/tmp/data.txt").content
    4. Environment variables:
    instance.env.set({"API_KEY": "value"})
    instance.env.get().variables
    instance.env.delete(["VAR_NAME"])

    **ERROR HANDLING:**
    from scrapybara.core.api_error import ApiError
    try:
        client.start_ubuntu()
    except ApiError as e:
        print(f"Error {e.status_code}: {e.body}")

    **IMPORTANT GUIDELINES:**
    - Always stop instances after use to prevent unnecessary billing
    - Use async client (AsyncScrapybara) for non-blocking operations
    - Handle API errors with try/except ApiError blocks
    - Default timeout is 60s; customize with timeout parameter or request_options
    - Instance auto-terminates after 1 hour by default
    - For browser operations, always start browser before BrowserTool usage
    - Prefer bash commands over GUI interactions for launching applications
    ```
  

  
    ```md .cursorrules
    You are working with Scrapybara, a TypeScript SDK for deploying and managing remote desktop instances for AI agents. Use this guide to properly interact with the SDK.

    **CORE SDK USAGE:**
    - Initialize client: import { ScrapybaraClient } from "scrapybara"; const client = new ScrapybaraClient({ apiKey: "KEY" });
    - Instance lifecycle:
        const instance = await client.startUbuntu({ timeoutHours: 1 });
        await instance.pause(); // Pause to save resources
        await instance.resume({ timeoutHours: 1 }); // Resume work
        await instance.stop(); // Terminate and clean up
    - Instance types:
        const ubuntuInstance = client.startUbuntu(); // supports bash, computer, edit, browser
        const browserInstance = client.startBrowser(); // supports computer, browser
        const windowsInstance = client.startWindows(); // supports computer

    **TYPE IMPORTS:**
    - Core types:
        import { ScrapybaraClient, UbuntuInstance, BrowserInstance, WindowsInstance } from "scrapybara";
    - Tool types:
        import { bashTool, computerTool, editTool } from "scrapybara/tools";
    - Model types:
        import { anthropic } from "scrapybara/anthropic";
    - Message types:
        import { z } from "zod";
    - Error types:
        import { ScrapybaraError } from "scrapybara";
    - Request/Response types:
        import { Scrapybara } from "scrapybara";  // Namespace containing all request/response types

    **CORE INSTANCE OPERATIONS:**
    - Screenshots: const base64Image = await instance.screenshot().base64Image;
    - Bash commands: await instance.bash({ command: "ls -la" });
    - Mouse control: await instance.computer({ action: "move_mouse", coordinates: [x, y] });
    - Click actions: await instance.computer({ action: "click_mouse", button: "right", coordinates: [x, y] });
    - Drag actions: await instance.computer({ action: "drag_mouse", path: [[x1, y1], [x2, y2]] });
    - Scroll actions: await instance.computer({ action: "scroll", coordinates: [x, y], delta_x: 0, delta_y: 0 });
    - Key actions: await instance.computer({ action: "press_key", keys: ["a", "b", "c"] });
    - Type actions: await instance.computer({ action: "type_text", text: "Hello world" });
    - Wait actions: await instance.computer({ action: "wait", duration: 3 });
    - Get cursor position: await instance.computer({ action: "get_cursor_position" });
    - File operations: await instance.file.read({ path: "/path/file" }), await instance.file.write({ path: "/path/file", content: "data" });

    **ACT SDK (Primary Focus):**
    - Purpose: Enables building computer use agents with unified tools and model interfaces
    - Core components:
    1. Model: Handles LLM integration (currently Anthropic)
        import { anthropic } from "scrapybara/anthropic";
        const model = anthropic(); // Or model = anthropic({ apiKey: "KEY" }) for own key
    2. Tools: Interface for computer interactions
        - bashTool: Run shell commands
        - computerTool: Mouse/keyboard control
        - editTool: File operations
        const tools = [
            bashTool(instance),
            computerTool(instance),
            editTool(instance),
        ];
    3. Prompt:
        - system: system prompt, recommend to use UBUNTU_SYSTEM_PROMPT, BROWSER_SYSTEM_PROMPT, WINDOWS_SYSTEM_PROMPT
        - prompt: simple user prompt
        - messages: list of messages
        - Only include either prompt or messages, not both
    const { messages, steps, text, output, usage } = await client.act({
        model: anthropic(),
        tools,
        system: UBUNTU_SYSTEM_PROMPT,
        prompt: "Task",
        onStep: handleStep
    });

    **MESSAGE HANDLING:**
    - Response Structure: Messages are structured with roles (user/assistant/tool) and typed content
    - Content Types:
    - TextPart: Simple text content
        { type: "text", text: "content" }
    - ImagePart: Base64 or URL images
        { type: "image", image: "base64...", mimeType: "image/png" }
    - ReasoningPart: Model reasoning content
        {
            type: "reasoning",
            id: "id",
            reasoning: "reasoning",
            signature: "signature",
            instructions: "instructions"
        }
    - ToolCallPart: Tool invocations
        {
            type: "tool-call",
            toolCallId: "id",
            toolName: "bash",
            args: { command: "ls" }
        }
    - ToolResultPart: Tool execution results
        {
            type: "tool-result",
            toolCallId: "id",
            toolName: "bash",
            result: "output",
            isError: false
        }

    **STEP HANDLING:**
    const handleStep = (step: Step) => {
        console.log(`Text: ${step.text}`);
        if (step.toolCalls) {
            for (const call of step.toolCalls) {
                console.log(`Tool: ${call.toolName}`);
            }
        }
        if (step.toolResults) {
            for (const result of step.toolResults) {
                console.log(`Result: ${result.result}`);
            }
        }
        console.log(`Tokens: ${step.usage?.totalTokens ?? 'N/A'}`);
    };

    **STRUCTURED OUTPUT:**
    Use the schema parameter to define a desired structured output. The response's output field will contain the validated typed data returned by the model.
    const schema = z.object({
        posts: z.array(z.object({
            title: z.string(),
            url: z.string(),
            points: z.number(),
        })),
    });

    const { output } = await client.act({
        model: anthropic(),
        tools,
        schema,
        system: UBUNTU_SYSTEM_PROMPT,
        prompt: "Get the top 10 posts on Hacker News",
    });

    const posts = output.posts;

    **TOKEN USAGE:**
    - Track token usage through TokenUsage objects
    - Fields: promptTokens, completionTokens, totalTokens
    - Available in both Step and ActResponse objects

    **EXAMPLE:**
    import { ScrapybaraClient } from "scrapybara";
    import { anthropic } from "scrapybara/anthropic";
    import { UBUNTU_SYSTEM_PROMPT } from "scrapybara/prompts";
    import { bashTool, computerTool, editTool } from "scrapybara/tools";

    const client = new ScrapybaraClient();
    const instance = await client.startUbuntu();
    await instance.browser.start();

    const { messages, steps, text, output, usage } = await client.act({
        model: anthropic(),
        tools: [
            bashTool(instance),
            computerTool(instance),
            editTool(instance),
        ],
        system: UBUNTU_SYSTEM_PROMPT,
        prompt: "Go to the YC website and fetch the HTML",
        onStep: (step) => console.log(`${step}\n`),
    });

    await instance.browser.stop();
    await instance.stop();

    **EXECUTION PATTERNS:**
    1. Basic agent execution:
    const { messages, steps, text, output, usage } = await client.act({
        model: anthropic(),
        tools,
        system: "System context here",
        prompt: "Task description"
    });
    2. Browser automation:
    const cdpUrl = await instance.browser.start().cdpUrl;
    const authStateId = await instance.browser.saveAuth({ name: "default" }).authStateId;  // Save auth
    await instance.browser.authenticate({ authStateId });  // Reuse auth
    3. File management:
    await instance.file.write({ path: "/tmp/data.txt", content: "content" });
    const content = await instance.file.read({ path: "/tmp/data.txt" }).content;
    4. Environment variables:
    await instance.env.set({ API_KEY: "value" });
    const vars = await instance.env.get().variables;
    await instance.env.delete(["VAR_NAME"]);

    **ERROR HANDLING:**
    import { ApiError } from "scrapybara/core";
    try {
        await client.startUbuntu();
    } catch (e) {
        if (e instanceof ApiError) {
            console.error(`Error ${e.statusCode}: ${e.body}`);
        }
    }

    **IMPORTANT GUIDELINES:**
    - Always stop instances after use to prevent unnecessary billing
    - Use async/await for all operations as they are asynchronous
    - Handle API errors with try/catch blocks
    - Default timeout is 60s; customize with timeout parameter or requestOptions
    - Instance auto-terminates after 1 hour by default
    - For browser operations, always start browser before browserTool usage
    - Prefer bash commands over GUI interactions for launching applications
    ```
  


## llms-full.txt

Need more context? Check out [llms-full.txt](/llms-full.txt).


# Start instance

```http
POST https://api.scrapybara.com/v1/start
Content-Type: application/json
```



## Response Body

- 200: Successful Response
- 422: Validation Error

## Examples

```shell
curl -X POST https://api.scrapybara.com/v1/start \
     -H "x-api-key: " \
     -H "Content-Type: application/json" \
     -d '{}'
```

```shell
curl -X POST https://api.scrapybara.com/v1/start \
     -H "x-api-key: " \
     -H "Content-Type: application/json" \
     -d '{}'
```

# Get instance by ID

```http
GET https://api.scrapybara.com/v1/instance/{instance_id}
```



## Path Parameters

- InstanceId (required)

## Response Body

- 200: Successful Response
- 422: Validation Error

## Examples

```shell
curl https://api.scrapybara.com/v1/instance/instance_id \
     -H "x-api-key: "
```

```shell
curl https://api.scrapybara.com/v1/instance/:instance_id \
     -H "x-api-key: "
```

# List all instances

```http
GET https://api.scrapybara.com/v1/instances
```



## Response Body

- 200: Successful Response

## Examples

```shell
curl https://api.scrapybara.com/v1/instances \
     -H "x-api-key: "
```

# List all browser authentication states

```http
GET https://api.scrapybara.com/v1/auth_states
```



## Response Body

- 200: Successful Response

## Examples

```shell
curl https://api.scrapybara.com/v1/auth_states \
     -H "x-api-key: "
```

# Take screenshot

```http
POST https://api.scrapybara.com/v1/instance/{instance_id}/screenshot
```



## Path Parameters

- InstanceId (required)

## Response Body

- 200: Successful Response
- 422: Validation Error

## Examples

```shell
curl -X POST https://api.scrapybara.com/v1/instance/instance_id/screenshot \
     -H "x-api-key: "
```

```shell
curl -X POST https://api.scrapybara.com/v1/instance/:instance_id/screenshot \
     -H "x-api-key: "
```

# Get stream URL

```http
GET https://api.scrapybara.com/v1/instance/{instance_id}/stream_url
```



## Path Parameters

- InstanceId (required)

## Response Body

- 200: Successful Response
- 422: Validation Error

## Examples

```shell
curl https://api.scrapybara.com/v1/instance/instance_id/stream_url \
     -H "x-api-key: "
```

```shell
curl https://api.scrapybara.com/v1/instance/:instance_id/stream_url \
     -H "x-api-key: "
```

# Run computer actions

```http
POST https://api.scrapybara.com/v1/instance/{instance_id}/computer
Content-Type: application/json
```



## Path Parameters

- InstanceId (required)

## Response Body

- 200: Successful Response
- 422: Validation Error

## Examples

```shell
curl -X POST https://api.scrapybara.com/v1/instance/instance_id/computer \
     -H "x-api-key: " \
     -H "Content-Type: application/json" \
     -d '{
  "action": "move_mouse",
  "coordinates": [
    1
  ]
}'
```

```shell
curl -X POST https://api.scrapybara.com/v1/instance/:instance_id/computer \
     -H "x-api-key: " \
     -H "Content-Type: application/json" \
     -d '{
  "action": "move_mouse",
  "coordinates": [
    0
  ]
}'
```

# Run bash actions

```http
POST https://api.scrapybara.com/v1/instance/{instance_id}/bash
Content-Type: application/json
```



## Path Parameters

- InstanceId (required)

## Response Body

- 200: Successful Response
- 422: Validation Error

## Examples

```shell
curl -X POST https://api.scrapybara.com/v1/instance/instance_id/bash \
     -H "x-api-key: " \
     -H "Content-Type: application/json" \
     -d '{}'
```

```shell
curl -X POST https://api.scrapybara.com/v1/instance/:instance_id/bash \
     -H "x-api-key: " \
     -H "Content-Type: application/json" \
     -d '{}'
```

# Run edit actions

```http
POST https://api.scrapybara.com/v1/instance/{instance_id}/edit
Content-Type: application/json
```



## Path Parameters

- InstanceId (required)

## Response Body

- 200: Successful Response
- 422: Validation Error

## Examples

```shell
curl -X POST https://api.scrapybara.com/v1/instance/instance_id/edit \
     -H "x-api-key: " \
     -H "Content-Type: application/json" \
     -d '{
  "command": "view",
  "path": "path"
}'
```

```shell
curl -X POST https://api.scrapybara.com/v1/instance/:instance_id/edit \
     -H "x-api-key: " \
     -H "Content-Type: application/json" \
     -d '{
  "command": "view",
  "path": "string"
}'
```

# Run file actions

```http
POST https://api.scrapybara.com/v1/instance/{instance_id}/file
Content-Type: application/json
```



## Path Parameters

- InstanceId (required)

## Response Body

- 200: Successful Response
- 422: Validation Error

## Examples

```shell
curl -X POST https://api.scrapybara.com/v1/instance/instance_id/file \
     -H "x-api-key: " \
     -H "Content-Type: application/json" \
     -d '{
  "command": "command"
}'
```

```shell
curl -X POST https://api.scrapybara.com/v1/instance/:instance_id/file \
     -H "x-api-key: " \
     -H "Content-Type: application/json" \
     -d '{
  "command": "string"
}'
```

# Upload a file to the instance

```http
POST https://api.scrapybara.com/v1/instance/{instance_id}/upload
Content-Type: multipart/form-data
```

Upload a file to the instance.



## Path Parameters

- InstanceId (required)

## Response Body

- 200: Successful Response
- 422: Validation Error

## Examples

```shell
curl -X POST https://api.scrapybara.com/v1/instance/instance_id/upload \
     -H "x-api-key: " \
     -H "Content-Type: multipart/form-data" \
     -F file=@ \
     -F path="path"
```

```shell
curl -X POST https://api.scrapybara.com/v1/instance/:instance_id/upload \
     -H "x-api-key: " \
     -H "Content-Type: multipart/form-data" \
     -F file=@ \
     -F path="string"
```

# Stop instance

```http
POST https://api.scrapybara.com/v1/instance/{instance_id}/stop
```



## Path Parameters

- InstanceId (required)

## Response Body

- 200: Successful Response
- 422: Validation Error

## Examples

```shell
curl -X POST https://api.scrapybara.com/v1/instance/instance_id/stop \
     -H "x-api-key: "
```

```shell
curl -X POST https://api.scrapybara.com/v1/instance/:instance_id/stop \
     -H "x-api-key: "
```

# Pause instance

```http
POST https://api.scrapybara.com/v1/instance/{instance_id}/pause
```



## Path Parameters

- InstanceId (required)

## Response Body

- 200: Successful Response
- 422: Validation Error

## Examples

```shell
curl -X POST https://api.scrapybara.com/v1/instance/instance_id/pause \
     -H "x-api-key: "
```

```shell
curl -X POST https://api.scrapybara.com/v1/instance/:instance_id/pause \
     -H "x-api-key: "
```

# Resume instance

```http
POST https://api.scrapybara.com/v1/instance/{instance_id}/resume
```



## Path Parameters

- InstanceId (required)

## Query Parameters

- TimeoutHours (optional)

## Response Body

- 200: Successful Response
- 422: Validation Error

## Examples

```shell
curl -X POST https://api.scrapybara.com/v1/instance/instance_id/resume \
     -H "x-api-key: "
```

```shell
curl -X POST "https://api.scrapybara.com/v1/instance/:instance_id/resume?timeout_hours=1" \
     -H "x-api-key: "
```

# Start browser

```http
POST https://api.scrapybara.com/v1/instance/{instance_id}/browser/start
```



## Path Parameters

- InstanceId (required)

## Response Body

- 200: Successful Response
- 422: Validation Error

## Examples

```shell
curl -X POST https://api.scrapybara.com/v1/instance/instance_id/browser/start \
     -H "x-api-key: "
```

```shell
curl -X POST https://api.scrapybara.com/v1/instance/:instance_id/browser/start \
     -H "x-api-key: "
```

# Get CDP URL

```http
GET https://api.scrapybara.com/v1/instance/{instance_id}/browser/cdp_url
```



## Path Parameters

- InstanceId (required)

## Response Body

- 200: Successful Response
- 422: Validation Error

## Examples

```shell
curl https://api.scrapybara.com/v1/instance/instance_id/browser/cdp_url \
     -H "x-api-key: "
```

```shell
curl https://api.scrapybara.com/v1/instance/:instance_id/browser/cdp_url \
     -H "x-api-key: "
```

# Get current URL

```http
GET https://api.scrapybara.com/v1/instance/{instance_id}/browser/current_url
```



## Path Parameters

- InstanceId (required)

## Response Body

- 200: Successful Response
- 422: Validation Error

## Examples

```shell
curl https://api.scrapybara.com/v1/instance/instance_id/browser/current_url \
     -H "x-api-key: "
```

```shell
curl https://api.scrapybara.com/v1/instance/:instance_id/browser/current_url \
     -H "x-api-key: "
```

# Save browser authentication state

```http
POST https://api.scrapybara.com/v1/instance/{instance_id}/browser/save_auth
```



## Path Parameters

- InstanceId (required)

## Query Parameters

- Name (optional)

## Response Body

- 200: Successful Response
- 422: Validation Error

## Examples

```shell
curl -X POST https://api.scrapybara.com/v1/instance/instance_id/browser/save_auth \
     -H "x-api-key: "
```

```shell
curl -X POST "https://api.scrapybara.com/v1/instance/:instance_id/browser/save_auth?name=string" \
     -H "x-api-key: "
```

# Modify browser authentication state

```http
POST https://api.scrapybara.com/v1/instance/{instance_id}/browser/modify_auth
```



## Path Parameters

- InstanceId (required)

## Query Parameters

- AuthStateId (required)
- Name (optional)

## Response Body

- 200: Successful Response
- 422: Validation Error

## Examples

```shell
curl -X POST "https://api.scrapybara.com/v1/instance/instance_id/browser/modify_auth?auth_state_id=auth_state_id" \
     -H "x-api-key: "
```

```shell
curl -X POST "https://api.scrapybara.com/v1/instance/:instance_id/browser/modify_auth?auth_state_id=string&name=string" \
     -H "x-api-key: "
```

# Authenticate browser using saved state

```http
POST https://api.scrapybara.com/v1/instance/{instance_id}/browser/authenticate
```



## Path Parameters

- InstanceId (required)

## Query Parameters

- AuthStateId (required)

## Response Body

- 200: Successful Response
- 422: Validation Error

## Examples

```shell
curl -X POST "https://api.scrapybara.com/v1/instance/instance_id/browser/authenticate?auth_state_id=auth_state_id" \
     -H "x-api-key: "
```

```shell
curl -X POST "https://api.scrapybara.com/v1/instance/:instance_id/browser/authenticate?auth_state_id=string" \
     -H "x-api-key: "
```

# Stop browser

```http
POST https://api.scrapybara.com/v1/instance/{instance_id}/browser/stop
```



## Path Parameters

- InstanceId (required)

## Response Body

- 200: Successful Response
- 422: Validation Error

## Examples

```shell
curl -X POST https://api.scrapybara.com/v1/instance/instance_id/browser/stop \
     -H "x-api-key: "
```

```shell
curl -X POST https://api.scrapybara.com/v1/instance/:instance_id/browser/stop \
     -H "x-api-key: "
```

# Execute code without notebook

```http
POST https://api.scrapybara.com/v1/instance/{instance_id}/code/execute
Content-Type: application/json
```



## Path Parameters

- InstanceId (required)

## Response Body

- 200: Successful Response
- 422: Validation Error

## Examples

```shell
curl -X POST https://api.scrapybara.com/v1/instance/instance_id/code/execute \
     -H "x-api-key: " \
     -H "Content-Type: application/json" \
     -d '{
  "code": "code"
}'
```

```shell
curl -X POST https://api.scrapybara.com/v1/instance/:instance_id/code/execute \
     -H "x-api-key: " \
     -H "Content-Type: application/json" \
     -d '{
  "code": "string"
}'
```

# List available notebook kernels

```http
GET https://api.scrapybara.com/v1/instance/{instance_id}/notebook/kernels
```



## Path Parameters

- InstanceId (required)

## Response Body

- 200: Successful Response
- 422: Validation Error

## Examples

```shell
curl https://api.scrapybara.com/v1/instance/instance_id/notebook/kernels \
     -H "x-api-key: "
```

```shell
curl https://api.scrapybara.com/v1/instance/:instance_id/notebook/kernels \
     -H "x-api-key: "
```

# Create new notebook

```http
POST https://api.scrapybara.com/v1/instance/{instance_id}/notebook/create
Content-Type: application/json
```



## Path Parameters

- InstanceId (required)

## Response Body

- 200: Successful Response
- 422: Validation Error

## Examples

```shell
curl -X POST https://api.scrapybara.com/v1/instance/instance_id/notebook/create \
     -H "x-api-key: " \
     -H "Content-Type: application/json" \
     -d '{
  "name": "name"
}'
```

```shell
curl -X POST https://api.scrapybara.com/v1/instance/:instance_id/notebook/create \
     -H "x-api-key: " \
     -H "Content-Type: application/json" \
     -d '{
  "name": "string"
}'
```

# Get notebook by ID

```http
GET https://api.scrapybara.com/v1/instance/{instance_id}/notebook/{notebook_id}
```



## Path Parameters

- InstanceId (required)
- NotebookId (required)

## Response Body

- 200: Successful Response
- 422: Validation Error

## Examples

```shell
curl https://api.scrapybara.com/v1/instance/instance_id/notebook/notebook_id \
     -H "x-api-key: "
```

```shell
curl https://api.scrapybara.com/v1/instance/:instance_id/notebook/:notebook_id \
     -H "x-api-key: "
```

# Delete notebook

```http
POST https://api.scrapybara.com/v1/instance/{instance_id}/notebook/{notebook_id}/delete
```



## Path Parameters

- InstanceId (required)
- NotebookId (required)

## Response Body

- 200: Successful Response
- 422: Validation Error

## Examples

```shell
curl -X POST https://api.scrapybara.com/v1/instance/instance_id/notebook/notebook_id/delete \
     -H "x-api-key: "
```

```shell
curl -X POST https://api.scrapybara.com/v1/instance/:instance_id/notebook/:notebook_id/delete \
     -H "x-api-key: "
```

# Add cell to notebook

```http
POST https://api.scrapybara.com/v1/instance/{instance_id}/notebook/{notebook_id}/cell
Content-Type: application/json
```



## Path Parameters

- InstanceId (required)
- NotebookId (required)

## Response Body

- 200: Successful Response
- 422: Validation Error

## Examples

```shell
curl -X POST https://api.scrapybara.com/v1/instance/instance_id/notebook/notebook_id/cell \
     -H "x-api-key: " \
     -H "Content-Type: application/json" \
     -d '{
  "type": "code",
  "content": "content"
}'
```

```shell
curl -X POST https://api.scrapybara.com/v1/instance/:instance_id/notebook/:notebook_id/cell \
     -H "x-api-key: " \
     -H "Content-Type: application/json" \
     -d '{
  "type": "code",
  "content": "string"
}'
```

# Execute notebook cell

```http
POST https://api.scrapybara.com/v1/instance/{instance_id}/notebook/{notebook_id}/cell/{cell_id}/execute
Content-Type: application/json
```



## Path Parameters

- InstanceId (required)
- NotebookId (required)
- CellId (required)

## Response Body

- 200: Successful Response
- 422: Validation Error

## Examples

```shell
curl -X POST https://api.scrapybara.com/v1/instance/instance_id/notebook/notebook_id/cell/cell_id/execute \
     -H "x-api-key: " \
     -H "Content-Type: application/json" \
     -d '{}'
```

```shell
curl -X POST https://api.scrapybara.com/v1/instance/:instance_id/notebook/:notebook_id/cell/:cell_id/execute \
     -H "x-api-key: " \
     -H "Content-Type: application/json" \
     -d '{}'
```

# Execute all cells in notebook

```http
POST https://api.scrapybara.com/v1/instance/{instance_id}/notebook/{notebook_id}/execute
Content-Type: application/json
```



## Path Parameters

- InstanceId (required)
- NotebookId (required)

## Response Body

- 200: Successful Response
- 422: Validation Error

## Examples

```shell
curl -X POST https://api.scrapybara.com/v1/instance/instance_id/notebook/notebook_id/execute \
     -H "x-api-key: " \
     -H "Content-Type: application/json" \
     -d '{}'
```

```shell
curl -X POST https://api.scrapybara.com/v1/instance/:instance_id/notebook/:notebook_id/execute \
     -H "x-api-key: " \
     -H "Content-Type: application/json" \
     -d '{}'
```

# Get environment variables

```http
GET https://api.scrapybara.com/v1/instance/{instance_id}/env
```



## Path Parameters

- InstanceId (required)

## Response Body

- 200: Successful Response
- 422: Validation Error

## Examples

```shell
curl https://api.scrapybara.com/v1/instance/instance_id/env \
     -H "x-api-key: "
```

```shell
curl https://api.scrapybara.com/v1/instance/:instance_id/env \
     -H "x-api-key: "
```

# Set environment variables

```http
POST https://api.scrapybara.com/v1/instance/{instance_id}/env
Content-Type: application/json
```



## Path Parameters

- InstanceId (required)

## Response Body

- 200: Successful Response
- 422: Validation Error

## Examples

```shell
curl -X POST https://api.scrapybara.com/v1/instance/instance_id/env \
     -H "x-api-key: " \
     -H "Content-Type: application/json" \
     -d '{
  "variables": {
    "key": "value"
  }
}'
```

```shell
curl -X POST https://api.scrapybara.com/v1/instance/:instance_id/env \
     -H "x-api-key: " \
     -H "Content-Type: application/json" \
     -d '{
  "variables": {
    "string": "string"
  }
}'
```

# Delete environment variables

```http
POST https://api.scrapybara.com/v1/instance/{instance_id}/env/delete
Content-Type: application/json
```



## Path Parameters

- InstanceId (required)

## Response Body

- 200: Successful Response
- 422: Validation Error

## Examples

```shell
curl -X POST https://api.scrapybara.com/v1/instance/instance_id/env/delete \
     -H "x-api-key: " \
     -H "Content-Type: application/json" \
     -d '{
  "keys": [
    "keys"
  ]
}'
```

```shell
curl -X POST https://api.scrapybara.com/v1/instance/:instance_id/env/delete \
     -H "x-api-key: " \
     -H "Content-Type: application/json" \
     -d '{
  "keys": [
    "string"
  ]
}'
```

# Python SDK

[![pypi](https://img.shields.io/pypi/v/scrapybara)](https://pypi.python.org/pypi/scrapybara)


  
    View the Python SDK source code
  

  
    View the Scrapybara package on PyPI
  


The Scrapybara Python library provides convenient access to the Scrapybara API from Python.

## Installation

```sh
pip install scrapybara
```

## Reference

Please only refer to this documentation site for reference. The GitHub reference [here](https://github.com/scrapybara/scrapybara-python/blob/master/reference.md) is generated programmatically and incomplete.

## Usage

Instantiate and use the client with the following:

```python
from scrapybara import Scrapybara

client = Scrapybara(
    api_key="YOUR_API_KEY",
)
instance = client.start_ubuntu()
```

## Async Client

The SDK also exports an `async` client so that you can make non-blocking calls to our API.

```python
import asyncio

from scrapybara import AsyncScrapybara

client = AsyncScrapybara(
    api_key="YOUR_API_KEY",
)


async def main() -> None:
    await client.start_ubuntu()


asyncio.run(main())
```

## Exception Handling

When the API returns a non-success status code (4xx or 5xx response), a subclass of the following error
will be thrown.

```python
from scrapybara.core.api_error import ApiError

try:
    client.start_ubuntu(...)
except ApiError as e:
    print(e.status_code)
    print(e.body)
```

## Advanced

### Retries

The SDK is instrumented with automatic retries with exponential backoff. A request will be retried as long
as the request is deemed retriable and the number of retry attempts has not grown larger than the configured
retry limit (default: 2).

A request is deemed retriable when any of the following HTTP status codes is returned:

* [408](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/408) (Timeout)
* [429](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429) (Too Many Requests)
* [5XX](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/500) (Internal Server Errors)

Use the `max_retries` request option to configure this behavior.

```python
client.start_ubuntu(..., request_options={
    "max_retries": 1
})
```

### Timeouts

The SDK defaults to a 60 second timeout. You can configure this with a timeout option at the client or request level.

```python

from scrapybara import Scrapybara

client = Scrapybara(
    ...,
    timeout=20.0,
)


# Override timeout for a specific method
client.start_ubuntu(..., request_options={
    "timeout_in_seconds": 1
})
```

### Custom Client

You can override the `httpx` client to customize it for your use-case. Some common use-cases include support for proxies
and transports.

```python
import httpx
from scrapybara import Scrapybara

client = Scrapybara(
    ...,
    httpx_client=httpx.Client(
        proxies="http://my.test.proxy.example.com",
        transport=httpx.HTTPTransport(local_address="0.0.0.0"),
    ),
)
```

## Contributing

While we value open-source contributions to this SDK, this library is generated programmatically.
Additions made directly to this library would have to be moved over to our generation code,
otherwise they would be overwritten upon the next generated release. Feel free to open a PR as
a proof of concept, but know that we will not be able to merge it as-is. We suggest opening
an issue first to discuss with us!

On the other hand, contributions to the README are always very welcome!


# TypeScript SDK

[![npm shield](https://img.shields.io/npm/v/scrapybara)](https://www.npmjs.com/package/scrapybara)


  
    View the TypeScript SDK source code
  

  
    View the Scrapybara package on NPM
  


The Scrapybara TypeScript library provides convenient access to the Scrapybara API from TypeScript.

## Installation

```sh
npm i -s scrapybara
```

## Reference

Please only refer to this documentation site for reference. The GitHub reference [here](https://github.com/scrapybara/scrapybara-ts/blob/main/reference.md) is generated programmatically and incomplete.

## Usage

Instantiate and use the client with the following:

```typescript
import { ScrapybaraClient } from "scrapybara";

const client = new ScrapybaraClient({ apiKey: "YOUR_API_KEY" });
await client.startUbuntu();
```

## Request And Response Types

The SDK exports all request and response types as TypeScript interfaces. Simply import them with the
following namespace:

```typescript
import { Scrapybara } from "scrapybara";

const request: Scrapybara.ComputerRequest = {
    ...
};
```

## Exception Handling

When the API returns a non-success status code (4xx or 5xx response), a subclass of the following error
will be thrown.

```typescript
import { ScrapybaraError } from "scrapybara";

try {
    await client.startUbuntu(...);
} catch (err) {
    if (err instanceof ScrapybaraError) {
        console.log(err.statusCode);
        console.log(err.message);
        console.log(err.body);
    }
}
```

## Advanced

### Additional Headers

If you would like to send additional headers as part of the request, use the `headers` request option.

```typescript
const response = await client.startUbuntu(..., {
    headers: {
        'X-Custom-Header': 'custom value'
    }
});
```

### Retries

The SDK is instrumented with automatic retries with exponential backoff. A request will be retried as long
as the request is deemed retriable and the number of retry attempts has not grown larger than the configured
retry limit (default: 2).

A request is deemed retriable when any of the following HTTP status codes is returned:

* [408](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/408) (Timeout)
* [429](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429) (Too Many Requests)
* [5XX](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/500) (Internal Server Errors)

Use the `maxRetries` request option to configure this behavior.

```typescript
const response = await client.startUbuntu(..., {
    maxRetries: 0 // override maxRetries at the request level
});
```

### Timeouts

The SDK defaults to a 60 second timeout. Use the `timeoutInSeconds` option to configure this behavior.

```typescript
const response = await client.startUbuntu(..., {
    timeoutInSeconds: 30 // override timeout to 30s
});
```

### Aborting Requests

The SDK allows users to abort requests at any point by passing in an abort signal.

```typescript
const controller = new AbortController();
const response = await client.startUbuntu(..., {
    abortSignal: controller.signal
});
controller.abort(); // aborts the request
```

### Runtime Compatibility

The SDK defaults to `node-fetch` but will use the global fetch client if present. The SDK works in the following
runtimes:

* Node.js 18+
* Vercel
* Cloudflare Workers
* Deno v1.25+
* Bun 1.0+
* React Native

### Customizing Fetch Client

The SDK provides a way for your to customize the underlying HTTP client / Fetch function. If you're running in an
unsupported environment, this provides a way for you to break glass and ensure the SDK works.

```typescript
import { ScrapybaraClient } from "scrapybara";

const client = new ScrapybaraClient({
    ...
    fetcher: // provide your implementation here
});
```

## Contributing

While we value open-source contributions to this SDK, this library is generated programmatically.
Additions made directly to this library would have to be moved over to our generation code,
otherwise they would be overwritten upon the next generated release. Feel free to open a PR as
a proof of concept, but know that we will not be able to merge it as-is. We suggest opening
an issue first to discuss with us!

On the other hand, contributions to the README are always very welcome!


# Scrapybara Cookbook

> A collection of examples and guides for getting the most out of Scrapybara

## Web research and scraping


  } href="/cookbook/copycapy">
    Scrape and transform websites into capybara-themed versions with Scrapybara Act SDK and Playwright.

    


    `TypeScript` `Act SDK` `Playwright`
  

  } href="/cookbook/wide-research">
    Deep Research but wide. Scrape YC W25 companies and find the best way to contact each company in parallel batches.

    


    `Python` `Act SDK` `Structured Outputs`
  


## Personal assistant


  
    Full-stack web interface for testing computer use models.

    


    `TypeScript` `Act SDK` `Next.js`
  

  
    A command line interface for Scrapybara.

    


    `Python` `Act SDK`
  


## Other


  } href="/cookbook/dungeon-crawler">
    Computer-using agent that autonomously plays Dungeon Crawl Stone Soup (DCSS) with Scrapybara Act SDK.

    


    `Python` `Act SDK`
  



# CopyCapy

> Scrape and transform websites into capybara-themed versions with Scrapybara Act SDK and Playwright.


  Detailed explanation coming soon!


CopyCapy

## Features

* HTML + CSS + image scraping with Playwright
* Agentic capybara-themed code generation
* Single-file output with embedded CSS
* Support for dynamically-loaded content

## Prerequisites

* Node.js 18+
* pnpm
* Scrapybara API key (get one at [scrapybara.com](https://scrapybara.com))





  
    View the source code on GitHub
  



# Wide Research

> Deep Research but wide. Scrape YC W25 companies and find the best way to contact each company in parallel batches.


  Detailed explanation coming soon!