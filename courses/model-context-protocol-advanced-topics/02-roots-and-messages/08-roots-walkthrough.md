# Roots walkthrough

> Source: https://anthropic.skilljar.com/model-context-protocol-advanced-topics/295839

/* Root color variables */
:root {
  /* Default text color */
  --color-text-default: #191919;
  --font-serif: "Copernicus", Georgia, serif;

  /* Slate color system */
  --color-slate-50: #faf9f6; /* Ivory Light */
  --color-slate-150: #f0eee6; /* Ivory Medium */
  --color-slate-200: #e5e2d9; /* Ivory Dark */
  --color-slate-300: #d1cfc5; /* Cloud Light */
  --color-slate-400: #b8b5a6; /* Cloud Medium */
  --color-slate-500: #9a9788; /* Cloud Dark */
  --color-slate-600: #7c7968; /* Slate Light */
  --color-slate-700: #5e5b4e; /* Slate Medium */
  --color-slate-950: #2c2b25; /* Slate Dark */
}

#lesson-main {
  padding-left: 20px !important;
  padding-right: 20px !important;
}

#tutorial-container {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 10px;
  height: 80vh;
}

#tutorial-container .accordion-content-inner li {
  line-height: 1.5;
  font-size: 16px !important;
  color: var(--color-slate-700);
  font-weight: normal;
  text-align: left;
  word-wrap: break-word;
  white-space: normal;
  font-family: var(--font-serif) !important;
}

/* Editor Container Layout */
#tutorial-container .editor-container {
  display: flex;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--color-slate-300);
  background: var(--color-slate-50);
  min-width: 0;
}

#tutorial-container .editor-main {
  flex: 1;
  display: flex;
  flex-direction: column;
}

/* File Explorer Styles - keeping code editor font */
#tutorial-container .file-explorer {
  width: 15%;
  min-width: 180px;
  max-width: 200px;
  background: var(--color-slate-150);
  flex-shrink: 0;
  border-right: 1px solid var(--color-slate-200);
  font-family: "Consolas", "Monaco", "Courier New", monospace;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

#tutorial-container .file-explorer-header {
  padding: 13px 16px 11px 16px;
  background: var(--color-slate-200);
  border-bottom: 1px solid var(--color-slate-300);
  flex-shrink: 0;
}

#tutorial-container .file-explorer-header h3 {
  margin: 0;
  font-size: 11px !important;
  color: var(--color-slate-700);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-family: var(--font-serif);
  line-height: 100%;
}

#tutorial-container .file-tree {
  padding: 8px 0;
  overflow-y: auto;
  flex: 1;
}

#tutorial-container .file-tree-item {
  user-select: none;
  cursor: pointer;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

#tutorial-container .file-tree-file {
  padding: 2px 8px;
  display: flex;
  align-items: center;
  gap: 4px;
  color: var(--color-slate-700);
  font-size: 12px;
  height: 22px;
  line-height: 22px;
}

#tutorial-container .file-tree-file:hover {
  background: var(--color-slate-200);
  cursor: pointer;
}

#tutorial-container .file-tree-file.active {
  background: var(--color-slate-300);
  color: var(--color-text-default);
}

#tutorial-container .folder-header {
  padding: 2px 8px;
  display: flex;
  align-items: center;
  gap: 4px;
  color: var(--color-slate-700);
  font-size: 12px;
  height: 22px;
  line-height: 22px;
}

#tutorial-container .folder-header:hover {
  background: var(--color-slate-200);
  cursor: pointer;
}

#tutorial-container .file-icon,
#tutorial-container .folder-icon {
  font-size: 14px;
  line-height: 1;
  flex-shrink: 0;
  opacity: 0.8;
}

#tutorial-container .file-name,
#tutorial-container .folder-name {
  overflow: hidden;
  text-overflow: ellipsis;
}

#tutorial-container .tutorial-nav {
  background: var(--color-slate-150);
  padding: 20px;
  border-radius: 8px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  font-family: var(--font-serif);
}

#tutorial-container .tutorial-nav h3 {
  margin-top: 0;
  color: var(--color-text-default) !important;
  font-family: var(--font-serif);
  font-size: 18px !important;
}

#tutorial-container #accordion-container {
  flex: 1;
  overflow-y: auto;
  margin-bottom: 20px;
  scroll-behavior: smooth;
}

#tutorial-container .accordion-item {
  margin-bottom: 8px;
  border-radius: 4px;
  background: var(--color-slate-200);
  position: relative;
  z-index: 1;
  transition: margin-bottom 0.3s ease;
}

#tutorial-container .accordion-button {
  display: block;
  width: 100%;
  padding: 12px 40px 12px 16px;
  background: transparent;
  color: var(--color-text-default);
  border: none;
  cursor: pointer;
  text-align: left;
  font-size: 18px;
  transition: background 0.2s;
  position: relative;
  z-index: 2;
  font-family: var(--font-serif);
  margin-bottom: 0;
}

#tutorial-container .accordion-button::after {
  content: "";
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  width: 0;
  height: 0;
  border-left: 6px solid var(--color-text-default);
  border-top: 4px solid transparent;
  border-bottom: 4px solid transparent;
  transition: transform 0.2s;
}

#tutorial-container .accordion-item.expanded .accordion-button::after {
  transform: translateY(-50%) rotate(90deg);
}

#tutorial-container .accordion-button:hover {
  background: var(--color-slate-300);
}

#tutorial-container .accordion-item.active .accordion-button {
  background: var(--color-slate-400);
}

#tutorial-container .accordion-item.expanded {
  margin-bottom: 16px;
  z-index: 10;
}

#tutorial-container .accordion-content {
  display: none;
  overflow: hidden;
  background: var(--color-slate-50);
  position: relative;
  z-index: 1;
  border-radius: 0 0 4px 4px;
}

#tutorial-container .accordion-item.expanded .accordion-content {
  display: block;
  overflow-y: auto;
  min-height: 60px;
  animation: accordionOpen 0.3s ease-out;
}

@keyframes accordionOpen {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

#tutorial-container .accordion-content-inner {
  padding: 16px;
  font-size: 13px;
  line-height: 1.5;
  color: var(--color-slate-700);
  display: block;
  box-sizing: border-box;
  word-wrap: break-word;
  white-space: normal;
  text-align: left;
  font-family: var(--font-serif);
}

#tutorial-container .accordion-content-inner p {
  margin: 0 0 12px 0;
  display: block;
  line-height: 1.5;
  font-size: 16px !important;
  color: var(--color-slate-700);
  font-weight: normal;
  text-align: left;
  word-wrap: break-word;
  white-space: normal;
  font-family: var(--font-serif) !important;
}

#tutorial-container .accordion-content-inner p:last-child {
  margin-bottom: 0;
}

#tutorial-container .accordion-content-inner strong {
  color: var(--color-text-default);
  font-weight: bold;
}

#tutorial-container .accordion-content-inner code {
  background: var(--color-slate-200);
  padding: 2px 4px;
  border-radius: 3px;
  font-family: "Consolas", "Monaco", monospace;
  color: var(--color-slate-950);
  display: inline;
  font-size: 12px;
}

/* File tabs - keeping code editor font */
#tutorial-container .file-tabs {
  background: var(--color-slate-150);
  padding: 0;
  display: flex;
  border-bottom: 1px solid var(--color-slate-300);
  height: 35px;
  overflow-x: auto;
  overflow-y: hidden;
}

#tutorial-container .file-tab {
  padding: 0 12px 0 16px;
  background: transparent;
  color: var(--color-slate-600);
  border: none;
  cursor: pointer;
  font-size: 13px;
  border-right: 1px solid var(--color-slate-200);
  display: flex;
  align-items: center;
  white-space: nowrap;
  min-width: fit-content;
  gap: 8px;
  position: relative;
  font-family: "Consolas", "Monaco", "Courier New", monospace;
}

#tutorial-container .file-tab:hover {
  color: var(--color-slate-700);
}

#tutorial-container .file-tab.active {
  background: var(--color-slate-50);
  color: var(--color-text-default);
  border-right-color: var(--color-slate-50);
}

#tutorial-container .file-tab-text {
  pointer-events: none;
}

#tutorial-container .file-tab-close {
  opacity: 0;
  font-size: 18px;
  line-height: 1;
  padding: 2px 4px;
  border-radius: 3px;
  margin-left: 4px;
  transition: opacity 0.1s;
}

