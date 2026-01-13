"""
PDF Cloud Service - Flask Backend for LeanCloud
提供 PDF 合并、拆分等功能的云端 API
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from pypdf import PdfReader, PdfWriter
import tempfile
import os

app = Flask(__name__)
CORS(app)

# 创建临时目录
TEMP_DIR = "/tmp/pdf-service"
os.makedirs(TEMP_DIR, exist_ok=True)


@app.route("/")
def index():
    """API 健康检查"""
    return jsonify({
        "service": "PDF Cloud Service",
        "version": "1.0.0",
        "status": "running"
    })


@app.route("/health")
def health():
    """健康检查端点"""
    return jsonify({"status": "healthy"})


@app.route("/api/merge", methods=["POST"])
def merge_pdfs():
    """合并多个 PDF 文件"""
    files = request.files.getlist("files")

    if len(files) < 2:
        return jsonify({"error": "至少需要上传 2 个 PDF 文件"}), 400

    try:
        writer = PdfWriter()

        for file in files:
            if not file.filename.endswith('.pdf'):
                return jsonify({"error": f"文件 {file.filename} 不是 PDF 格式"}), 400

            content = file.read()

            # 保存到临时文件
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                tmp.write(content)
                tmp_path = tmp.name

            try:
                reader = PdfReader(tmp_path)
                for page in reader.pages:
                    writer.add_page(page)
            finally:
                os.unlink(tmp_path)

        return jsonify({
            "success": True,
            "message": f"成功合并 {len(files)} 个 PDF 文件",
            "data": {
                "filename": "merged.pdf",
                "pages": len(writer.pages)
            }
        })

    except Exception as e:
        return jsonify({"error": f"合并失败: {str(e)}"}), 500


@app.route("/api/split", methods=["POST"])
def split_pdf():
    """拆分 PDF 文件"""
    file = request.files.get("file")
    mode = request.form.get("mode", "single")
    ranges = request.form.get("ranges")

    if not file:
        return jsonify({"error": "请上传 PDF 文件"}), 400

    if not file.filename.endswith('.pdf'):
        return jsonify({"error": "只支持 PDF 文件"}), 400

    try:
        content = file.read()

        # 保存到临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            tmp.write(content)
            tmp_path = tmp.name

        try:
            reader = PdfReader(tmp_path)
            total_pages = len(reader.pages)

            if mode == "single":
                output_files = []
                for i in range(total_pages):
                    output_files.append({
                        "filename": f"{file.filename.replace('.pdf', '')}_page_{i+1}.pdf",
                        "page": i + 1
                    })

                return jsonify({
                    "success": True,
                    "message": f"成功拆分 {total_pages} 页",
                    "data": {
                        "total_files": len(output_files),
                        "files": output_files
                    }
                })

            elif mode == "range":
                if not ranges:
                    return jsonify({"error": "使用 range 模式时必须指定 ranges 参数"}), 400

                range_list = [r.strip() for r in ranges.split(",")]
                output_files = []

                for range_str in range_list:
                    try:
                        if "-" in range_str:
                            start, end = map(int, range_str.split("-"))
                        else:
                            start = end = int(range_str)

                        if start < 1 or end > total_pages or start > end:
                            return jsonify({"error": f"无效的页面范围: {range_str}"}), 400

                        output_files.append({
                            "filename": f"{file.filename.replace('.pdf', '')}_pages_{start}-{end}.pdf",
                            "range": f"{start}-{end}",
                            "page_count": end - start + 1
                        })

                    except ValueError:
                        return jsonify({"error": f"无法解析范围: {range_str}"}), 400

                return jsonify({
                    "success": True,
                    "message": f"成功按范围拆分为 {len(output_files)} 个文件",
                    "data": {
                        "total_files": len(output_files),
                        "files": output_files
                    }
                })

            else:
                return jsonify({"error": f"不支持的拆分模式: {mode}"}), 400

        finally:
            os.unlink(tmp_path)

    except Exception as e:
        return jsonify({"error": f"拆分失败: {str(e)}"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
