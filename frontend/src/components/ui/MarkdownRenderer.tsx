// src/components/ui/MarkdownRenderer.tsx

import React, { useMemo } from 'react';
import ReactMarkdown, { Components } from 'react-markdown';
import remarkGfm from 'remark-gfm';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import rehypeRaw from 'rehype-raw';

interface MarkdownRendererProps {
  text: string;
}

const MarkdownRenderer: React.FC<MarkdownRendererProps> = React.memo(({ text }) => {
  // Memoize custom components to prevent re-creation on every render
  const components: Components = useMemo(() => ({
    // Custom Code Block Renderer with Syntax Highlighting
    code({ node, className, children, ...props }) {

      return (
        <code className={className} {...props}>
          {children}
        </code>
      );
    },

    // Custom Link Renderer with Accessibility Enhancements
    a({ href, children, ...props }) {
      return (
        <a
          href={href}
          target="_blank"
          rel="noopener noreferrer"
          className="text-blue-600 hover:underline"
          {...props}
        >
          {children}
        </a>
      );
    },

    // Custom Image Renderer with Alt Text and Responsive Styling
    img({ alt, src, title, ...props }) {
      return (
        <img
          src={src}
          alt={alt}
          title={title}
          className="max-w-full h-auto rounded"
          {...props}
        />
      );
    },

    // Custom Heading Renderer with Anchor Links for Easy Navigation
    h1({ children, ...props }) {
      return (
        <h1 {...props} className="text-2xl font-bold my-4">
          {children}
        </h1>
      );
    },
    h2({ children, ...props }) {
      return (
        <h2 {...props} className="text-xl font-semibold my-3">
          {children}
        </h2>
      );
    },
    h3({ children, ...props }) {
      return (
        <h3 {...props} className="text-lg font-medium my-2">
          {children}
        </h3>
      );
    },
    // Add more heading levels as needed

    // Custom List Renderer with Improved Styling
    ul({ children, ...props }) {
      return (
        <ul {...props} className="list-disc list-inside space-y-1">
          {children}
        </ul>
      );
    },
    ol({ children, ...props }) {
      return (
        <ol {...props} className="list-decimal list-inside space-y-1">
          {children}
        </ol>
      );
    },

    // Blockquote Renderer with Distinct Styling
    blockquote({ children, ...props }) {
      return (
        <blockquote
          {...props}
          className="border-l-4 border-gray-300 pl-4 italic text-gray-700"
        >
          {children}
        </blockquote>
      );
    },

    // Table Renderer with Responsive and Styled Tables
    table({ children, ...props }) {
      return (
        <div className="overflow-x-auto">
          <table {...props} className="min-w-full table-auto border-collapse">
            {children}
          </table>
        </div>
      );
    },
    th({ children, ...props }) {
      return (
        <th
          {...props}
          className="px-4 py-2 border-b border-gray-300 bg-gray-100 text-left"
        >
          {children}
        </th>
      );
    },
    td({ children, ...props }) {
      return (
        <td {...props} className="px-4 py-2 border-b border-gray-300">
          {children}
        </td>
      );
    },

    // Add more custom renderers as needed
  }), []);

  return (
    <div className="markdown-renderer p-4 bg-white rounded-lg max-w-full">
      <ReactMarkdown
        className="markdown-content"
        remarkPlugins={[remarkGfm, remarkMath]}
        rehypePlugins={[rehypeKatex, rehypeRaw]}
        components={components}
      >
        {text}
      </ReactMarkdown>
    </div>
  );
});

export default MarkdownRenderer;