#tutorial-container .file-tab:hover .file-tab-close {
  opacity: 0.5;
}

#tutorial-container .file-tab-close:hover {
  opacity: 1 !important;
  background: var(--color-slate-300);
}

#tutorial-container #editor {
  height: calc(100% - 35px);
  background: var(--color-slate-50);
}

/* Empty state when no files are open */
#tutorial-container #editor-empty-state {
  height: calc(100% - 35px);
  background: var(--color-slate-50);
  display: none;
  align-items: center;
  justify-content: center;
  text-align: center;
}

#tutorial-container .empty-state-content {
  color: var(--color-slate-500);
  font-size: 14px;
  font-family: var(--font-serif);
}

#tutorial-container .empty-state-content p {
  margin: 0;
  padding: 4px 0;
}

#tutorial-container .empty-state-hint {
  font-size: 12px;
  color: var(--color-slate-400);
}

#tutorial-container .tutorial-highlight {
  background: rgba(184, 181, 166, 0.6) !important;
  border-left: 2px solid var(--color-slate-500) !important;
}

/* Navigation buttons */
#tutorial-container .tutorial-nav-buttons {
  display: flex;
  gap: 10px;
  margin-top: auto;
  padding-top: 10px;
  border-top: 1px solid var(--color-slate-300);
}

#tutorial-container .nav-button {
  flex: 1;
  padding: 10px 16px;
  background: var(--color-slate-700);
  color: var(--color-slate-50);
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.2s;
  font-family: var(--font-serif);
}

#tutorial-container .nav-button:hover:not(:disabled) {
  background: var(--color-slate-600);
}

#tutorial-container .nav-button:disabled {
  background: var(--color-slate-300);
  color: var(--color-slate-500);
  cursor: not-allowed;
}

/* Tour/Spotlight Styles */
.tour-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 9998;
  pointer-events: none;
  transition: opacity 0.3s ease;
}

.tour-overlay.active {
  pointer-events: auto;
}

.tour-spotlight {
  position: absolute;
  border-radius: 8px;
  box-shadow: 0 0 0 9999px rgba(0, 0, 0, 0.6) !important;
  transition: all 0.3s ease;
  pointer-events: auto;
  z-index: 9999;
}

.tour-tooltip {
  position: absolute;
  background: var(--color-slate-50);
  border: 1px solid var(--color-slate-300);
  border-radius: 8px;
  padding: 20px;
  max-width: 320px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  z-index: 10000;
  font-family: var(--font-serif);
  opacity: 0;
  transform: translateY(10px);
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.tour-tooltip.show {
  opacity: 1;
  transform: translateY(0);
}

.tour-tooltip h3 {
  margin: 0 0 8px 0;
  font-size: 16px;
  color: var(--color-text-default);
}

.tour-tooltip p {
  margin: 0 0 16px 0;
  font-size: 14px;
  line-height: 1.5;
  color: var(--color-slate-700);
}

.tour-tooltip-buttons {
  display: flex;
  gap: 8px;
  margin-top: 12px;
}

.tour-button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  font-size: 13px;
  font-family: var(--font-serif);
  cursor: pointer;
  transition: background 0.2s;
}

.tour-button-primary {
  background: var(--color-slate-700);
  color: var(--color-slate-50);
}

.tour-button-primary:hover {
  background: var(--color-slate-600);
}

.tour-button-secondary {
  background: var(--color-slate-200);
  color: var(--color-slate-700);
}

.tour-button-secondary:hover {
  background: var(--color-slate-300);
}

.tour-progress {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-bottom: 8px;
  font-size: 12px;
  color: var(--color-slate-500);
}

.tour-progress-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--color-slate-300);
  transition: background 0.2s;
}

.tour-progress-dot.active {
  background: var(--color-slate-700);
}

/* Tour trigger button */
.tour-trigger {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: var(--color-slate-700);
  color: var(--color-slate-50);
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  transition: transform 0.2s, background 0.2s;
  z-index: 1000;
}

.tour-trigger:hover {
  transform: scale(1.1);
  background: var(--color-slate-600);
}

.tour-trigger.pulse {
  animation: tourPulse 2s infinite;
}

@keyframes tourPulse {
  0% {
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2), 0 0 0 0 rgba(124, 121, 104, 0.4);
  }
  70% {
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2), 0 0 0 15px rgba(124, 121, 104, 0);
  }
  100% {
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2), 0 0 0 0 rgba(124, 121, 104, 0);
  }
}

/* Ensure tour elements work well with existing layout */
#tutorial-container.tour-active {
  position: relative;
}

/* Mobile styles */
@media (max-width: 768px) {
  #tutorial-container .file-explorer {
    display: none;
  }

  #tutorial-container {
    grid-template-columns: 1fr;
  }

  /* Hide tutorial name on mobile */
  #tutorial-container #tutorial-name {
    display: none;
  }

  /* Reduce padding on tutorial nav */
  #tutorial-container .tutorial-nav {
    padding: 12px;
    max-height: 40vh;
  }

  /* Remove margin from nav buttons container */
  #tutorial-container .tutorial-nav-buttons {
    margin-top: 0;
    padding-top: 8px;
    border-top: none;
  }

  /* Reduce height of nav buttons */
  #tutorial-container .nav-button {
    padding: 6px 12px;
    margin-bottom: 0;
    font-size: 13px;
  }

  /* Reduce accordion container margin */
  #tutorial-container #accordion-container {
    margin-bottom: 10px;
  }

  #tutorial-container .accordion-button {
    padding: 8px 10px 8px 16px;
  }

  #lesson-main {
    padding-left: 0px !important;
    padding-right: 0px !important;
  }

  /* Tour adjustments for mobile */
  .tour-tooltip {
    max-width: 280px;
    padding: 16px;
    margin: 0 10px;
  }

  .tour-trigger {
    bottom: 16px;
    right: 16px;
    width: 40px;
    height: 40px;
    font-size: 18px;
  }
}

  


      
      
        
      
        
        
          
        
          📄
          __init__.py
        
      
        
          📄
          chat.py
        
      
        
          📄
          claude.py
        
      
        
          📄
          cli_chat.py
        
      
        
          📄
          cli.py
        
      
        
          📄
          tools.py
        
      
        
          📄
          utils.py
        
      
        
          📄
          video_converter.py
        
      
        
      
    
        
          📄
          .env.example
        
      
        
          📄
          .gitignore
        
      
        
          📄
          main.py
        
      
        
          📄
          mcp_client.py
        
      
        
          📄
          mcp_server.py
        
      
        
          📄
          pyproject.toml
        
      
        
          📄
          README.md
        
      
      
    

main.py×
2223242526272829303132333435363738(    "Error:     ANTHROPIC_API_KEY     cannot be empty.     Update .env")async def main():    claude_service =     Claude    (model=claude_model)    # Get root     directories from     command line arguments    root_paths = sys.argv    [1:]    if not root_paths:        print("Usage: uv         run main.py         <root1>         [root2] ...")        print("Example:         uv run main.py /        path/to/videos /        another/path")        sys.exit(1)    clients = {}    async with     AsyncExitStack() as 


