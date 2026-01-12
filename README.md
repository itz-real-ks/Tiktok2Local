<h1>TikTok No-Watermark Downloader (curl-based) 🎥</h1>

<p>
A <strong>reliable, cross-platform TikTok downloader</strong> that fetches
<strong>no-watermark videos only</strong>, powered by <code>curl</code> for
maximum CDN compatibility and a Python orchestrator for batching, logging,
and automation.
</p>

<p>
This tool <strong>fails fast</strong> if a no-watermark video is unavailable —
no silent fallbacks, no watermarked downloads.
</p>

<hr/>

<h2>✨ Features</h2>
<ul>
  <li>✅ <strong>No-watermark only</strong> (strict)</li>
  <li>⚡ <strong>curl-powered downloads</strong> (native progress bar, robust TLS)</li>
  <li>🧵 <strong>Async batch downloads</strong></li>
  <li>📄 <strong>CSV logging</strong> (success / failure per ID)</li>
  <li>📁 <strong>Custom output directory</strong></li>
  <li>📝 <strong>Custom filename support</strong></li>
  <li>🖥️ <strong>Cross-platform</strong> (Linux, macOS, Windows 10+)</li>
  <li>🧱 <strong>Class-based + standalone CLI</strong></li>
</ul>

<hr/>

<h2>📦 Requirements</h2>

<h3>System</h3>
<ul>
  <li><strong>Python 3.9+</strong></li>
  <li><strong>curl</strong>
    <ul>
      <li>Linux: preinstalled</li>
      <li>macOS: preinstalled</li>
      <li>Windows 10+: included (or via Git Bash)</li>
    </ul>
  </li>
</ul>

<h3>Python Dependencies</h3>

<pre><code>beautifulsoup4&gt;=4.12.0
</code></pre>

<p>Install:</p>

<pre><code>pip install -r requirements.txt
</code></pre>

<hr/>

<h2>🚀 Installation</h2>

<pre><code>git clone https://github.com/itz-real-ks/Tiktok2Local.git
cd Tiktok2Local
pip install -r requirements.txt
</code></pre>

<hr/>

<h2>🧠 How It Works</h2>
<ol>
  <li>Fetches metadata from <code>api.twitterpicker.com</code></li>
  <li>Extracts <strong>only</strong> <code>video_no_watermark.url</code></li>
  <li>Uses <strong>curl</strong> to download the video (<code>-o</code> controls filename)</li>
  <li>Logs results to a CSV file</li>
</ol>

<p>
If <code>video_no_watermark</code> is missing →
<strong>hard failure</strong>.
</p>

<hr/>

<h2>🖥️ Usage</h2>

<h3>Download a single video</h3>

<pre><code>python tiktok_dl.py --id 7516724876304977183
</code></pre>

<p>Saves as:</p>

<pre><code>videos/7516724876304977183.mp4
</code></pre>

<hr/>

<h3>Download multiple videos</h3>

<pre><code>python tiktok_dl.py --id 7516724876304977183 1234567890123456789
</code></pre>

<hr/>

<h3>Custom output directory</h3>

<pre><code>python tiktok_dl.py --id 7516724876304977183 --out my_videos
</code></pre>

<hr/>

<h3>Custom filename</h3>

<pre><code>python tiktok_dl.py --id 7516724876304977183 --name custom_name.mp4
</code></pre>

<p>
⚠️ When multiple IDs are provided, <code>--name</code> applies to
<strong>each run</strong>, not per ID.
</p>

<hr/>

<h3>Custom CSV log file</h3>

<pre><code>python tiktok_dl.py --id 7516724876304977183 --log results.csv
</code></pre>

<hr/>

<h2>📄 CSV Log Format</h2>

<pre><code>id,status,filename,error
7516724876304977183,success,7516724876304977183.mp4,
1234567890123456789,failed,,no_watermark video not available
</code></pre>

<hr/>

<h2>🧩 CLI Parameters</h2>

<table>
  <thead>
    <tr>
      <th>Flag</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>--id</code></td>
      <td>One or more TikTok video IDs (<strong>required</strong>)</td>
    </tr>
    <tr>
      <td><code>--out</code></td>
      <td>Output directory (default: <code>videos</code>)</td>
    </tr>
    <tr>
      <td><code>--name</code></td>
      <td>Custom filename (default: <code>{id}.mp4</code>)</td>
    </tr>
    <tr>
      <td><code>--log</code></td>
      <td>CSV log file (default: <code>download_log.csv</code>)</td>
    </tr>
  </tbody>
</table>

<hr/>

<h2>❌ What This Tool Does <em>Not</em> Do</h2>
<ul>
  <li>❌ Download watermarked videos</li>
  <li>❌ Bypass TikTok DRM</li>
  <li>❌ Use fragile Python TLS stacks</li>
  <li>❌ Hide failures</li>
</ul>

<p>This is intentional.</p>

<hr/>

<h2>⚠️ Notes & Limitations</h2>
<ul>
  <li>TikTok metadata APIs may change without notice</li>
  <li>No-watermark availability is <strong>not guaranteed</strong> for all videos</li>
  <li>curl is used by design for TLS fingerprint compatibility</li>
</ul>

<hr/>

<h2>🔮 Roadmap Ideas</h2>
<ul>
  <li><code>--jobs N</code> concurrency limit</li>
  <li>Per-ID filename templates</li>
  <li>Retry logic (metadata only)</li>
  <li>TikTok URL → ID auto extraction</li>
  <li>Playwright fallback when API breaks</li>
</ul>

<hr/>

<h2>📜 License</h2>
<p><a href="https://github.com/itz-real-ks/Tiktok2Local/blob/main/LICENSE">MIT </a> — do whatever you want, responsibly.</p>
