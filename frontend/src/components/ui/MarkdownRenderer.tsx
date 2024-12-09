import React from 'react';
import ReactMarkdown  from 'react-markdown';
import remarkGfm from 'remark-gfm';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import rehypeRaw from 'rehype-raw';

interface MarkdownRendererProps {
  text: string;
}

const MarkdownRenderer: React.FC<MarkdownRendererProps> = React.memo(({ text }) => {
  return (
    <div className="markdown-renderer p-4 bg-white rounded-lg max-w-full">
      <ReactMarkdown
        className="markdown-content"
        remarkPlugins={[remarkGfm, remarkMath]}
        rehypePlugins={[rehypeKatex, rehypeRaw]}
      >
        {text}
      </ReactMarkdown>
    </div>
  );
});

export default MarkdownRenderer;