// Data from advanced_mcp/roots.js
const files = {
  ".env.example": `CLAUDE_MODEL="claude-sonnet-4-0"
ANTHROPIC_API_KEY=""`,

  ".gitignore": `.env
__pycache__
.venv
.DS_Store`,

  "README.md": `# MCP Chat with File System Access

MCP Chat is a command-line interface application that enables interactive chat capabilities with AI models through the Anthropic API. The application supports file system operations with controlled access to specified directories, video conversion capabilities, and extensible tool integrations via the MCP (Model Control Protocol) architecture.

## Prerequisites

- Python 3.10+
- Anthropic API Key
- FFmpeg (for video conversion features)

## Setup

_You must have FFmpeg already installed to convert a video file_. To install FFmpeg on MacOS run:

\`\`\`
brew install ffmpeg
\`\`\`

### Step 1: Configure the environment variables

1. Copy the \`.env.example\` file to create a new \`.env\` file:

\`\`\`bash
cp .env.example .env
\`\`\`

2. Edit the \`.env\` file and set your environment variables:

\`\`\`
CLAUDE_MODEL="claude-sonnet-4-0"  # Or your preferred Claude model
ANTHROPIC_API_KEY=""  # Enter your Anthropic API secret key
\`\`\`

### Step 2: Install dependencies

#### Setup with uv

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver.

1. Install uv, if not already installed:

\`\`\`bash
pip install uv
\`\`\`

2. Install dependencies:

\`\`\`bash
uv sync
\`\`\`

3. Run the project

When running the project, you must specify one or more root directories that the MCP server will have access to. Only files and directories within these roots can be accessed by the server.

\`\`\`bash
uv run main.py <root1> [root2] [root3] ...
\`\`\`

Examples:

\`\`\`bash
# Single directory
uv run main.py /path/to/videos

# Multiple directories
uv run main.py /home/user/videos /mnt/storage/media ~/Documents

# Current directory
uv run main.py .
\`\`\`

## Features

### File System Access

The server can only access files and directories within the specified root paths. This provides security by limiting file system access to approved locations.

### Available Tools

- **list_roots**: List all accessible root directories
- **read_dir**: Read contents of a directory (must be within a root)
- **convert_video**: Convert MP4 videos to other formats (avi, mov, webm, mkv, gif)

### Video Conversion

The video conversion tool uses FFmpeg to convert MP4 files to various formats:

- Standard video formats: AVI, MOV, WebM, MKV
- GIF conversion with optimized settings
- Medium quality preset for balanced file size and quality
`,

  "core/__init__.py": ``,

  "core/chat.py": `from core.claude import Claude
from mcp_client import MCPClient
from core.tools import ToolManager
from anthropic.types import MessageParam


class Chat:
    def __init__(self, claude_service: Claude, clients: dict[str, MCPClient]):
        self.claude_service: Claude = claude_service
        self.clients: dict[str, MCPClient] = clients
        self.messages: list[MessageParam] = []

    async def _process_query(self, query: str):
        self.messages.append({"role": "user", "content": query})

    async def run(
        self,
        query: str,
        stream: bool = False,
        on_event=None,
    ) -> str:
        final_text_response = ""

        await self._process_query(query)

        while True:
            if stream and on_event:
                response = await self.claude_service.chat_stream(
                    messages=self.messages,
                    tools=await ToolManager.get_all_tools(self.clients),
                    on_event=on_event,
                )
            else:
                response = await self.claude_service.chat(
                    messages=self.messages,
                    tools=await ToolManager.get_all_tools(self.clients),
                )

            self.claude_service.add_assistant_message(self.messages, response)

            if response.stop_reason == "tool_use":
                if not stream:
                    print(self.claude_service.text_from_message(response))
                tool_result_parts = await ToolManager.execute_tool_requests(
                    self.clients, response
                )

                self.claude_service.add_user_message(
                    self.messages, tool_result_parts
                )
            else:
                final_text_response = self.claude_service.text_from_message(
                    response
                )
                break

        return final_text_response
`,

  "core/claude.py": `from anthropic import AsyncAnthropic
from anthropic.types import Message


class Claude:
    def __init__(self, model: str):
        self.client = AsyncAnthropic()
        self.model = model

    def add_user_message(self, messages: list, message):
        user_message = {
            "role": "user",
            "content": message.content
            if isinstance(message, Message)
            else message,
        }
        messages.append(user_message)

    def add_assistant_message(self, messages: list, message):
        assistant_message = {
            "role": "assistant",
            "content": message.content
            if isinstance(message, Message)
            else message,
        }
        messages.append(assistant_message)

    def text_from_message(self, message: Message):
        return "\n".join(
            [block.text for block in message.content if block.type == "text"]
        )

    async def chat(
        self,
        messages,
        system=None,
        temperature=1.0,
        stop_sequences=[],
        tools=None,
        thinking=False,
        thinking_budget=1024,
    ) -> Message:
        params = {
            "model": self.model,
            "max_tokens": 8000,
            "messages": messages,
            "temperature": temperature,
            "stop_sequences": stop_sequences,
        }

        if thinking:
            params["thinking"] = {
                "type": "enabled",
                "budget_tokens": thinking_budget,
            }

        if tools:
            params["tools"] = tools

        if system:
            params["system"] = system

        message = await self.client.messages.create(**params)
        return message

    async def chat_stream(
        self,
        messages,
        system=None,
        temperature=1.0,
        stop_sequences=[],
        tools=None,
        thinking=False,
        thinking_budget=1024,
        on_event=None,
    ) -> Message:
        params = {
            "model": self.model,
            "max_tokens": 8000,
            "messages": messages,
            "temperature": temperature,
            "stop_sequences": stop_sequences,
        }

        if thinking:
            params["thinking"] = {
                "type": "enabled",
                "budget_tokens": thinking_budget,
            }

        if tools:
            params["tools"] = tools

        if system:
            params["system"] = system

        async with self.client.messages.stream(**params) as stream:
            if on_event:
                async for event in stream:
                    await on_event(event)
            else:
                async for event in stream:
                    pass

        return await stream.get_final_message()
`,

  "core/cli.py": `from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
from prompt_toolkit.history import InMemoryHistory
from core.cli_chat import CliChat
import json
from pyboxen import boxen


class CliApp:
    def __init__(self, agent: CliChat):
        self.agent = agent
        self.history = InMemoryHistory()
        self.session = PromptSession(
            history=self.history,
            style=Style.from_dict(
                {
                    "prompt": "#aaaaaa",
                    "completion-menu.completion": "bg:#222222 #ffffff",
                    "completion-menu.completion.current": "bg:#444444 #ffffff",
                }
            ),
            complete_while_typing=True,
            complete_in_thread=True,
        )

    async def initialize(self):
        pass

    async def run(self):
        while True:
            try:
                user_input = await self.session.prompt_async("> ")
                if not user_input.strip():
                    continue

                print()

                tool_calls = {}
                response_text = ""

                async def handle_event(event):
                    nonlocal response_text
                    if hasattr(event, "type"):
                        if event.type == "content_block_delta":
                            if hasattr(event, "delta") and hasattr(
                                event.delta, "type"
                            ):
                                if event.delta.type == "text_delta":
                                    response_text += event.delta.text
                                    print(event.delta.text, end="", flush=True)
                                elif event.delta.type == "input_json_delta":
                                    # Track tool call arguments as they stream
                                    index = event.index
                                    if index not in tool_calls:
                                        tool_calls[index] = {
                                            "name": "",
                                            "args": "",
                                        }
                                    tool_calls[index]["args"] += (
                                        event.delta.partial_json
                                    )
                        elif event.type == "content_block_start":
                            if hasattr(event, "content_block") and hasattr(
                                event.content_block, "type"
                            ):
                                if event.content_block.type == "tool_use":
                                    print()  # New line before tool call
                                    # Store tool name but don't print yet
                                    index = getattr(event, "index", 0)
                                    if index not in tool_calls:
                                        tool_calls[index] = {
                                            "name": "",
                                            "args": "",
                                        }
                                    tool_calls[index]["name"] = (
                                        event.content_block.name
                                    )
                        elif event.type == "content_block_stop":
                            if event.index in tool_calls:
                                tool_name = tool_calls[event.index]["name"]
                                args_json = tool_calls[event.index]["args"]

                                try:
                                    parsed_args = json.loads(args_json)
                                    formatted_args = json.dumps(
                                        parsed_args, indent=2
                                    )
                                    tool_content = f"🔧 {tool_name}\n\nArguments:\n{formatted_args}"
                                except (
                                    json.JSONDecodeError,
                                    TypeError,
                                    ValueError,
                                ):
                                    tool_content = f"🔧 {tool_name}\n\nArguments: {args_json}"

                                tool_box = boxen(
                                    tool_content,
                                    title="Tool Call",
                                    style="rounded",
                                    color="blue",
                                    padding=0,
                                )
                                print(tool_box)
                                del tool_calls[event.index]

                await self.agent.run(
                    user_input, stream=True, on_event=handle_event
                )

                print()  # Add newline after everything

            except KeyboardInterrupt:
                break
`,

  "core/cli_chat.py": `from typing import List
from mcp.types import Prompt, PromptMessage
from anthropic.types import MessageParam

from core.chat import Chat
from core.claude import Claude
from mcp_client import MCPClient


class CliChat(Chat):
    def __init__(
        self,
        doc_client: MCPClient,
        clients: dict[str, MCPClient],
        claude_service: Claude,
    ):
        super().__init__(clients=clients, claude_service=claude_service)

        self.doc_client: MCPClient = doc_client

    async def list_prompts(self) -> list[Prompt]:
        return await self.doc_client.list_prompts()

    async def get_prompt(
        self, command: str, doc_id: str
    ) -> list[PromptMessage]:
        return await self.doc_client.get_prompt(command, {"doc_id": doc_id})

    async def _process_query(self, query: str):
        self.messages.append({"role": "user", "content": query})


def convert_prompt_message_to_message_param(
    prompt_message: "PromptMessage",
) -> MessageParam:
    role = "user" if prompt_message.role == "user" else "assistant"

    content = prompt_message.content

    # Check if content is a dict-like object with a "type" field
    if isinstance(content, dict) or hasattr(content, "__dict__"):
        content_type = (
            content.get("type", None)
            if isinstance(content, dict)
            else getattr(content, "type", None)
        )
        if content_type == "text":
            content_text = (
                content.get("text", "")
                if isinstance(content, dict)
                else getattr(content, "text", "")
            )
            return {"role": role, "content": content_text}

    if isinstance(content, list):
        text_blocks = []
        for item in content:
            # Check if item is a dict-like object with a "type" field
            if isinstance(item, dict) or hasattr(item, "__dict__"):
                item_type = (
                    item.get("type", None)
                    if isinstance(item, dict)
                    else getattr(item, "type", None)
                )
                if item_type == "text":
                    item_text = (
                        item.get("text", "")
                        if isinstance(item, dict)
                        else getattr(item, "text", "")
                    )
                    text_blocks.append({"type": "text", "text": item_text})

        if text_blocks:
            return {"role": role, "content": text_blocks}

    return {"role": role, "content": ""}


def convert_prompt_messages_to_message_params(
    prompt_messages: List[PromptMessage],
) -> List[MessageParam]:
    return [
        convert_prompt_message_to_message_param(msg) for msg in prompt_messages
    ]
`,

  "core/tools.py": `import json
from typing import Optional, Literal, List
from mcp.types import CallToolResult, Tool, TextContent
from mcp_client import MCPClient
from anthropic.types import Message, ToolResultBlockParam


class ToolManager:
    @classmethod
    async def get_all_tools(cls, clients: dict[str, MCPClient]) -> list[Tool]:
        """Gets all tools from the provided clients."""
        tools = []
        for client in clients.values():
            tool_models = await client.list_tools()
            tools += [
                {
                    "name": t.name,
                    "description": t.description,
                    "input_schema": t.inputSchema,
                }
                for t in tool_models
            ]
        return tools

    @classmethod
    async def _find_client_with_tool(
        cls, clients: list[MCPClient], tool_name: str
    ) -> Optional[MCPClient]:
        """Finds the first client that has the specified tool."""
        for client in clients:
            tools = await client.list_tools()
            tool = next((t for t in tools if t.name == tool_name), None)
            if tool:
                return client
        return None

    @classmethod
    def _build_tool_result_part(
        cls,
        tool_use_id: str,
        text: str,
        status: Literal["success"] | Literal["error"],
    ) -> ToolResultBlockParam:
        """Builds a tool result part dictionary."""
        return {
            "tool_use_id": tool_use_id,
            "type": "tool_result",
            "content": text,
            "is_error": status == "error",
        }

    @classmethod
    async def execute_tool_requests(
        cls, clients: dict[str, MCPClient], message: Message
    ) -> List[ToolResultBlockParam]:
        """Executes a list of tool requests against the provided clients."""
        tool_requests = [
            block for block in message.content if block.type == "tool_use"
        ]
        tool_result_blocks: list[ToolResultBlockParam] = []
        for tool_request in tool_requests:
            tool_use_id = tool_request.id
            tool_name = tool_request.name
            tool_input = tool_request.input

            client = await cls._find_client_with_tool(
                list(clients.values()), tool_name
            )

            if not client:
                tool_result_part = cls._build_tool_result_part(
                    tool_use_id, "Could not find that tool", "error"
                )
                tool_result_blocks.append(tool_result_part)
                continue

            tool_output = None
            try:
                tool_output: CallToolResult | None = await client.call_tool(
                    tool_name, tool_input
                )
                items = []
                if tool_output:
                    items = tool_output.content
                content_list = [
                    item.text for item in items if isinstance(item, TextContent)
                ]
                content_json = json.dumps(content_list)
                tool_result_part = cls._build_tool_result_part(
                    tool_use_id,
                    content_json,
                    "error"
                    if tool_output and tool_output.isError
                    else "success",
                )
            except Exception as e:
                error_message = f"Error executing tool '{tool_name}': {e}"
                print(error_message)
                tool_result_part = cls._build_tool_result_part(
                    tool_use_id,
                    json.dumps({"error": error_message}),
                    "error"
                    if tool_output and tool_output.isError
                    else "success",
                )

            tool_result_blocks.append(tool_result_part)
        return tool_result_blocks
`,

  "core/utils.py": `from pathlib import Path
from urllib.parse import unquote, urlparse


def file_url_to_path(file_url) -> Path:
    """Convert a file:// URL to a Path object."""
    url_str = str(file_url)
    parsed = urlparse(url_str)
    path = unquote(parsed.path)
    if len(path) > 2 and path[0] == "/" and path[2] == ":":
        path = path[1:]

    return Path(path)`,

  "core/video_converter.py": `import os
import asyncio
from pathlib import Path


class VideoConverter:
    """Handles video conversion operations using ffmpeg."""
    
    # Quality presets for video conversion
    QUALITY_PRESETS = {
        "low": {"crf": "28", "preset": "fast"},
        "medium": {"crf": "23", "preset": "medium"},
        "high": {"crf": "18", "preset": "slow"},
    }
    
    SUPPORTED_FORMATS = ["webm", "mkv", "avi", "mov", "gif"]
    
    @classmethod
    def validate_input(cls, input_path: str) -> Path:
        """Validate the input file exists and is an MP4."""
        input_file = Path(input_path)
        
        if not input_file.exists():
            raise ValueError(f"Input file not found: {input_path}")
        
        if not input_path.lower().endswith(".mp4"):
            raise ValueError("Input file must be an MP4 file")
            
        return input_file
    
    @classmethod
    def generate_output_path(cls, input_path: str, format: str) -> str:
        """Generate output path by replacing the file extension."""
        base_path = os.path.splitext(input_path)[0]
        return f"{base_path}.{format.lower()}"
    
    @classmethod
    def build_ffmpeg_command(cls, input_path: str, output_path: str, format: str) -> list:
        """Build the ffmpeg command based on format settings."""
        preset = cls.QUALITY_PRESETS["medium"]
        
        # Base command
        cmd = ["ffmpeg", "-i", input_path, "-y"]
        
        if format.lower() == "gif":
            # Special handling for GIF conversion
            cmd.extend([
                "-vf", "fps=15,scale=480:-1:flags=lanczos",
                "-c:v", "gif",
                output_path
            ])
        elif format.lower() in cls.SUPPORTED_FORMATS:
            # Standard video conversion
            cmd.extend([
                "-c:v", "libx264",
                "-preset", preset["preset"],
                "-crf", preset["crf"],
                "-c:a", "aac",
                "-b:a", "128k",
                output_path
            ])
        else:
            raise ValueError(f"Unsupported output format: {format}")
            
        return cmd
    
    @classmethod
    async def convert(cls, input_path: str, format: str) -> str:
        """
        Convert video file to specified format.
        Returns success message or raises an error.
        """
        # Validate input
        cls.validate_input(input_path)
        
        # Generate output path
        output_path = cls.generate_output_path(input_path, format)
        
        # Build ffmpeg command
        cmd = cls.build_ffmpeg_command(input_path, output_path, format)
        
        try:
            # Run ffmpeg asynchronously
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            _, stderr = await process.communicate()
            
            if process.returncode != 0:
                raise RuntimeError(f"FFmpeg conversion failed: {stderr.decode()}")
                
            return f"Successfully converted {input_path} to {output_path}"
            
        except FileNotFoundError:
            raise RuntimeError("FFmpeg not found. Please ensure ffmpeg is installed and in PATH")`,

  "main.py": `import asyncio
import sys
import os
from dotenv import load_dotenv
from contextlib import AsyncExitStack

from mcp_client import MCPClient
from core.claude import Claude

from core.cli_chat import CliChat
from core.cli import CliApp

load_dotenv()

# Anthropic Config
claude_model = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-0")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", "")


assert claude_model, "Error: CLAUDE_MODEL cannot be empty. Update .env"
assert anthropic_api_key, (
    "Error: ANTHROPIC_API_KEY cannot be empty. Update .env"
)


async def main():
    claude_service = Claude(model=claude_model)

    # Get root directories from command line arguments
    root_paths = sys.argv[1:]
    if not root_paths:
        print("Usage: uv run main.py <root1> [root2] ...")
        print("Example: uv run main.py /path/to/videos /another/path")
        sys.exit(1)

    clients = {}

    async with AsyncExitStack() as stack:
        # Create the MCP client with the provided root directories
        doc_client = await stack.enter_async_context(
            MCPClient(
                command="uv", args=["run", "mcp_server.py"], roots=root_paths
            )
        )
        clients["doc_client"] = doc_client

        chat = CliChat(
            doc_client=doc_client,
            clients=clients,
            claude_service=claude_service,
        )

        cli = CliApp(chat)
        await cli.initialize()
        await cli.run()


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(main())
`,

  "mcp_client.py": `from typing import Optional, Any
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
from mcp.types import Root, ListRootsResult, ErrorData
from mcp.shared.context import RequestContext
from pathlib import Path
from pydantic import FileUrl

import json
from pydantic import AnyUrl


class MCPClient:
    def __init__(
        self,
        command: str,
        args: list[str],
        env: Optional[dict] = None,
        roots: Optional[list[str]] = None,
    ):
        self._command = command
        self._args = args
        self._env = env
        self._roots = self._create_roots(roots) if roots else []
        self._session: Optional[ClientSession] = None
        self._exit_stack: AsyncExitStack = AsyncExitStack()

    def _create_roots(self, root_paths: list[str]) -> list[Root]:
        """Convert path strings to Root objects."""
        roots = []
        for path in root_paths:
            p = Path(path).resolve()
            file_url = FileUrl(f"file://{p}")
            roots.append(Root(uri=file_url, name=p.name or "Root"))
        return roots

    async def _handle_list_roots(
        self, context: RequestContext["ClientSession", None]
    ) -> ListRootsResult | ErrorData:
        """Callback for when server requests roots."""
        return ListRootsResult(roots=self._roots)

    async def connect(self):
        server_params = StdioServerParameters(
            command=self._command,
            args=self._args,
            env=self._env,
        )
        stdio_transport = await self._exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        _stdio, _write = stdio_transport
        self._session = await self._exit_stack.enter_async_context(
            ClientSession(
                _stdio,
                _write,
                list_roots_callback=self._handle_list_roots
                if self._roots
                else None,
            )
        )
        await self._session.initialize()

    def session(self) -> ClientSession:
        if self._session is None:
            raise ConnectionError(
                "Client session not initialized or cache not populated. Call connect_to_server first."
            )
        return self._session

    async def list_tools(self) -> list[types.Tool]:
        result = await self.session().list_tools()
        return result.tools

    async def call_tool(
        self, tool_name: str, tool_input
    ) -> types.CallToolResult | None:
        return await self.session().call_tool(tool_name, tool_input)

    async def list_prompts(self) -> list[types.Prompt]:
        result = await self.session().list_prompts()
        return result.prompts

    async def get_prompt(self, prompt_name, args: dict[str, str]):
        result = await self.session().get_prompt(prompt_name, args)
        return result.messages

    async def read_resource(self, uri: str) -> Any:
        result = await self.session().read_resource(AnyUrl(uri))
        resource = result.contents[0]

        if isinstance(resource, types.TextResourceContents):
            if resource.mimeType == "application/json":
                return json.loads(resource.text)

            return resource.text

    async def cleanup(self):
        await self._exit_stack.aclose()
        self._session = None

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.cleanup()
`,

  "mcp_server.py": `from pathlib import Path
from mcp.server.fastmcp import FastMCP
from pydantic import Field
from mcp.server.fastmcp import Context
from core.video_converter import VideoConverter
from core.utils import file_url_to_path

mcp = FastMCP("VidsMCP", log_level="ERROR")


async def is_path_allowed(requested_path: Path, ctx: Context) -> bool:
    roots_result = await ctx.session.list_roots()
    client_roots = roots_result.roots

    if not requested_path.exists():
        return False

    if requested_path.is_file():
        requested_path = requested_path.parent

    for root in client_roots:
        root_path = file_url_to_path(root.uri)
        try:
            requested_path.relative_to(root_path)
            return True
        except ValueError:
            continue

    return False


@mcp.tool()
async def convert_video(
    input_path: str = Field(description="Path to the input MP4 file"),
    format: str = Field(description="Output format (e.g. 'mov')"),
    *,
    ctx: Context,
):
    """Convert an MP4 video file to another format using ffmpeg"""
    input_file = VideoConverter.validate_input(input_path)

    # Ensure the input file is contained in a root
    if not await is_path_allowed(input_file, ctx):
        raise ValueError(f"Access to path is not allowed: {input_path}")

    return await VideoConverter.convert(input_path, format)


@mcp.tool()
async def list_roots(ctx: Context):
    """
    List all directories that are accessible to this server.
    These are the root directories where files can be read from or written to.
    """
    roots_result = await ctx.session.list_roots()
    client_roots = roots_result.roots

    return [file_url_to_path(root.uri) for root in client_roots]


@mcp.tool()
async def read_dir(
    path: str = Field(description="Path to a directory to read"),
    *,
    ctx: Context,
):
    """Read directory contents. Path must be within one of the client's roots."""
    requested_path = Path(path).resolve()

    if not await is_path_allowed(requested_path, ctx):
        raise ValueError("Error: can only read directories within a root")

    return [entry.name for entry in requested_path.iterdir()]


if __name__ == "__main__":
    mcp.run(transport="stdio")
`,

  "pyproject.toml": `[project]
name = "app"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "anthropic>=0.51.0",
    "mcp[cli]>=1.8.0",
    "prompt-toolkit>=3.0.51",
    "pyboxen>=1.3.0",
    "python-dotenv>=1.1.0",
]
`,
};

