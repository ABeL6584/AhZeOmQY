# 代码生成时间: 2025-08-22 03:01:17
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
# 改进用户体验
from typing import Optional
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter
import re

# Pydantic模型用于接收上传的文件
class FileUpload(BaseModel):
    file: UploadFile
# TODO: 优化性能

# 创建FastAPI实例
app = FastAPI()

# 文本内容分析端点
# NOTE: 重要实现细节
@app.post("/analyze-text")
async def analyze_text(file_upload: FileUpload = File(...)):
    # 读取文件内容
    content = await file_upload.file.read()
    try:
        # 将文件内容转换为字符串
        text = content.decode("utf-8")
        # 使用正则表达式去除特殊字符
        text = re.sub(r'\W', ' ', text)
# 优化算法效率
        # 使用NLTK进行分句和分词
        sentences = sent_tokenize(text)
# 优化算法效率
        words = [word_tokenize(sentence) for sentence in sentences]
        # 将所有分词结果合并成一个列表
        words = [word for sublist in words for word in sublist]
        # 去除停用词和标点符号并进行词形还原
        stop_words = set(stopwords.words('english'))
        lemmatizer = WordNetLemmatizer()
        words = [lemmatizer.lemmatize(word.lower()) for word in words if word.isalpha() and word.lower() not in stop_words]
        # 词频统计
        word_counts = Counter(words)
        # 获取最常见的10个词
        common_words = word_counts.most_common(10)
# 添加错误处理
        return JSONResponse(content={"status": "success", "common_words": common_words})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 错误处理
# 改进用户体验
@app.exception_handler(404)
async def not_found_exception_handler(request, exc):
    return JSONResponse(
        status_code=404, content={"status": "error", "message": "Not Found"}
    )

@app.exception_handler(500)
async def server_error_exception_handler(request, exc):
    return JSONResponse(
        status_code=500, content={"status": "error", "message": "Server Error"}
    )

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)