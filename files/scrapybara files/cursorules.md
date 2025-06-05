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
- Prefer bash commands over GUI interactions for launching app