const tutorialTitle = "Understanding Roots";

const tutorialSteps = [
  {
    file: "main.py",
    line: 30,
    endLine: 30,
    title: "Defining roots",
    markdown: `Ideally, a user will dictate which files/folders can be accessed by the MCP server. 

This program is set up to accept a list of CLI arguments, which are interpretted as paths that the user wants to allow access to.

That list of paths is provided to the \`MCPClient\` down on lines 42.`,
  },
  {
    file: "mcp_client.py",
    line: 29,
    endLine: 36,
    title: "Creating root objects",
    markdown: `According to the MCP spec, all roots should have a URI that begins with \`file://\`. 
    
This function takes the list of paths of that the user provided and turns them into \`Root\` objects.`,
  },
  {
    file: "mcp_client.py",
    line: 38,
    endLine: 42,
    title: "Roots callback",
    markdown: `The client doesn't immediately provide the list of roots to the server. Instead, the server can make a request to the client at some future point in time. We make a callback that will be executed when the server requests the roots. The callback needs to return the list of roots inside of a \`ListRootsResult\` object.
    
This callback is passed into the ClientSession down on line 58.`,
  },
  {
    file: "mcp_server.py",
    line: 49,
    endLine: 58,
    title: "Using the roots",
    markdown: `On to the server. The server will use the roots in two scenarios: 
    
1. Whenever a tool attempts to access a file or folder
2. When a LLM (like Claude) needs to resolve a file or folder to a full path. Think of when a user says 'read the todos.txt file' - Claude needs to figure out where the text file is, and might do so by looking at the list of roots
    
To handle the second case, we can either define a tool that lists out the roots or inject them directly in a prompt.`,
  },
  {
    file: "mcp_server.py",
    line: 55,
    endLine: 55,
    title: "Accessing the roots",
    markdown: `Roots are accessed by calling \`ctx.session.list_roots()\`. 
    
This sends a message back to the client, which causes it to run the root-listing callback.`,
  },
  {
    file: "mcp_server.py",
    line: 11,
    endLine: 29,
    title: "Authorizing access",
    markdown: `Remember: the MCP SDK does not attempt to limit what files or folders your tools attempt to read! You must implement that check yourself.
    
Consider implementing a function like \`is_path_allowed\`, which will decide whether a path is accessible by comparing it to the list of roots.`,
  },
  {
    file: "mcp_server.py",
    line: 43,
    endLine: 44,
    title: "Authorizing access",
    markdown: `Once you've put an authorization function together - like \`is_path_allowed\` - use it throughout your tools to ensure the requested path is accessible.`,
  },
];


