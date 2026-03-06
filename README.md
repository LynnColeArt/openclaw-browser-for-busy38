# OpenClaw Browser for Busy38

A security-first browser automation plugin for Busy38, ported from OpenClaw's browser component with enhanced content screening capabilities.

## Overview

This plugin brings OpenClaw's powerful browser automation capabilities to Busy38, featuring:

- **Full Browser Control**: Navigate, screenshot, click, type, evaluate JavaScript
- **Security-First Architecture**: Toots content prescreener, HTML sanitization, context injection prevention
- **Busy38 Integration**: Native cheatcode namespace (`browser:*`) with full plugin schema support
- **MIT Licensed**: Same license as OpenClaw

## Security Features

### Toots Content Prescreener

Toots is a noir detective persona that screens all web content before it reaches the agent:

- **Hidden Instruction Detection**: Identifies prompt injection attempts, hidden commands, and social engineering
- **Script Analysis**: Detects malicious scripts, eval() patterns, and obfuscated code
- **Context Injection Prevention**: Prevents content from manipulating the agent's context or instructions
- **Audit Logging**: All browser actions are logged for security review

### Content Sanitization Pipeline

1. **HTML Parsing**: Content is parsed and stripped of dangerous elements
2. **Script Neutralization**: JavaScript is either removed or sandboxed
3. **Attribute Filtering**: Dangerous attributes (onload, onerror, etc.) are stripped
4. **Text Extraction**: Safe text content is extracted for LLM consumption

### Security Configurations

```yaml
# Security levels
security_level: strict  # strict|moderate|permissive
enable_toots_screening: true
enable_js_sandbox: true
audit_all_actions: true
```

## Busy38 Plugin Schema

### manifest.json

```json
{
  "name": "busy-38-browser",
  "version": "0.1.0",
  "description": "OpenClaw browser automation with Toots security screening",
  "license": "MIT",
  "type": "toolkit",
  "permissions": ["browser:control", "browser:screenshot", "browser:evaluate"],
  "toolkit_path": "toolkit"
}
```

### tool_spec.yaml

Defines the `browser:*` namespace with actions:

- `navigate` - Load a URL
- `screenshot` - Capture page or element
- `snapshot` - Get accessible page structure
- `click` - Click an element by ref
- `type` - Type text into an element
- `evaluate` - Execute JavaScript (security-screened)
- `status` - Get browser status

### Namespaces

All browser actions are exposed under the `browser:*` namespace:

```
[browser:navigate url="https://example.com"]
[browser:snapshot]
[browser:click ref="12"]
[browser:screenshot full_page=true]
```

### Cheatcodes

Cheatcodes use the format `[browser:action]` with key=value parameters:

| Cheatcode | Description | Parameters |
|-----------|-------------|------------|
| `[browser:navigate]` | Navigate to URL | `url`, `timeout`, `wait_until` |
| `[browser:snapshot]` | Get page snapshot | `format`, `interactive`, `compact` |
| `[browser:click]` | Click element | `ref`, `double`, `slowly` |
| `[browser:type]` | Type text | `ref`, `text`, `submit`, `clear` |
| `[browser:screenshot]` | Take screenshot | `full_page`, `ref`, `type` |
| `[browser:evaluate]` | Run JavaScript | `fn`, `arg`, `timeout` |
| `[browser:status]` | Browser status | - |
| `[browser:close]` | Close browser | - |

### Hooks & Filters

The plugin provides hooks for:

- **Pre-navigation**: URL validation, blocklist checking
- **Post-navigation**: Content screening, sanitization
- **Pre-evaluation**: JavaScript security analysis
- **Post-screenshot**: Image metadata scrubbing

## Installation

### Prerequisites

- Python 3.9+
- Playwright: `pip install playwright`
- Browser binaries: `playwright install chromium`
- Busy38 with plugin support enabled

### Install Plugin

1. Clone to Busy38 vendor directory:

```bash
cd /path/to/busy38/vendor
git clone https://github.com/LynnColeArt/openclaw-browser-for-busy38.git busy-38-browser
```

2. Install Python dependencies:

```bash
cd busy-38-browser
pip install -r requirements.txt
playwright install chromium
```

3. Enable in Busy38 config:

```yaml
# busy38-config.yaml
plugins:
  vendor:
    - busy-38-browser
```

4. Restart Busy38

## Usage

### Basic Navigation

```
[browser:navigate url="https://example.com"]
```

### Taking Screenshots

```
[browser:screenshot full_page=true]
```

Returns: `MEDIA: /path/to/screenshot.png`

### Page Snapshots

```
[browser:snapshot format=interactive]
```

Returns structured page content with element refs for interaction.

### Clicking Elements

```
[browser:snapshot]
[browser:click ref="12"]
```

### Typing Text

```
[browser:type ref="23" text="Hello World" submit=true]
```

### JavaScript Evaluation (Security-Screened)

```
[browser:evaluate fn="return document.title"]
```

Toots screens all JavaScript before execution. Dangerous patterns are blocked.

## Security Configuration

Edit `security.yaml` in the plugin directory:

```yaml
# security.yaml
toots:
  enabled: true
  strictness: high  # low|medium|high|paranoid
  block_patterns:
    - "eval("
    - "Function("
    - "document.write"
    - "innerHTML.*script"

sanitization:
  allowed_tags:
    - p
    - div
    - span
    - h1
    - h2
    - h3
    - a
    - img
  blocked_attributes:
    - onload
    - onerror
    - onclick
    - onmouseover

audit:
  enabled: true
  log_directory: ./audit_logs
  retention_days: 30
```

## Architecture

```
busy-38-browser/
├── manifest.json          # Plugin metadata
├── tool_spec.yaml         # Tool definitions
├── requirements.txt       # Python dependencies
├── security.yaml          # Security configuration
├── toolkit/
│   ├── __init__.py       # Plugin entry point
│   ├── browser_core.py   # Core browser automation
│   └── security_screen.py # Toots content prescreener
└── docs/
    └── EVALUATION_AND_PLAN.md  # Technical documentation
```

## Testing

Run the test suite:

```bash
pytest tests/
```

Run security tests:

```bash
pytest tests/test_security.py -v
```

## Differences from OpenClaw

1. **Security-First**: Toots prescreener added for all content
2. **Busy38 Native**: Uses cheatcode namespace instead of direct tool calls
3. **Plugin Architecture**: Fits Busy38's vendor plugin pattern
4. **Python Implementation**: Ported from TypeScript to Python
5. **Content Over Navigation**: Allows arbitrary URLs with content sanitization

## License

MIT License - same as OpenClaw

Copyright (c) 2024 Lynn Cole Art

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Contributing

Contributions welcome! Please ensure:

1. Security tests pass
2. Toots screening covers new code paths
3. Documentation is updated
4. MIT license compatibility maintained

## Support

- Issues: https://github.com/LynnColeArt/openclaw-browser-for-busy38/issues
- Discussions: https://github.com/LynnColeArt/openclaw-browser-for-busy38/discussions
