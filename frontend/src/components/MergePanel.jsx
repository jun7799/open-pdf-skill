import { useState } from 'react';
import { Link, Download, Loader2 } from 'lucide-react';
import FileUploader from './FileUploader';
import { mergePDFs, downloadFile } from '../api/pdf';

export default function MergePanel() {
  const [files, setFiles] = useState([]);
  const [processing, setProcessing] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleMerge = async () => {
    if (files.length < 2) {
      setError('请至少上传 2 个 PDF 文件');
      return;
    }

    setProcessing(true);
    setError(null);
    setResult(null);

    try {
      const response = await mergePDFs(files);
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
        <div className="p-3 bg-primary-100 rounded-lg">
          <Link className="h-6 w-6 text-primary-600" />
        </div>
        <div>
          <h2 className="text-xl font-bold text-gray-900">合并 PDF</h2>
          <p className="text-sm text-gray-500">将多个 PDF 文件合并为一个</p>
        </div>
      </div>

      <FileUploader
        files={files}
        onFilesChange={setFiles}
        multiple={true}
        maxFiles={20}
      />

      {files.length >= 2 && (
        <button
          onClick={handleMerge}
          disabled={processing}
          className="w-full mt-6 btn-primary flex items-center justify-center gap-2 disabled:opacity-50"
        >
          {processing ? (
            <>
              <Loader2 className="h-5 w-5 animate-spin" />
              处理中...
            </>
          ) : (
            <>
              <Download className="h-5 w-5" />
              合并 PDF ({files.length} 个文件)
            </>
          )}
        </button>
      )}

      {error && (
        <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
          {error}
        </div>
      )}

      {result && (
        <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg">
          <p className="text-green-700 font-medium">
            合并成功！共 {result.pages} 页
          </p>
          <p className="text-sm text-green-600 mt-1">
            会话 ID: {result.session_id}
          </p>
          <p className="text-xs text-gray-500 mt-2">
            注意：当前版本仅返回处理结果，下载功能将在后续版本中实现
          </p>
        </div>
      )}
    </div>
  );
}
