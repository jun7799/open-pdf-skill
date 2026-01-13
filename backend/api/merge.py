"""
PDF 合并接口
支持多个 PDF 文件合并为一个
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pypdf import PdfReader, PdfWriter
import uuid
import os
from pathlib import Path

router = APIRouter()

TEMP_DIR = Path("/tmp/pdf-service")
TEMP_DIR.mkdir(exist_ok=True)


@router.post("/merge")
async def merge_pdfs(files: list[UploadFile] = File(...)):
    """
    合并多个 PDF 文件

    参数:
        files: 要合并的 PDF 文件列表

    返回:
        合并后的 PDF 文件下载链接
    """
    if len(files) < 2:
        raise HTTPException(status_code=400, detail="至少需要上传 2 个 PDF 文件")

    # 创建会话目录
    session_id = str(uuid.uuid4())
    session_dir = TEMP_DIR / session_id
    session_dir.mkdir(exist_ok=True)

    try:
        # 保存上传的文件
        input_paths = []
        file_names = []

        for file in files:
            # 验证文件类型
            if not file.filename.endswith('.pdf'):
                raise HTTPException(
                    status_code=400,
                    detail=f"文件 {file.filename} 不是 PDF 格式"
                )

            # 保存文件
            file_path = session_dir / file.filename
            content = await file.read()
            with open(file_path, "wb") as f:
                f.write(content)

            input_paths.append(str(file_path))
            file_names.append(file.filename)

        # 执行合并
        output_path = session_dir / "merged.pdf"
        writer = PdfWriter()

        for pdf_file in input_paths:
            try:
                reader = PdfReader(pdf_file)
                for page in reader.pages:
                    writer.add_page(page)
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"处理文件时出错: {str(e)}"
                )

        # 写入合并后的文件
        with open(output_path, "wb") as output:
            writer.write(output)

        # 返回结果
        return JSONResponse({
            "success": True,
            "message": f"成功合并 {len(files)} 个 PDF 文件",
            "data": {
                "filename": "merged.pdf",
                "pages": len(writer.pages),
                "session_id": session_id
            }
        })

    except HTTPException:
        # 重新抛出 HTTP 异常
        raise
    except Exception as e:
        # 清理会话目录
        if session_dir.exists():
            shutil.rmtree(session_dir)
        raise HTTPException(
            status_code=500,
            detail=f"合并失败: {str(e)}"
        )
