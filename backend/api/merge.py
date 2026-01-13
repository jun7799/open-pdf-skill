"""
PDF 合并接口
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pypdf import PdfReader, PdfWriter
import uuid
import tempfile
import os

router = APIRouter()


@router.post("/merge")
async def merge_pdfs(files: list[UploadFile] = File(...)):
    """合并多个 PDF 文件"""
    if len(files) < 2:
        raise HTTPException(status_code=400, detail="至少需要上传 2 个 PDF 文件")

    session_id = str(uuid.uuid4())

    try:
        writer = PdfWriter()

        for file in files:
            if not file.filename.endswith('.pdf'):
                raise HTTPException(
                    status_code=400,
                    detail=f"文件 {file.filename} 不是 PDF 格式"
                )

            content = await file.read()

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
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"合并失败: {str(e)}"
        )