// Library code
function render(files, tutorialSteps) {
  let editor;
  let currentDecorations = [];

  // Build file tree structure from flat file list
  function buildFileTree(files) {
    const root = { name: "root", type: "folder", children: {} };

    Object.keys(files).forEach((filePath) => {
      const parts = filePath.split("/");
      let current = root;

      parts.forEach((part, index) => {
        if (index === parts.length - 1) {
          // It's a file
          current.children[part] = {
            name: part,
            type: "file",
            path: filePath,
            content: files[filePath],
          };
        } else {
          // It's a folder
          if (!current.children[part]) {
            current.children[part] = {
              name: part,
              type: "folder",
              children: {},
              expanded: true, // Start with folders expanded
            };
          }
          current = current.children[part];
        }
      });
    });

    return root;
  }

  // Render file tree as HTML
  function renderFileTree(node, level = 0) {
    if (node.type === "file") {
      return `
        <div class="file-tree-item file-tree-file" data-path="${
          node.path
        }" style="padding-left: ${level * 20}px">
          <span class="file-icon">📄</span>
          <span class="file-name">${node.name}</span>
        </div>
      `;
    }

    // It's a folder
    const children = Object.values(node.children)
      .sort((a, b) => {
        // Folders first, then files
        if (a.type !== b.type) return a.type === "folder" ? -1 : 1;
        return a.name.localeCompare(b.name);
      })
      .map((child) => renderFileTree(child, level + 1))
      .join("");

    // Skip rendering the root folder itself
    if (node.name === "root") {
      return children;
    }

    return `
      <div class="file-tree-item file-tree-folder ${
        node.expanded ? "expanded" : ""
      }" data-name="${node.name}">
        <div class="folder-header" style="padding-left: ${level * 20}px">
          <span class="folder-icon">${node.expanded ? "📂" : "📁"}</span>
          <span class="folder-name">${node.name}</span>
        </div>
        <div class="folder-children" style="display: ${
          node.expanded ? "block" : "none"
        }">
          ${children}
        </div>
      </div>
    `;
  }

  // Initialize Monaco Editor
  require.config({
    paths: {
      vs: "https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.44.0/min/vs",
    },
  });

  require(["vs/editor/editor.main"], function () {
    // Build and render file explorer
    const fileTree = buildFileTree(files);
    const fileExplorer = document.createElement("div");
    fileExplorer.id = "file-explorer";
    fileExplorer.className = "file-explorer";
    fileExplorer.innerHTML = `
      <div class="file-explorer-header">
        <h3>Files</h3>
      </div>
      <div class="file-tree">
        ${renderFileTree(fileTree)}
      </div>
    `;

    // Insert file explorer inside editor container
    const editorContainer = document.querySelector(".editor-container");
    editorContainer.insertBefore(fileExplorer, editorContainer.firstChild);

    // Track open tabs
    let openTabs = [];
    let activeTab = null;

    // Track current tutorial step
    let currentStepIndex = 0;

    // Function to create a file tab
    function createFileTab(filePath) {
      const tab = document.createElement("div");
      tab.className = "file-tab";
      tab.setAttribute("data-file", filePath);

      const tabText = document.createElement("span");
      tabText.className = "file-tab-text";
      tabText.textContent = filePath.split("/").pop();

      const closeBtn = document.createElement("span");
      closeBtn.className = "file-tab-close";
      closeBtn.innerHTML = "×";
      closeBtn.onclick = (e) => {
        e.stopPropagation();
        closeFileTab(filePath);
      };

      tab.appendChild(tabText);
      tab.appendChild(closeBtn);
      tab.onclick = () => switchFile(filePath);

      return tab;
    }

    // Function to open a file tab
    function openFileTab(filePath) {
      if (!openTabs.includes(filePath)) {
        openTabs.push(filePath);
        const fileTabsContainer = document.getElementById(
          "file-tabs-container"
        );
        const tab = createFileTab(filePath);
        fileTabsContainer.appendChild(tab);
      }
      setActiveTab(filePath);
      hideEmptyState();

      // Update active file in explorer
      document.querySelectorAll(".file-tree-file").forEach((f) => {
        f.classList.toggle("active", f.dataset.path === filePath);
      });

      // Scroll to file in tree
      scrollFileIntoView(filePath);
    }

    // Function to close a file tab
    function closeFileTab(filePath) {
      const index = openTabs.indexOf(filePath);
      if (index > -1) {
        openTabs.splice(index, 1);
        const tab = document.querySelector(
          `.file-tab[data-file="${filePath}"]`
        );
        if (tab) tab.remove();

        // If closing the active tab, switch to another open tab
        if (activeTab === filePath && openTabs.length > 0) {
          switchFile(openTabs[openTabs.length - 1]);
        } else if (openTabs.length === 0) {
          // No more open tabs, show empty state
          showEmptyState();
        }
      }
    }

    // Function to show empty state when no files are open
    function showEmptyState() {
      const editorElement = document.getElementById("editor");
      editorElement.style.display = "none";

      // Create or show empty state message
      let emptyState = document.getElementById("editor-empty-state");
      if (!emptyState) {
        emptyState = document.createElement("div");
        emptyState.id = "editor-empty-state";
        emptyState.innerHTML = `
          <div class="empty-state-content">
            <p>No file open</p>
            <p class="empty-state-hint">Open a file from the explorer or navigate through the tutorial steps</p>
          </div>
        `;
        editorElement.parentNode.appendChild(emptyState);
      }
      emptyState.style.display = "flex";
      activeTab = null;
    }

    // Function to hide empty state
    function hideEmptyState() {
      const editorElement = document.getElementById("editor");
      const emptyState = document.getElementById("editor-empty-state");

      editorElement.style.display = "block";
      if (emptyState) {
        emptyState.style.display = "none";
      }
    }

    // Function to set active tab
    function setActiveTab(filePath) {
      activeTab = filePath;
      document.querySelectorAll(".file-tab").forEach((tab) => {
        tab.classList.toggle(
          "active",
          tab.getAttribute("data-file") === filePath
        );
      });
    }

    // Function to scroll file into view in the file tree
    function scrollFileIntoView(filePath) {
      const fileElement = document.querySelector(
        `.file-tree-file[data-path="${filePath}"]`
      );
      if (fileElement) {
        const fileTree = document.querySelector(".file-tree");
        const fileTreeRect = fileTree.getBoundingClientRect();
        const fileElementRect = fileElement.getBoundingClientRect();

        // Check if file is outside the visible area
        if (
          fileElementRect.top < fileTreeRect.top ||
          fileElementRect.bottom > fileTreeRect.bottom
        ) {
          fileElement.scrollIntoView({
            behavior: "smooth",
            block: "center",
          });
        }
      }
    }

    // Initialize with first file from tutorial steps
    const firstTutorialFile = tutorialSteps[0]?.file;
    if (firstTutorialFile) {
      openFileTab(firstTutorialFile);
    }

    // Dynamically build accordion items
    const accordionContainer = document.getElementById("accordion-container");
    tutorialSteps.forEach((step, index) => {
      const accordionItem = document.createElement("div");
      accordionItem.className = "accordion-item";
      accordionItem.setAttribute("data-step", index);

      const accordionButton = document.createElement("button");
      accordionButton.className = "accordion-button";
      accordionButton.textContent = `${index + 1}. ${step.title}`;

      const accordionContent = document.createElement("div");
      accordionContent.className = "accordion-content";

      const accordionContentInner = document.createElement("div");
      accordionContentInner.className = "accordion-content-inner";

      accordionContent.appendChild(accordionContentInner);
      accordionItem.appendChild(accordionButton);
      accordionItem.appendChild(accordionContent);
      accordionContainer.appendChild(accordionItem);
    });

    // Create models for each file
    const models = {};
    const fileNames = Object.keys(files);
    fileNames.forEach((filename) => {
      // Detect language based on file extension
      const ext = filename.split(".").pop();
      let language = "plaintext";
      switch (ext) {
        case "py":
          language = "python";
          break;
        case "js":
          language = "javascript";
          break;
        case "ts":
          language = "typescript";
          break;
        case "java":
          language = "java";
          break;
        case "cpp":
        case "cc":
        case "cxx":
          language = "cpp";
          break;
        case "c":
          language = "c";
          break;
        case "cs":
          language = "csharp";
          break;
        case "go":
          language = "go";
          break;
        case "rs":
          language = "rust";
          break;
        case "rb":
          language = "ruby";
          break;
        case "php":
          language = "php";
          break;
        case "html":
          language = "html";
          break;
        case "css":
          language = "css";
          break;
        case "json":
          language = "json";
          break;
        case "xml":
          language = "xml";
          break;
        case "yaml":
        case "yml":
          language = "yaml";
          break;
        case "md":
          language = "markdown";
          break;
      }
      models[filename] = monaco.editor.createModel(files[filename], language);
    });

    // Create editor instance - start with first file
    const firstFile = firstTutorialFile || fileNames[0];

    // Check if mobile on load
    const isMobile = window.innerWidth <= 768;

    editor = monaco.editor.create(document.getElementById("editor"), {
      model: models[firstFile],
      theme: "vs-light",
      fontSize: isMobile ? 12 : 14,
      lineNumbers: "on",
      minimap: { enabled: false },
      scrollBeyondLastLine: false,
      automaticLayout: true,
      wordWrap: "on",
      glyphMargin: false,
      lineNumbersMinChars: 3,
      fontFamily: "'Menlo', 'Monaco', 'Consolas', 'Courier New', monospace",
      readOnly: true,
    });

    // Highlight the initial file in explorer
    document.querySelectorAll(".file-tree-file").forEach((f) => {
      f.classList.toggle("active", f.dataset.path === firstFile);
    });

    // Scroll to initial file in tree
    setTimeout(() => {
      scrollFileIntoView(firstFile);
    }, 500);

    // Navigation function
    function navigateToStep(stepIndex) {
      const step = tutorialSteps[stepIndex];
      const model = models[step.file];

      if (model) {
        // Update current step index
        currentStepIndex = stepIndex;

        // Update navigation buttons
        updateNavigationButtons();

        // Switch to the file
        editor.setModel(model);

        // Open the file tab for this step
        openFileTab(step.file);

        // Navigate to line with smooth scrolling
        editor.revealLineInCenter(step.line, monaco.editor.ScrollType.Smooth);
        editor.setPosition({ lineNumber: step.line, column: 1 });

        // Highlight the relevant lines
        if (step.endLine) {
          currentDecorations = editor.deltaDecorations(currentDecorations, [
            {
              range: new monaco.Range(step.line, 1, step.endLine, 1),
              options: {
                className: "tutorial-highlight",
                isWholeLine: true,
              },
            },
          ]);
        }

        // Update active accordion
        document
          .querySelectorAll("#tutorial-container .accordion-item")
          .forEach((item) => {
            item.classList.remove("active");
            item.classList.remove("expanded");
          });
        const activeAccordion = document.querySelector(
          `#tutorial-container .accordion-item[data-step="${stepIndex}"]`
        );
        activeAccordion.classList.add("active");
        activeAccordion.classList.add("expanded");

        // Scroll accordion item into view (iOS-friendly approach)
        setTimeout(() => {
          const accordionRect = activeAccordion.getBoundingClientRect();
          const containerRect = accordionContainer.getBoundingClientRect();

          // Only scroll if the accordion is not fully visible
          if (
            accordionRect.top < containerRect.top ||
            accordionRect.bottom > containerRect.bottom
          ) {
            accordionContainer.scrollTop =
              activeAccordion.offsetTop - accordionContainer.offsetTop;
          }
        }, 100);
      }
    }

    // Update navigation button states
    function updateNavigationButtons() {
      const prevButton = document.getElementById("prev-step");
      const nextButton = document.getElementById("next-step");

      prevButton.disabled = currentStepIndex === 0;
      nextButton.disabled = currentStepIndex === tutorialSteps.length - 1;
    }

    // File tab switching
    function switchFile(filename) {
      const model = models[filename];
      if (model) {
        editor.setModel(model);

        // Clear highlights when manually switching files
        currentDecorations = editor.deltaDecorations(currentDecorations, []);

        // Open tab if not already open
        openFileTab(filename);

        // Update active file in explorer
        document.querySelectorAll(".file-tree-file").forEach((f) => {
          f.classList.toggle("active", f.dataset.path === filename);
        });

        // Scroll to file in tree
        scrollFileIntoView(filename);
      }
    }

    // Simple markdown to HTML converter
    function simpleMarkdown(text) {
      // Wrap the text in a paragraph tag and handle markdown
      const html = text
        .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>") // Bold
        .replace(/\`(.+?)\`/g, "<code>$1</code>"); // Inline code

      return `<p>${html}</p>`;
    }

    // Initialize accordion content with markdown
    tutorialSteps.forEach((step, index) => {
      const contentDiv = document.querySelector(
        `#tutorial-container .accordion-item[data-step="${index}"] .accordion-content-inner`
      );
      if (contentDiv && step.markdown) {
        try {
          // Use marked if available, otherwise use simple converter
          if (typeof marked !== "undefined" && marked.parse) {
            contentDiv.innerHTML = marked.parse(step.markdown, {
              mangle: false,
              headerIds: false,
            });
          } else if (
            typeof marked !== "undefined" &&
            typeof marked === "function"
          ) {
            // Older version of marked
            contentDiv.innerHTML = marked(step.markdown);
          } else {
            contentDiv.innerHTML = simpleMarkdown(step.markdown);
          }
        } catch (e) {
          // Fallback to simple markdown
          contentDiv.innerHTML = simpleMarkdown(step.markdown);
        }
      }
    });

    // Accordion functionality
    document
      .querySelectorAll("#tutorial-container .accordion-button")
      .forEach((button) => {
        button.addEventListener("click", (e) => {
          const accordionItem = e.target.closest(".accordion-item");
          const stepIndex = parseInt(accordionItem.dataset.step);

          // Toggle expansion
          const wasExpanded = accordionItem.classList.contains("expanded");

          // Close all accordions
          document
            .querySelectorAll("#tutorial-container .accordion-item")
            .forEach((item) => {
              item.classList.remove("expanded");
            });

          // If this accordion wasn't expanded, expand it and navigate
          if (!wasExpanded) {
            accordionItem.classList.add("expanded");
            navigateToStep(stepIndex);
          }
        });
      });

    // File explorer event handlers
    document.addEventListener("click", (e) => {
      // Handle file clicks
      if (e.target.closest(".file-tree-file")) {
        const fileItem = e.target.closest(".file-tree-file");
        const filePath = fileItem.dataset.path;
        switchFile(filePath);
      }

      // Handle folder clicks
      if (e.target.closest(".folder-header")) {
        const folderHeader = e.target.closest(".folder-header");
        const folderItem = folderHeader.closest(".file-tree-folder");
        const folderChildren = folderItem.querySelector(".folder-children");
        const folderIcon = folderHeader.querySelector(".folder-icon");

        // Toggle expanded state
        if (folderItem.classList.contains("expanded")) {
          folderItem.classList.remove("expanded");
          folderChildren.style.display = "none";
          folderIcon.textContent = "📁";
        } else {
          folderItem.classList.add("expanded");
          folderChildren.style.display = "block";
          folderIcon.textContent = "📂";
        }
      }
    });

    // Navigation button event listeners
    document.getElementById("prev-step").addEventListener("click", () => {
      if (currentStepIndex > 0) {
        navigateToStep(currentStepIndex - 1);
      }
    });

    document.getElementById("next-step").addEventListener("click", () => {
      if (currentStepIndex < tutorialSteps.length - 1) {
        navigateToStep(currentStepIndex + 1);
      }
    });

    // Auto-navigate to first step and expand its accordion
    navigateToStep(0);
    document
      .querySelector('#tutorial-container .accordion-item[data-step="0"]')
      .classList.add("expanded");
  });
}

