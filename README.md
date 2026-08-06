<img src="https://capsule-render.vercel.app/api?type=waving&color=ff1f3d&height=260&section=header&text=DiscordReaper&fontSize=86&fontColor=ffffff&animation=twinkling&fontAlignY=48" width="100%">

<div align="center">

[![Stars](https://img.shields.io/github/stars/R3CI/DiscordReaper?style=for-the-badge&color=ff1f3d&labelColor=0d0d10&logo=github&logoColor=white)](https://github.com/R3CI/DiscordReaper/stargazers)
[![Forks](https://img.shields.io/github/forks/R3CI/DiscordReaper?style=for-the-badge&color=f5c040&labelColor=0d0d10&logo=github&logoColor=white)](https://github.com/R3CI/DiscordReaper/network/members)
[![Issues](https://img.shields.io/github/issues/R3CI/DiscordReaper?style=for-the-badge&color=00d0f0&labelColor=0d0d10&logo=github&logoColor=white)](https://github.com/R3CI/DiscordReaper/issues)
[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white&labelColor=0d0d10)](https://python.org)
[![License](https://img.shields.io/github/license/R3CI/DiscordReaper?style=for-the-badge&color=1fd97a&labelColor=0d0d10)](LICENSE)
[![Platform](https://img.shields.io/badge/Windows%20%7C%20Linux-Supported-b78cff?style=for-the-badge&labelColor=0d0d10&logo=windows&logoColor=white)](https://github.com/R3CI/DiscordReaper)
[![Telegram](https://img.shields.io/badge/Telegram-%40ther3ci-229ED9?style=for-the-badge&logo=telegram&logoColor=white&labelColor=0d0d10)](https://t.me/ther3ci)

</div>

<br>

<div align="center">

Discord token tool. Spread to servers and DMs, check validity, evaluate accounts, capture full snapshots, and surface rare usernames. Native GUI on Windows and Linux.

</div>

---

> [!WARNING]
> This project is provided for **educational and research purposes only**. The developer takes no responsibility for how this tool is used. Usage of this tool against accounts or servers you do not own or have explicit permission to test is against Discord's Terms of Service and may be illegal in your jurisdiction. By using this software you accept full responsibility for your actions.

---

## Architecture

```mermaid
flowchart TD
    subgraph Input [" Input "]
        direction LR
        T([Token List])
        P([Proxy List])
        CF([Config / Settings])
    end

    subgraph Core [" Core Engine "]
        direction TB
        SM[Session Manager\nInjects headers + rotates proxies]
        subgraph Pool [Thread Pool]
            W1[Worker 1] & W2[Worker 2] & WN[Worker N]
        end
        CC["curl_cffi\nChrome 146 TLS + JA3 fingerprint"]
    end

    subgraph Tools [" Tools "]
        direction LR
        SP[Spread]
        CH[Checker]
        NC[Nukable Capture]
        EV[Evaluator]
        RC[Rare Checker]
        TC[Token Capture]
    end

    subgraph RateControl [" Rate Control "]
        direction LR
        R429["retry_after backoff\n(Discord 429)"]
        RCF["Sleep + retry\n(Cloudflare block)"]
        RDEAD["Bucket immediately\n(401 dead)"]
    end

    subgraph Output [" Output "]
        direction LR
        GUI[Live GUI Stream]
        CSV[CSV Export]
    end

    Input --> SM
    SM --> Pool
    Pool --> Tools
    Tools --> CC
    CC -->|HTTPS| API[(Discord API v9)]
    API -->|429| R429 --> CC
    API -->|Cloudflare| RCF --> CC
    API -->|401| RDEAD --> GUI
    API -->|200 OK| GUI
    GUI --> CSV
```

---

## Tools

<table>
<thead>
<tr>
<th width="20%">Tool</th>
<th>What it does</th>
</tr>
</thead>
<tbody>

<tr>
<td><strong>Spread</strong></td>
<td>Sends messages to server channels and DMs across multiple tokens concurrently. Supports dynamic placeholders (<code>{ping}</code>, <code>{random}</code>), file and image attachments, configurable thread count and message delay. Tracks sent, failed, dead, and locked counts per run.</td>
</tr>

<tr>
<td><strong>Checker</strong></td>
<td>Checks tokens against the Discord API and sorts them into alive, dead, and locked. Results stream in as each token finishes. Handles rate limits automatically.</td>
</tr>

<tr>
<td><strong>Nukable Capture</strong></td>
<td>Pulls every guild each token is in and checks whether the account has <code>Administrator</code>. Returns server name and token pairs where admin access was found.</td>
</tr>

<tr>
<td><strong>Evaluator</strong></td>
<td>Fetches guild count, DM count, and friend count for each valid token along with account creation date. Results export as CSV.</td>
</tr>

<tr>
<td><strong>Rare Checker</strong></td>
<td>Scores accounts 0-100 based on username length, account creation year, and rare badges (Early Supporter, Staff, Partner, Bug Hunter, Verified Developer). Filter by length, year, score, or rare-only.</td>
</tr>

<tr>
<td><strong>Token Capture</strong></td>
<td>Pulls the full account snapshot for each token: valid/invalid/locked status, Nitro type, payment methods, badges, email verification, phone, and MFA. Filterable in real time, exports as CSV.</td>
</tr>

</tbody>
</table>

---

## How it works

Each tool follows the same pipeline:

```mermaid
sequenceDiagram
    participant U as User
    participant G as GUI
    participant Pool as Thread Pool
    participant H as curl_cffi
    participant D as Discord API

    U->>G: Load tokens + proxies, press Start
    G->>Pool: Spawn N worker threads
    loop Per token
        Pool->>H: Assign token + proxy
        H->>D: API request (Chrome 146 fingerprint)
        D-->>H: 200 / 401 / 429 / Cloudflare
        H-->>Pool: Parse response
        Pool-->>G: Stream result to UI live
    end
    G-->>U: Export CSV on demand
```

Rate limit responses (`429`) back off using Discord's `retry_after` value. Cloudflare blocks trigger a short sleep and retry. Dead tokens (`401`) are immediately bucketed and never retried.

---

## Features

| Feature | Detail |
|---|---|
| GUI | pywebview, native window, no browser or Electron required |
| Concurrency | Semaphore-bounded thread pool per tool, 1-1000 threads |
| Proxies | HTTP proxies from file, rotated per session automatically |
| Rate limiting | Reads `retry_after` from Discord, sleeps exactly that long |
| Fingerprinting | Every request uses `curl_cffi` with Chrome 146 TLS/JA3 |
| Storage | Tokens, proxies, messages, settings persisted to disk |
| Export | All tool results dump to CSV in the app data folder |
| Platform | Windows and Linux, single codebase |

---

## Tech stack

| Package | Role |
|---|---|
| `pywebview` | Native GUI window (WebKit2GTK on Linux, WebView2 on Windows) |
| `curl_cffi` | HTTP client with Chrome 146 TLS fingerprint |
| `ruamel.yaml` | Config and settings persistence |
| `threading` | Per-tool concurrent worker pools with semaphore control |

---

## Installation

> [!IMPORTANT]
> Requires **Python 3.8** or newer. Run the fix script if anything is missing, it checks and installs everything automatically.

```bash
git clone https://github.com/R3CI/DiscordReaper.git
cd DiscordReaper
pip install -r requirements.txt
python main.py
```

<details>
<summary><strong>Windows - having trouble?</strong></summary>

Run `fix_windows.bat`. Checks Python version, pip, WebView2 runtime, all dependencies and source files. Installs anything missing and tells you exactly what failed.

</details>

<details>
<summary><strong>Linux - having trouble?</strong></summary>

Run `bash fix_linux.sh`. Detects your distro (Debian/Ubuntu, Fedora, Arch), installs GTK3 and WebKit2GTK system packages, installs Python dependencies, checks your display session.

</details>

> [!NOTE]
> On Linux, a desktop session is required (`DISPLAY` or `WAYLAND_DISPLAY` must be set). Headless servers will not work.

---

## Star History

<a href="https://www.star-history.com/?repos=R3CI%2FDiscordReaper&type=timeline&logscale=&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=R3CI/DiscordReaper&type=timeline&theme=dark&logscale&legend=top-left&sealed_token=n7VYCgq6tr64uZ-rbo70-22KpDqkERwIA431S0Mt0z8gHm22mvOWhR8Q4B1HHljsjOiMDJo31FXLjoJH8Rs826EsNU5Hxtt13aVWMfKQ3aeDwk2MFfkksUZmT50U1UHBnzS9RwGsmH_fLbHsgmckSI4Ba0CitqgKEnHx4tTQpklOY9WoBuH-gnZpVF18" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=R3CI/DiscordReaper&type=timeline&logscale&legend=top-left&sealed_token=n7VYCgq6tr64uZ-rbo70-22KpDqkERwIA431S0Mt0z8gHm22mvOWhR8Q4B1HHljsjOiMDJo31FXLjoJH8Rs826EsNU5Hxtt13aVWMfKQ3aeDwk2MFfkksUZmT50U1UHBnzS9RwGsmH_fLbHsgmckSI4Ba0CitqgKEnHx4tTQpklOY9WoBuH-gnZpVF18" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=R3CI/DiscordReaper&type=timeline&logscale&legend=top-left&sealed_token=n7VYCgq6tr64uZ-rbo70-22KpDqkERwIA431S0Mt0z8gHm22mvOWhR8Q4B1HHljsjOiMDJo31FXLjoJH8Rs826EsNU5Hxtt13aVWMfKQ3aeDwk2MFfkksUZmT50U1UHBnzS9RwGsmH_fLbHsgmckSI4Ba0CitqgKEnHx4tTQpklOY9WoBuH-gnZpVF18" />
 </picture>
</a>

---

<div align="center">

### If this is useful to you, drop a star.

[![Star this repo](https://img.shields.io/badge/Star%20This%20Repo-ff1f3d?style=for-the-badge&labelColor=0d0d10&logo=github&logoColor=white)](https://github.com/R3CI/DiscordReaper/stargazers)

</div>

---

## Contact

Telegram: **[@ther3ci](https://t.me/ther3ci)**

---

## License

MIT - see [LICENSE](LICENSE).

<img src="https://capsule-render.vercel.app/api?type=waving&color=ff1f3d&height=120&section=footer" width="100%">
