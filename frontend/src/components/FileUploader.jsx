import { useCallback, useState } from 'react';
import { UploadCloud, X, File } from 'lucide-react';

export default function FileUploader({ files, onFilesChange, multiple = true, maxFiles = 10 }) {
  const [isDragging, setIsDragging] = useState(false);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    setIsDragging(false);

    const droppedFiles = Array.from(e.dataTransfer.files).filter(
      (file) => file.type === 'application/pdf'
    );

    if (droppedFiles.length === 0) {
      alert('请只上传 PDF 文件');
      return;
    }

    addFiles(droppedFiles);
  }, []);

  const handleFileInput = useCallback((e) => {
    const selectedFiles = Array.from(e.target.files || []);
    addFiles(selectedFiles);
  }, []);

  const addFiles = (newFiles) => {
    if (!multiple) {
      onFilesChange([newFiles[0]]);
      return;
    }

    const currentCount = files.length;
    const availableSlots = maxFiles - currentCount;

    if (availableSlots <= 0) {
      alert(`最多只能上传 ${maxFiles} 个文件`);
      return;
    }

    const filesToAdd = newFiles.slice(0, availableSlots);
    onFilesChange([...files, ...filesToAdd]);
  };

  const removeFile = (index) => {
    onFilesChange(files.filter((_, i) => i !== index));
  };

  const formatFileSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  };

  return (
    <div className="space-y-4">
      {/* 拖拽上传区域 */}
      <div
        onDragOver={(e) => {
          e.preventDefault();
          setIsDragging(true);
        }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
        className={`
          border-2 border-dashed rounded-xl p-8 text-center transition-all
          ${isDragging
            ? 'border-primary-500 bg-primary-50'
            : 'border-gray-300 hover:border-gray-400'
          }
        `}
      >
        <UploadCloud className={`mx-auto h-12 w-12 ${isDragging ? 'text-primary-500' : 'text-gray-400'}`} />
        <p className="mt-4 text-lg font-medium text-gray-700">
          拖拽 PDF 文件到这里，或点击选择
        </p>
        <p className="mt-2 text-sm text-gray-500">
          {multiple ? `最多 ${maxFiles} 个文件` : '单个文件'}
        </p>
        <input
          type="file"
          accept=".pdf"
          multiple={multiple}
          onChange={handleFileInput}
          className="hidden"
          id="file-input"
        />
        <label
          htmlFor="file-input"
          className="mt-4 inline-block cursor-pointer btn-primary"
        >
          选择文件
        </label>
      </div>

      {/* 文件列表 */}
      {files.length > 0 && (
        <div className="space-y-2">
          <h3 className="font-medium text-gray-700">
            已选择 {files.length} 个文件
          </h3>
          <div className="space-y-2">
            {files.map((file, index) => (
              <div
                key={index}
                className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg group"
              >
                <File className="h-5 w-5 text-red-500 flex-shrink-0" />
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-900 truncate">
                    {file.name}
                  </p>
                  <p className="text-xs text-gray-500">
                    {formatFileSize(file.size)}
                  </p>
                </div>
                <button
                  onClick={() => removeFile(index)}
                  className="opacity-0 group-hover:opacity-100 p-1 hover:bg-gray-200 rounded transition-all"
                >
                  <X className="h-4 w-4 text-gray-500" />
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
