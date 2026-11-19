⚡ SQLSentinel

<div align="center">
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:050816,50:0077B6,100:00E5FF&height=220&section=header&text=SQLSentinel&fontSize=65&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=Advanced%20SQL%20Injection%20Auditing%20Framework&descAlignY=60&descSize=17" width="100%" />

Detect. Analyze. Secure.

A powerful Python-based framework for authorized SQL injection security auditing.

</div>

⸻

🧬 ABOUT THE PROJECT

SQLSentinel is an advanced Python-based CLI framework engineered for ethical hackers, penetration testers, and security researchers.

It streamlines SQL injection auditing through automated vulnerability detection, database error analysis, boolean-based response comparison, WAF indicators, and professional security reporting.

⚡ CORE CAPABILITIES

Feature	Description
🔍 Detection Engine	Automated SQL injection assessment
🧠 Error Analysis	Database error identification
⚖️ Boolean Analysis	Response behavior comparison
🛡️ WAF Intelligence	WAF presence indicators
📊 Reporting Engine	Structured security reports
💻 CLI Interface	Interactive terminal workflow

🖥️ TERMINAL PREVIEW

┌──────────────────────────────────────────────┐
│                                              │
│   ███████╗ ██████╗ ██╗      ███████╗         │
│   ██╔════╝██╔═══██╗██║      ██╔════╝         │
│   ███████╗██║   ██║██║      ███████╗         │
│   ╚════██║██║▄▄ ██║██║      ╚════██║         │
│   ███████║╚██████╔╝███████╗ ███████║         │
│   ╚══════╝ ╚══▀▀═╝ ╚══════╝ ╚══════╝         │
│                                              │
│             SQL SENTINEL                     │
│       SQL INJECTION AUDITING FRAMEWORK       │
│                                              │
└──────────────────────────────────────────────┘
[+] Initializing SQLSentinel...
[+] Loading detection modules...
[+] Security engine ready.
[*] Awaiting authorized target...

⚙️ INSTALLATION

Python 3.10 or newer is required. Other users can clone the repository and
install the CLI from its root directory:

```shell
git clone https://github.com/Kichu-10/SQLSentinel.git
cd SQLSentinel
python -m pip install .
```

🚀 USAGE

Show available commands and the installed version:

```shell
sqlsentinel --help
sqlsentinel version
```

Inspect a URL's query parameters without sending a request:

```shell
sqlsentinel inspect-url "https://example.com/products?id=1&category=books"
```

To scan a different URL, replace the example URL and hostname with the exact
target covered by your written authorization:

```shell
sqlsentinel scan "https://app.example.com/products?id=1" --scope-host app.example.com --authorized --allow-public-target --max-requests 12 --delay 1 --timeout 8 --output reports/report.json --format json
```

`--scope-host` must match the URL's hostname exactly (no scheme or path).
`--allow-public-target` is required for public hosts; use it only when your
written authorization covers that host. Omit it for private or local targets.
The scanner is bounded and non-destructive; it does not extract database
contents or write to the target. Run `sqlsentinel scan --help` for all options.

🧪 TESTS

Contributors can install the test dependencies and run the test suite from the
repository root:

```shell
python -m pip install -e ".[dev]"
python -m pytest -q
```

See the documentation for supported commands and authorized testing workflows.

🏗️ PROJECT PHILOSOPHY

Security isn’t about finding weaknesses alone.
It’s about understanding them, documenting them, and fixing them.

🔐 ETHICAL USE

SQLSentinel is developed exclusively for:

* Authorized penetration testing
* Personal security labs
* Educational research
* Defensive security assessments

Never test systems without explicit authorization.

⸻

<div align="center">

⚡ SQLSentinel

BUILT FOR SECURITY. DESIGNED FOR PRECISION.

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:00E5FF,50:0077B6,100:050816&height=100&section=footer" width="100%" />
</div>
