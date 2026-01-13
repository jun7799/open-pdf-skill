"""
PDF 拆分接口
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from pypdf import PdfReader, PdfWriter
import uuid
import tempfile
import os

router = APIRouter()


@router.post("/split")
async def split_pdf(
    file: UploadFile = File(...),
    mode: str = Form("single"),
    ranges: str = Form(None)
):
    """拆分 PDF 文件"""

    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="只支持 PDF 文件")

    session_id = str(uuid.uuid4())

    try:
        content = await file.read()

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

                return JSONResponse({
                    "success": True,
                    "message": f"成功拆分 {total_pages} 页",
                    "data": {
                        "total_files": len(output_files),
                        "files": output_files,
                        "session_id": session_id
                    }
                })

            elif mode == "range":
                if not ranges:
                    raise HTTPException(
                        status_code=400,
                        detail="使用 range 模式时必须指定 ranges 参数"
                    )

                range_list = [r.strip() for r in ranges.split(",")]
                output_files = []

                for range_str in range_list:
                    try:
                        if "-" in range_str:
                            start, end = map(int, range_str.split("-"))
                        else:
                            start = end = int(range_str)

                        if start < 1 or end > total_pages or start > end:
                            raise HTTPException(
                                status_code=400,
                                detail=f"无效的页面范围: {range_str}"
                            )

                        output_files.append({
                            "filename": f"{file.filename.replace('.pdf', '')}_pages_{start}-{end}.pdf",
                            "range": f"{start}-{end}",
                            "page_count": end - start + 1
                        })

                    except ValueError:
                        raise HTTPException(
                            status_code=400,
                            detail=f"无法解析范围: {range_str}"
                        )

                return JSONResponse({
                    "success": True,
                    "message": f"成功按范围拆分为 {len(output_files)} 个文件",
                    "data": {
                        "total_files": len(output_files),
                        "files": output_files,
                        "session_id": session_id
                    }
                })

            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"不支持的拆分模式: {mode}"
                )

        finally:
            os.unlink(tmp_path)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"拆分失败: {str(e)}"
        )
