/**
 * PDF API 调用封装
 */

// 生产环境的 API 地址
const API_BASE_URL = 'https://bumpy-cordey-wind-change-cb8f2d51.koyeb.app/api';

/**
 * 上传文件并返回进度
 */
async function uploadWithProgress(file, onProgress) {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();

    xhr.upload.addEventListener('progress', (e) => {
      if (e.lengthComputable) {
        const percentComplete = (e.loaded / e.total) * 100;
        onProgress(percentComplete);
      }
    });

    xhr.addEventListener('load', () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        resolve(xhr.response);
      } else {
        reject(new Error(`Upload failed: ${xhr.statusText}`));
      }
    });

    xhr.addEventListener('error', () => {
      reject(new Error('Upload failed'));
    });

    xhr.open('POST', `${API_BASE_URL}/merge`);
    xhr.responseType = 'json';
    xhr.send(file);
  });
}

/**
 * 合并 PDF 文件
 */
export async function mergePDFs(files) {
  const formData = new FormData();
  files.forEach((file) => {
    formData.append('files', file);
  });

  const response = await fetch(`${API_BASE_URL}/merge`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || '合并失败');
  }

  return response.json();
}

/**
 * 拆分 PDF 文件
 * @param {File} file - 要拆分的 PDF 文件
 * @param {string} mode - 拆分模式: 'single' | 'range'
 * @param {string} ranges - 页面范围，如 "1-3,5-7"
 */
export async function splitPDF(file, mode = 'single', ranges = null) {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('mode', mode);
  if (ranges) {
    formData.append('ranges', ranges);
  }

  const response = await fetch(`${API_BASE_URL}/split`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || '拆分失败');
  }

  return response.json();
}

/**
 * 下载文件
 */
export function downloadFile(blob, filename) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}
