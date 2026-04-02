const OWNER = 'Neue-Studio';
const REPO = 'photonassay-website';
const BRANCH = 'main';

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const token = process.env.GITHUB_TOKEN;
  if (!token) {
    return res.status(500).json({ error: 'Server configuration error' });
  }

  const { file, html, status } = req.body;

  try {
    if (status) {
      await commitFile(token, 'copy-status.json', JSON.stringify(status, null, 2), 'Copy dashboard: status update');
      return res.status(200).json({ ok: true, type: 'status' });
    }

    if (file && html) {
      if (!file.endsWith('.html') || file.includes('..') || file.includes('/')) {
        return res.status(400).json({ error: 'Invalid file path' });
      }
      await commitFile(token, file, html, `Copy update: ${file}`);
      return res.status(200).json({ ok: true, type: 'copy', file });
    }

    return res.status(400).json({ error: 'Missing required fields: (file + html) or status' });
  } catch (err) {
    const msg = err.message || 'Unknown error';
    if (msg.includes('409')) {
      return res.status(409).json({ error: 'File was updated by someone else. Please retry.' });
    }
    return res.status(500).json({ error: msg });
  }
}

async function commitFile(token, path, content, message) {
  const url = `https://api.github.com/repos/${OWNER}/${REPO}/contents/${path}`;
  const headers = {
    Authorization: `Bearer ${token}`,
    Accept: 'application/vnd.github+json',
    'Content-Type': 'application/json',
  };

  const existing = await fetch(url + `?ref=${BRANCH}`, { headers });
  let sha = null;
  if (existing.ok) {
    const data = await existing.json();
    sha = data.sha;
  }

  const body = {
    message,
    content: Buffer.from(content, 'utf-8').toString('base64'),
    branch: BRANCH,
    committer: { name: 'Copy Dashboard', email: 'copy-dashboard@photonassay.com' },
  };
  if (sha) body.sha = sha;

  const commit = await fetch(url, { method: 'PUT', headers, body: JSON.stringify(body) });
  if (!commit.ok) {
    const err = await commit.text();
    throw new Error(`GitHub API ${commit.status}: ${err}`);
  }

  return commit.json();
}
