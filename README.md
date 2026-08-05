<img src="https://capsule-render.vercel.app/api?type=waving&color=ff1f3d&height=180&section=header&text=DiscordReaper&fontSize=82&fontColor=ffffff&animation=twinkling&fontAlignY=55" width="100%">

<div align="center">

[![Stars](https://img.shields.io/github/stars/R3CI/DiscordReaper?style=for-the-badge&color=ff1f3d&labelColor=0d0d10&logo=github&logoColor=white)](https://github.com/R3CI/DiscordReaper/stargazers)
[![Forks](https://img.shields.io/github/forks/R3CI/DiscordReaper?style=for-the-badge&color=f5c040&labelColor=0d0d10&logo=github&logoColor=white)](https://github.com/R3CI/DiscordReaper/network/members)
[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white&labelColor=0d0d10)](https://python.org)
[![License](https://img.shields.io/github/license/R3CI/DiscordReaper?style=for-the-badge&color=1fd97a&labelColor=0d0d10)](LICENSE)
[![Platform](https://img.shields.io/badge/Windows%20%7C%20Linux-Supported-b78cff?style=for-the-badge&labelColor=0d0d10)](https://github.com/R3CI/DiscordReaper)
[![Telegram](https://img.shields.io/badge/Telegram-%40ther3ci-229ED9?style=for-the-badge&logo=telegram&logoColor=white&labelColor=0d0d10)](https://t.me/ther3ci)

</div>

---

## What is DiscordReaper?

Discord token tool. Spread to servers and DMs, check token validity, evaluate accounts by guild/DM/friend count, capture full account info, and score usernames for rarity. Runs on Windows and Linux with a native GUI.

---

## Tools

<table>
<thead>
<tr>
<th width="22%">Tool</th>
<th>What it does</th>
</tr>
</thead>
<tbody>

<tr>
<td><strong>Spread</strong></td>
<td>
Sends messages to server channels and DMs across multiple tokens concurrently. Supports dynamic placeholders (<code>{ping}</code>, <code>{random}</code>), file and image attachments, configurable thread count and message delay. Tracks sent, failed, dead, and locked counts per run.
</td>
</tr>

<tr>
<td><strong>Checker</strong></td>
<td>
Checks tokens against the Discord API and sorts them into alive, dead, and locked. Results stream in as each token finishes. Handles rate limits automatically.
</td>
</tr>

<tr>
<td><strong>Nukable Capture</strong></td>
<td>
Pulls every guild each token is in and checks whether the account has <code>Administrator</code>. Returns server name and token pairs where admin access was found.
</td>
</tr>

<tr>
<td><strong>Evaluator</strong></td>
<td>
Fetches guild count, DM count, and friend count for each valid token along with account creation date. Results export as CSV.
</td>
</tr>

<tr>
<td><strong>Rare Checker</strong></td>
<td>
Scores accounts 0-100 based on username length, account creation year, and rare badges (Early Supporter, Staff, Partner, Bug Hunter, Verified Developer). Filter by length, year, score, or rare-only.
</td>
</tr>

<tr>
<td><strong>Token Capture</strong></td>
<td>
Pulls the full account snapshot for each token: valid/invalid/locked status, Nitro type, payment methods, badges, email verification, phone, and MFA. Filterable in real time, exports as CSV.
</td>
</tr>

</tbody>
</table>

---

## Features

| Feature | Detail |
|---|---|
| GUI | pywebview, runs as a native window, no browser required |
| Concurrency | Thread pool per tool, configurable up to 1000 concurrent threads |
| Proxies | HTTP proxies loaded from file, rotated per session |
| Rate limiting | Automatic retry with `retry_after` from Discord responses |
| Storage | Tokens, proxies, messages and settings saved to disk |
| Export | Results saved as CSV to the app data folder |
| Platform | Windows and Linux |

---

## Installation

> **Requires Python 3.8 or newer**

```bash
git clone https://github.com/R3CI/DiscordReaper.git
cd DiscordReaper
pip install -r requirements.txt
python main.py
```

<details>
<summary><strong>Windows - having trouble?</strong></summary>

Run `fix_windows.bat`. Checks Python version, pip, WebView2, all dependencies and source files, installs anything missing.

</details>

<details>
<summary><strong>Linux - having trouble?</strong></summary>

Run `bash fix_linux.sh`. Detects your distro, installs GTK3 and WebKit2GTK system packages, installs Python dependencies, checks your display session.

</details>

---

## Star History

<div align="center">

[![Star History Chart](https://api.star-history.com/svg?repos=R3CI/DiscordReaper&type=Date)](https://star-history.com/#R3CI/DiscordReaper&Date)

</div>

---

<div align="center">

### If this is useful to you, drop a star.

[![Star this repo](https://img.shields.io/badge/Star%20This%20Repo-ff1f3d?style=for-the-badge&labelColor=0d0d10)](https://github.com/R3CI/DiscordReaper/stargazers)

</div>

---

## Contact

Telegram: **[@ther3ci](https://t.me/ther3ci)**

---

## License

MIT - see [LICENSE](LICENSE).

<img src="https://capsule-render.vercel.app/api?type=waving&color=ff1f3d&height=110&section=footer" width="100%">
