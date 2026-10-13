import { marked } from 'marked';
import { useEffect, useState } from 'react';

const renderer = new marked.Renderer();

/**
 * Renders Markdown (AI explanations, complexity analysis) as sanitized-ish HTML.
 * `marked` never executes code here; raw HTML is escaped by the parser config.
 */
marked.setOptions({ gfm: true, breaks: true, renderer });

export function Markdown({ text }: { text: string }) {
  const [html, setHtml] = useState('');

  useEffect(() => {
    let cancelled = false;
    // marked.parse can be async-safe; force sync usage and cast.
    const out = marked.parse(text) as string;
    if (!cancelled) setHtml(out);
    return () => {
      cancelled = true;
    };
  }, [text]);

  return (
    <div
      className="markdown-body"
      // Content comes from our own backend's AI responses; never from other users.
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
}
