import { useState } from 'react';
import { Scissors, Loader2, Download } from 'lucide-react';
import FileUploader from './FileUploader';
import { splitPDF } from '../api/pdf';

export default function SplitPanel() {
  const [files, setFiles] = useState([]);
  const [mode, setMode] = useState('single');
  const [ranges, setRanges] = useState('');
  const [processing, setProcessing] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleSplit = async () => {
    if (files.length === 0) {
      setError('请先上传 PDF 文件');
      return;
    }

    if (mode === 'range' && !ranges.trim()) {
      setError('请输入页面范围，例如：1-3,5-7');
      return;
    }

    setProcessing(true);
    setError(null);
    setResult(null);

    try {
      const response = await splitPDF(files[0], mode, ranges);
      setResult(response.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setProcessing(false);
    }
  };

  return (
    <div className="card">
      <div className="flex items-center gap-3 mb-6">
        <div className="p-3 bg-purple-100 rounded-lg">
          <Scissors className="h-6 w-6 text-purple-600" />
        </div>
        <div>
          <h2 className="text-xl font-bold text-gray-900">拆分 PDF</h2>
          <p className="text-sm text-gray-500">将 PDF 拆分为多个文件</p>
        </div>
      </div>

      <FileUploader
        files={files}
        onFilesChange={setFiles}
        multiple={false}
        maxFiles={1}
      />

      {files.length > 0 && (
        <div className="mt-6 space-y-4">
          {/* 拆分模式选择 */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              拆分模式
            </label>
            <div className="flex gap-3">
              <button
                onClick={() => setMode('single')}
                className={`flex-1 py-3 px-4 rounded-lg border-2 transition-all ${
                  mode === 'single'
                    ? 'border-purple-500 bg-purple-50 text-purple-700 font-medium'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                单页拆分
                <p className="text-xs text-gray-500 mt-1">每页单独保存</p>
              </button>
              <button
                onClick={() => setMode('range')}
                className={`flex-1 py-3 px-4 rounded-lg border-2 transition-all ${
                  mode === 'range'
                    ? 'border-purple-500 bg-purple-50 text-purple-700 font-medium'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                按范围拆分
                <p className="text-xs text-gray-500 mt-1">自定义页面范围</p>
              </button>
            </div>
          </div>

          {/* 页面范围输入 */}
          {mode === 'range' && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                页面范围
              </label>
              <input
                type="text"
                value={ranges}
                onChange={(e) => setRanges(e.target.value)}
                placeholder="例如：1-3,5-7"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              />
              <p className="mt-2 text-sm text-gray-500">
                用逗号分隔多个范围，例如 "1-3,5-7" 表示拆分成 1-3 页和 5-7 页两个文件
              </p>
            </div>
          )}

          {/* 拆分按钮 */}
          <button
            onClick={handleSplit}
            disabled={processing}
            className="w-full btn-primary bg-purple-600 hover:bg-purple-700 flex items-center justify-center gap-2 disabled:opacity-50"
          >
            {processing ? (
              <>
                <Loader2 className="h-5 w-5 animate-spin" />
                处理中...
              </>
            ) : (
              <>
                <Scissors className="h-5 w-5" />
                开始拆分
              </>
            )}
          </button>
        </div>
      )}

      {error && (
        <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
          {error}
        </div>
      )}

      {result && (
        <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg">
          <p className="text-green-700 font-medium">
            拆分成功！共生成 {result.total_files} 个文件
          </p>
          <div className="mt-3 space-y-1">
            {result.files.map((file, index) => (
              <p key={index} className="text-sm text-green-600">
                • {file.filename}
              </p>
            ))}
          </div>
          <p className="text-xs text-gray-500 mt-2">
            会话 ID: {result.session_id}
          </p>
        </div>
      )}
    </div>
  );
}
