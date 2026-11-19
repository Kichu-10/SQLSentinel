<div align="center">

<img src="https://capsule-render.vercel.app/api?type=venom&color=0:050816,50:0077B6,100:00E5FF&height=260&section=header&text=SQLSentinel&fontSize=78&fontColor=ffffff&animation=twinkling&fontAlignY=38&desc=Advanced%20SQL%20Injection%20Auditing%20Framework&descAlignY=60&descSize=18" width="100%" />

<a href="https://github.com/Kichu-10/SQLSentinel">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&pause=1000&color=00E5FF&center=true&vCenter=true&width=640&lines=Detect.+Analyze.+Secure.;Bounded+%E2%80%A2+Non-destructive+%E2%80%A2+Scope-locked;Built+for+authorized+security+audits" alt="Typing SVG" />
</a>

<br/>

![Python](https://img.shields.io/badge/Python-3.10%2B-0077B6?style=for-the-badge&logo=python&logoColor=white&labelColor=050816)
![CLI](https://img.shields.io/badge/Interface-CLI-00E5FF?style=for-the-badge&logo=gnubash&logoColor=050816&labelColor=050816)
![Scanner](https://img.shields.io/badge/Scanner-Non--Destructive-2ea44f?style=for-the-badge&logo=shield&logoColor=white&labelColor=050816)
![Scope](https://img.shields.io/badge/Scope-Locked-ff4d6d?style=for-the-badge&logo=target&logoColor=white&labelColor=050816)
![Use](https://img.shields.io/badge/Use-Authorized%20Only-f9c74f?style=for-the-badge&logo=lock&logoColor=050816&labelColor=050816)

<br/>

**A powerful Python-based framework for authorized SQL injection security auditing.**

[**About**](#-about) •
[**Features**](#-core-capabilities) •
[**Preview**](#-live-preview) •
[**Install**](#-installation) •
[**Usage**](#-usage) •
[**Tests**](#-tests) •
[**Ethics**](#-ethical-use)

</div>

---

## 🧬 About

**SQLSentinel** is an advanced Python-based CLI framework engineered for **ethical hackers, penetration testers, and security researchers**.

It streamlines SQL injection auditing through automated vulnerability detection, database error analysis, boolean-based response comparison, WAF indicators, and professional security reporting, all behind strict scope and authorization checks.

> [!IMPORTANT]
> SQLSentinel refuses to run until you confirm written authorization and an **exact hostname match**. Safety is built into the workflow, not bolted on.

---

## ⚡ Core Capabilities

<div align="center">

| | Module | Description |
|:-:|:--|:--|
| 🔍 | **Detection Engine** | Automated SQL injection assessment |
| 🧠 | **Error Analysis** | Database error identification |
| ⚖️ | **Boolean Analysis** | Response behavior comparison |
| 🛡️ | **WAF Intelligence** | WAF presence indicators |
| 📊 | **Reporting Engine** | Structured security reports (JSON) |
| 💻 | **CLI Interface** | Interactive terminal workflow and dashboard |
| 🔒 | **Scope Guard** | Exact host matching and authorization prompts |

</div>

---

## 🔄 How It Works

```mermaid
flowchart LR
    A([🎯 Target URL]) --> B{🔒 Scope Guard}
    B -- host mismatch --> X([⛔ Rejected])
    B -- exact match + authorized --> C[🔍 Detection Engine]
    C --> D[🧠 Error Analysis]
    C --> E[⚖️ Boolean Analysis]
    C --> F[🛡️ WAF Indicators]
    D --> G[📊 Report]
    E --> G
    F --> G
    G --> H([✅ Findings])

    style A fill:#050816,stroke:#00E5FF,color:#fff
    style B fill:#0077B6,stroke:#00E5FF,color:#fff
    style X fill:#7a1f2b,stroke:#ff4d6d,color:#fff
    style G fill:#0077B6,stroke:#00E5FF,color:#fff
    style H fill:#064e3b,stroke:#2ea44f,color:#fff
```

---

## 🖥️ Live Preview

### Interactive dashboard

Run `sqlsentinel dashboard` and answer the guided prompts. The scope guard validates everything before a single request is sent.

<div align="center">

<img src="assets/dashboard-preview.png" alt="SQLSentinel interactive dashboard showing the scope guard rejecting a mismatched hostname" width="85%" />

<sub>The dashboard enforces the exact hostname match. Here the scope was entered as a path, so the scan is safely rejected.</sub>

</div>

> [!TIP]
> The **scope hostname** is just the host, with no scheme and no path.
> ✅ `example.com`  ❌ `https://example.com`  ❌ `/admin`

### Startup banner

```text
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
```

---

## ⚙️ Installation

> **Requires Python 3.10 or newer.**

```shell
git clone https://github.com/Kichu-10/SQLSentinel.git
cd SQLSentinel
python -m pip install .
```

---

## 🚀 Usage

### 1️⃣ Explore the CLI

```shell
sqlsentinel --help
sqlsentinel version
```

### 2️⃣ Launch the guided dashboard

```shell
sqlsentinel dashboard
```

### 3️⃣ Inspect a URL (no request is sent)

```shell
sqlsentinel inspect-url "https://example.com/products?id=1&category=books"
```

### 4️⃣ Run a scoped scan

Replace the example URL and hostname with the **exact target covered by your written authorization**:

```shell
sqlsentinel scan "https://app.example.com/products?id=1" \
  --scope-host app.example.com \
  --authorized \
  --allow-public-target \
  --max-requests 12 \
  --delay 1 \
  --timeout 8 \
  --output reports/report.json \
  --format json
```

<details>
<summary><b>📖 Option reference</b></summary>

<br/>

| Option | Purpose |
|:--|:--|
| `--scope-host` | Must match the URL's hostname **exactly** (no scheme or path) |
| `--authorized` | Confirms you hold written authorization for this target |
| `--allow-public-target` | Required for public hosts. Omit for private or local targets |
| `--max-requests` | Hard cap on requests sent |
| `--delay` | Seconds to wait between requests |
| `--timeout` | Per-request timeout in seconds |
| `--output` | Where the report is written |
| `--format` | Report format (e.g. `json`) |

Run `sqlsentinel scan --help` for all options.

</details>

> [!NOTE]
> The scanner is **bounded and non-destructive**. It does not extract database contents or write to the target.

---

## 🧪 Tests

Install the dev dependencies and run the suite from the repository root:

```shell
python -m pip install -e ".[dev]"
python -m pytest -q
```

See the documentation for supported commands and authorized testing workflows.

---

## 🏗️ Project Philosophy

<div align="center">

> *Security isn't about finding weaknesses alone.*
> *It's about understanding them, documenting them, and fixing them.*

</div>

---

## 🔐 Ethical Use

SQLSentinel is developed **exclusively** for:

- ✅ Authorized penetration testing
- ✅ Personal security labs
- ✅ Educational research
- ✅ Defensive security assessments

> [!CAUTION]
> **Never test systems without explicit written authorization.** Unauthorized testing may be illegal. You are solely responsible for how you use this tool.

---

<div align="center">

### ⚡ SQLSentinel

**BUILT FOR SECURITY. DESIGNED FOR PRECISION.**

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:00E5FF,50:0077B6,100:050816&height=120&section=footer" width="100%" />

</div>
