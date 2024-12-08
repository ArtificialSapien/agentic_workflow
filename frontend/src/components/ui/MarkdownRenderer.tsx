import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeRaw from 'rehype-raw';

interface MarkdownRendererProps {
  text: string;
}

const MarkdownRenderer: React.FC<MarkdownRendererProps> = ({ text }) => {
  return (
    <div className="markdown-renderer">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[rehypeRaw]} // Enables HTML rendering
      >
        {text}
      </ReactMarkdown>
    </div>
  );
};

export default MarkdownRenderer;
