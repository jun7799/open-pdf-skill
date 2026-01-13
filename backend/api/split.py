"""
PDF 拆分接口
支持将 PDF 拆分为多个单页文件或指定页面范围
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from pypdf import PdfReader, PdfWriter
import uuid
import shutil
from pathlib import Path

router = APIRouter()

TEMP_DIR = Path("/tmp/pdf-service")
TEMP_DIR.mkdir(exist_ok=True)


@router.post("/split")
async def split_pdf(
    file: UploadFile = File(...),
    mode: str = Form("single"),  # single: 单页拆分, range: 按范围拆分
    ranges: str = Form(None)     # 如 "1-3,5-7" 表示拆分成 1-3页 和 5-7页
):
    """
    拆分 PDF 文件

    参数:
        file: 要拆分的 PDF 文件
        mode: 拆分模式
            - single: 每页拆分成一个文件
            - range: 按指定范围拆分
        ranges: 页面范围（如 "1-3,5-7"），仅在 mode=range 时使用

    返回:
        拆分后的文件信息
    """
    # 验证文件类型
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="只支持 PDF 文件")

    # 创建会话目录
    session_id = str(uuid.uuid4())
    session_dir = TEMP_DIR / session_id
    session_dir.mkdir(exist_ok=True)

    try:
        # 保存上传的文件
        input_path = session_dir / file.filename
        content = await file.read()
        with open(input_path, "wb") as f:
            f.write(content)

        # 读取 PDF
        reader = PdfReader(input_path)
        total_pages = len(reader.pages)

        if mode == "single":
            # 单页拆分模式
            output_files = []
            for i in range(total_pages):
                writer = PdfWriter()
                writer.add_page(reader.pages[i])

                output_filename = f"{file.filename.stem}_page_{i+1}.pdf"
                output_path = session_dir / output_filename

                with open(output_path, "wb") as output:
                    writer.write(output)

                output_files.append({
                    "filename": output_filename,
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
            # 按范围拆分模式
            if not ranges:
                raise HTTPException(
                    status_code=400,
                    detail="使用 range 模式时必须指定 ranges 参数"
                )

            # 解析范围
            range_list = [r.strip() for r in ranges.split(",")]
            output_files = []

            for range_str in range_list:
                try:
                    if "-" in range_str:
                        # 处理范围 "1-3"
                        start, end = map(int, range_str.split("-"))
                    else:
                        # 处理单页 "5"
                        start = end = int(range_str)

                    # 验证页面范围
                    if start < 1 or end > total_pages or start > end:
                        raise HTTPException(
                            status_code=400,
                            detail=f"无效的页面范围: {range_str}（文件共 {total_pages} 页）"
                        )

                    # 创建输出文件
                    writer = PdfWriter()
                    for page_num in range(start - 1, end):
                        writer.add_page(reader.pages[page_num])

                    output_filename = f"{file.filename.stem}_pages_{start}-{end}.pdf"
                    output_path = session_dir / output_filename

                    with open(output_path, "wb") as output:
                        writer.write(output)

                    output_files.append({
                        "filename": output_filename,
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

    except HTTPException:
        raise
    except Exception as e:
        # 清理会话目录
        if session_dir.exists():
            shutil.rmtree(session_dir)
        raise HTTPException(
            status_code=500,
            detail=f"拆分失败: {str(e)}"
        )
