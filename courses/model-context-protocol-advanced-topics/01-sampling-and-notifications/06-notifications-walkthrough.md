# Notifications walkthrough

> Source: https://anthropic.skilljar.com/model-context-protocol-advanced-topics/291036

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
          .gitignore
        
      
        
          📄
          client.py
        
      
        
          📄
          pyproject.toml
        
      
        
          📄
          README.md
        
      
        
          📄
          server.py
        
      
      
    

server.py×
12345678910111213141516171819202122from mcp.server.fastmcp import FastMCP, Contextimport asynciomcp = FastMCP(name="Demo Server")@mcp.tool()async def add(a: int, b: int, ctx: Context) -> int:    await ctx.info    ("Preparing to add...    ")    await ctx.    report_progress(20,     100)    await asyncio.sleep(2)    await ctx.info("OK,     adding...")    await ctx.    report_progress(80,     100)    return a + bif __name__ == "__main__":    mcp.run    (transport="stdio")


// Data from advanced_mcp/notifications.js
const files = {
  ".gitignore": `# Python-generated files
__pycache__/
*.py[oc]
build/
dist/
wheels/
*.egg-info

# Virtual environments
.venv
.python-version
`,

  "README.md": `# MCP Logging and Progress Demo

A demonstration of the Model Context Protocol using a STDIO transport.

## Setup

Install dependencies using uv:

\`\`\`bash
uv sync
\`\`\`

## Running the Project

Run the MCP client:

\`\`\`bash
uv run client.py
\`\`\`
`,

  "client.py": `from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.types import LoggingMessageNotificationParams

server_params = StdioServerParameters(
    command="uv",
    args=["run", "server.py"],
)


async def logging_callback(params: LoggingMessageNotificationParams):
    print(params.data)


async def print_progress_callback(
    progress: float, total: float | None, message: str | None
):
    if total is not None:
        percentage = (progress / total) * 100
        print(f"Progress: {progress}/{total} ({percentage:.1f}%)")
    else:
        print(f"Progress: {progress}")


async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(
            read, write, logging_callback=logging_callback
        ) as session:
            await session.initialize()

            await session.call_tool(
                name="add",
                arguments={"a": 1, "b": 3},
                progress_callback=print_progress_callback,
            )


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
`,

  "pyproject.toml": `[project]
name = "notifications"
version = "0.1.0"
description = "Demonstration of notifications with MCP"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "aioconsole>=0.8.1",
    "mcp[cli]>=1.9.3",
]

[tool.setuptools]
py-modules = ["client", "server"]

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"
`,

  "server.py": `from mcp.server.fastmcp import FastMCP, Context
import asyncio

mcp = FastMCP(name="Demo Server")


@mcp.tool()
async def add(a: int, b: int, ctx: Context) -> int:
    await ctx.info("Preparing to add...")
    await ctx.report_progress(20, 100)

    await asyncio.sleep(2)

    await ctx.info("OK, adding...")
    await ctx.report_progress(80, 100)

    return a + b


if __name__ == "__main__":
    mcp.run(transport="stdio")
`,
};

const tutorialTitle = "Log and Progress Notifications";

const tutorialSteps = [
  {
    file: "server.py",
    line: 8,
    endLine: 8,
    title: "Tool function receives Context argument",
    markdown:
      "Tool functions automatically receive 'Context' as their last argument. This object has methods for logging and reporting progress to the client.",
  },

  {
    file: "server.py",
    line: 9,
    endLine: 15,
    title: "Create logs and progress with context",
    markdown:
      "Throughout your tool function, call the `info()`, `warning()`, `debug()`, or `error()` methods to log different types of messages for the client. Also call the `report_progress()` method to estimate the amount of remaining work for the tool call.",
  },
  {
    file: "client.py",
    line: 11,
    endLine: 22,
    title: "Define callbacks on the client",
    markdown:
      "The client needs to define logging and progress callbacks, which will automatically be called whenever the server emits log or progress messages. These callbacks should try to display the provided logging and progress data to the user.",
  },
  {
    file: "client.py",
    line: 27,
    endLine: 36,
    title: "Pass callbacks to appropriate functions",
    markdown:
      "Make sure you provide the logging callback to the `ClientSession` and the progress callback to the `call_tool()` function.",
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