function startTour() {
  // Tour functionality
  class Tour {
    constructor() {
      this.steps = [
        {
          target: "#accordion-container",
          title: "Tutorial Steps",
          content:
            "Let's get a better sense of how to implement this feature by walking through a sample project.",
          placement: "right",
          mobilePlacement: "bottom",
        },
        {
          target: ".tutorial-nav-buttons",
          title: "Navigation Controls",
          content: "Use these buttons to move between tutorial steps.",
          placement: "top",
        },
        {
          target: ".editor-container",
          title: "Code Editor",
          content:
            "We will be looking at a sample project. We aren't going to run this code! We're just taking a look to understand how it works.",
          placement: "left",
          mobilePlacement: "top",
        },
      ];

      this.currentStep = 0;
      this.overlay = null;
      this.spotlight = null;
      this.tooltip = null;
      this.isActive = false;
      this.resizeHandler = null;

      this.init();
    }

    init() {
      // Add keyboard support for tour
      document.addEventListener("keydown", (e) => {
        // Escape to exit tour
        if (e.key === "Escape" && this.isActive) {
          this.end();
        }
      });

      // Create overlay elements
      this.overlay = document.createElement("div");
      this.overlay.className = "tour-overlay";

      this.spotlight = document.createElement("div");
      this.spotlight.className = "tour-spotlight";
      this.overlay.appendChild(this.spotlight);

      this.tooltip = document.createElement("div");
      this.tooltip.className = "tour-tooltip";

      // Add click handler to overlay to end tour when clicking outside
      this.overlay.addEventListener("click", (e) => {
        // Only end tour if clicking directly on overlay (not on spotlight or tooltip)
        if (e.target === this.overlay && this.isActive) {
          this.end();
        }
      });

      // Check if user is new (first visit) and auto-start tour
      if (!localStorage.getItem("tutorial-tour-completed")) {
        // Wait a moment for the page to fully load before starting
        setTimeout(() => {
          this.start();
        }, 500);
      }
    }

    start() {
      if (this.isActive) return;

      this.isActive = true;
      this.currentStep = 0;

      // Append overlay elements when tour starts
      document.body.appendChild(this.overlay);
      document.body.appendChild(this.tooltip);

      this.overlay.classList.add("active");
      document
        .querySelector("#tutorial-container")
        .classList.add("tour-active");

      // Add resize handler
      this.resizeHandler = () => {
        if (this.isActive) {
          this.updatePositions();
        }
      };
      window.addEventListener("resize", this.resizeHandler);

      this.showStep();
    }

    showStep() {
      const step = this.steps[this.currentStep];
      const target = document.querySelector(step.target);

      if (!target) {
        // Skip to next step if target not found
        if (this.currentStep < this.steps.length - 1) {
          this.currentStep++;
          this.showStep();
        } else {
          this.end();
        }
        return;
      }

      // Skip file explorer on mobile
      if (window.innerWidth <= 768 && step.target === "#file-explorer") {
        if (this.currentStep < this.steps.length - 1) {
          this.currentStep++;
          this.showStep();
        } else {
          this.end();
        }
        return;
      }

      // Position spotlight
      const rect = target.getBoundingClientRect();
      const padding = 8;

      this.spotlight.style.left = rect.left - padding + "px";
      this.spotlight.style.top = rect.top - padding + "px";
      this.spotlight.style.width = rect.width + padding * 2 + "px";
      this.spotlight.style.height = rect.height + padding * 2 + "px";

      // Create tooltip content
      this.tooltip.innerHTML = `
          <div class="tour-progress">
            ${this.steps
              .map(
                (_, i) =>
                  `<span class="tour-progress-dot ${
                    i === this.currentStep ? "active" : ""
                  }"></span>`
              )
              .join("")}
          </div>
          <h3>${step.title}</h3>
          <p>${step.content}</p>
          <div class="tour-tooltip-buttons">
            ${
              this.currentStep > 0
                ? '<button class="tour-button tour-button-secondary" onclick="tourManager.prev()">Previous</button>'
                : '<button class="tour-button tour-button-secondary" onclick="tourManager.end()">Skip</button>'
            }
            ${
              this.currentStep < this.steps.length - 1
                ? '<button class="tour-button tour-button-primary" onclick="tourManager.next()">Next</button>'
                : '<button class="tour-button tour-button-primary" onclick="tourManager.end()">Finish</button>'
            }
          </div>
        `;

      // Position tooltip - use mobilePlacement on mobile if available
      const isMobile = window.innerWidth <= 768;
      const placement =
        isMobile && step.mobilePlacement
          ? step.mobilePlacement
          : step.placement;
      this.positionTooltip(rect, placement);

      // Show tooltip with animation
      setTimeout(() => {
        this.tooltip.classList.add("show");
      }, 300);
    }

    updatePositions() {
      const step = this.steps[this.currentStep];
      const target = document.querySelector(step.target);
      
      if (!target) return;
      
      // Update spotlight position
      const rect = target.getBoundingClientRect();
      const padding = 8;
      
      this.spotlight.style.left = rect.left - padding + "px";
      this.spotlight.style.top = rect.top - padding + "px";
      this.spotlight.style.width = rect.width + padding * 2 + "px";
      this.spotlight.style.height = rect.height + padding * 2 + "px";
      
      // Update tooltip position
      const isMobile = window.innerWidth <= 768;
      const placement = isMobile && step.mobilePlacement ? step.mobilePlacement : step.placement;
      this.positionTooltip(rect, placement);
    }

    positionTooltip(targetRect, placement) {
      const tooltipRect = this.tooltip.getBoundingClientRect();
      const spacing = 16;
      let left, top;

      // Calculate position based on placement
      switch (placement) {
        case "top":
          left = targetRect.left + (targetRect.width - tooltipRect.width) / 2;
          top = targetRect.top - tooltipRect.height - spacing;
          break;
        case "bottom":
          left = targetRect.left + (targetRect.width - tooltipRect.width) / 2;
          top = targetRect.bottom + spacing;
          break;
        case "left":
          left = targetRect.left - tooltipRect.width - spacing;
          top = targetRect.top + (targetRect.height - tooltipRect.height) / 2;
          break;
        case "right":
          left = targetRect.right + spacing;
          top = targetRect.top + (targetRect.height - tooltipRect.height) / 2;
          break;
      }

      // Ensure tooltip stays within viewport
      const viewportWidth = window.innerWidth;
      const viewportHeight = window.innerHeight;

      // Adjust horizontal position
      if (left < 10) {
        left = 10;
      } else if (left + tooltipRect.width > viewportWidth - 10) {
        left = viewportWidth - tooltipRect.width - 10;
      }

      // Adjust vertical position
      if (top < 10) {
        top = targetRect.bottom + spacing;
      } else if (top + tooltipRect.height > viewportHeight - 10) {
        top = targetRect.top - tooltipRect.height - spacing;
      }

      this.tooltip.style.left = left + "px";
      this.tooltip.style.top = top + "px";
    }

    next() {
      if (this.currentStep < this.steps.length - 1) {
        this.tooltip.classList.remove("show");
        setTimeout(() => {
          this.currentStep++;
          this.showStep();
        }, 300);
      } else {
        this.end();
      }
    }

    prev() {
      if (this.currentStep > 0) {
        this.tooltip.classList.remove("show");
        setTimeout(() => {
          this.currentStep--;
          this.showStep();
        }, 300);
      }
    }

    end() {
      this.isActive = false;
      this.tooltip.classList.remove("show");
      this.overlay.classList.remove("active");
      document
        .querySelector("#tutorial-container")
        .classList.remove("tour-active");

      // Mark tour as completed
      localStorage.setItem("tutorial-tour-completed", "true");
      
      // Remove resize handler
      if (this.resizeHandler) {
        window.removeEventListener("resize", this.resizeHandler);
        this.resizeHandler = null;
      }

      // Remove overlay and tooltip from DOM after animation
      setTimeout(() => {
        this.currentStep = 0;
        this.spotlight.style.width = "0";
        this.spotlight.style.height = "0";

        // Remove elements from DOM
        if (this.overlay.parentNode) {
          this.overlay.parentNode.removeChild(this.overlay);
        }
        if (this.tooltip.parentNode) {
          this.tooltip.parentNode.removeChild(this.tooltip);
        }
      }, 300);
    }
  }

  // Initialize tour
  tourManager = new Tour();
  window.tourManager = tourManager; // Make it globally accessible for onclick handlers
}


// Initialize the tutorial
document.addEventListener('DOMContentLoaded', function() {
  // Wait a bit for dependencies to load
  let int = setInterval(() => {
    if (typeof files !== 'undefined' && typeof tutorialSteps !== 'undefined') {
      clearInterval(int)
      render(files, tutorialSteps);
      startTour()
    }
  }, 100);
});