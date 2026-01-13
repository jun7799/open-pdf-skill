import { useState } from 'react';
import { FileText, Github } from 'lucide-react';
import MergePanel from './components/MergePanel';
import SplitPanel from './components/SplitPanel';

function App() {
  const [activeTab, setActiveTab] = useState('merge');

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* 头部 */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-primary-100 rounded-lg">
              <FileText className="h-6 w-6 text-primary-600" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">PDF Cloud Service</h1>
              <p className="text-sm text-gray-500">免费的在线 PDF 工具</p>
            </div>
          </div>
          <a
            href="https://github.com"
            target="_blank"
            rel="noopener noreferrer"
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <Github className="h-5 w-5 text-gray-600" />
          </a>
        </div>
      </header>

      {/* 主内容 */}
      <main className="max-w-4xl mx-auto px-4 py-8">
        {/* 标签切换 */}
        <div className="flex gap-2 mb-8">
          <button
            onClick={() => setActiveTab('merge')}
            className={`px-6 py-3 rounded-lg font-medium transition-all ${
              activeTab === 'merge'
                ? 'bg-primary-600 text-white shadow-md'
                : 'bg-white text-gray-700 hover:bg-gray-50'
            }`}
          >
            合并 PDF
          </button>
          <button
            onClick={() => setActiveTab('split')}
            className={`px-6 py-3 rounded-lg font-medium transition-all ${
              activeTab === 'split'
                ? 'bg-primary-600 text-white shadow-md'
                : 'bg-white text-gray-700 hover:bg-gray-50'
            }`}
          >
            拆分 PDF
          </button>
        </div>

        {/* 功能面板 */}
        {activeTab === 'merge' && <MergePanel />}
        {activeTab === 'split' && <SplitPanel />}

        {/* 说明 */}
        <div className="mt-8 p-6 bg-blue-50 border border-blue-200 rounded-xl">
          <h3 className="font-semibold text-blue-900 mb-2">使用说明</h3>
          <ul className="text-sm text-blue-800 space-y-1">
            <li>• 支持的文件大小：最大 50MB</li>
            <li>• 所有文件处理均在云端完成，保护您的隐私</li>
            <li>• 处理后的文件会临时存储，下载后自动删除</li>
            <li>• 如有问题，请提交 Issue 反馈</li>
          </ul>
        </div>
      </main>

      {/* 页脚 */}
      <footer className="mt-16 py-6 border-t border-gray-200 bg-white">
        <div className="max-w-6xl mx-auto px-4 text-center text-sm text-gray-500">
          <p>Built with FastAPI + React + Tailwind CSS</p>
          <p className="mt-1">Deployed on Vercel</p>
        </div>
      </footer>
    </div>
  );
}

export default App;
