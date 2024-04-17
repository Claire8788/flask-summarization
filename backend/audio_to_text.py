from flask import Blueprint, request, jsonify
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import torch
from extension import db,socketio,emit
import os
import librosa
from datasets import load_dataset
import numpy as np
from werkzeug.utils import secure_filename
import tempfile
from pydub import AudioSegment
audio_blueprint = Blueprint('audio', __name__)

# # 加载预训练模型和处理器
# model_id = "openai/whisper-large-v3"
# model = AutoModelForSpeechSeq2Seq.from_pretrained(model_id)
# processor = AutoProcessor.from_pretrained(model_id)





device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

model_id = "openai/whisper-large-v3"

model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
)
model.to(device)

processor = AutoProcessor.from_pretrained(model_id)

pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    max_new_tokens=128,
    chunk_length_s=30,
    batch_size=16,
    return_timestamps=True,
    torch_dtype=torch_dtype,
    device=device,
)


# 上传语音文件转文字的 RESTful API 接口
@audio_blueprint.route('/upload', methods=['POST'])
def upload_audio():
    # 检查请求中是否包含文件
    if 'file' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    # 获取上传的音频文件
    audio_file = request.files['file']


    # 读取音频文件
    audio_data, _ = librosa.load(audio_file, sr=16000)

    # 将音频数据转换为NumPy数组
    audio_data_np = np.array(audio_data)

    # 调用语音识别管道，并传递NumPy数组作为输入
    result = pipe(audio_data_np, generate_kwargs={"language": "english"})

    return jsonify({'text': result["text"]}), 200


# @audio_blueprint.route('/upload_1', methods=['POST'])
# def upload_audio_1():
#     if 'audio' not in request.files:
#         return jsonify({'error': 'No audio file provided'}), 400

#     audio_file = request.files['audio']
#     filename = secure_filename(audio_file.filename)

#     with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
#         audio_file.save(tmp_file.name)

#         # 使用pydub进行格式转换
#         sound = AudioSegment.from_file(tmp_file.name)
#         sound = sound.set_frame_rate(16000).set_channels(1)
#         converted_audio_path = tmp_file.name + "_converted.wav"
#         sound.export(converted_audio_path, format="wav")

#         # 读取转换后的音频文件
#         audio_data, _ = librosa.load(converted_audio_path, sr=16000)

#     # 清理临时文件
#     os.remove(tmp_file.name)
#     os.remove(converted_audio_path)

#     # 将音频数据转换为NumPy数组
#     audio_data_np = np.array(audio_data)

#     # 假设有一个语音识别管道叫做pipe
#     result = pipe(audio_data_np, generate_kwargs={"language": "english"})

#     return jsonify({'text': result["text"]}), 200
# dataset = load_dataset("distil-whisper/librispeech_long", "clean", split="validation")
# sample = dataset[0]["audio"]

# result = pipe(sample)
# result = pipe(sample, generate_kwargs={"language": "english"})
# print(result["text"])

# # 实时语音转文字的 WebSocket 接口
# @audio_blueprint.route('/transcribe', methods=['POST'])
# def transcribe_audio():
#     # 获取 POST 请求中的音频数据
#     audio_data = request.data
    
#     # 将音频数据转换为 Tensor
#     inputs = processor(audio_data, return_tensors="pt", sampling_rate=16_000).input_values
    
#     # 使用模型进行推理
#     with torch.no_grad():
#         logits = model(inputs).logits
    
#     # 使用 beam search 解码得到最佳文本结果
#     predicted_ids = torch.argmax(logits, dim=-1)
#     transcription = processor.batch_decode(predicted_ids)
    
#     return jsonify({'text': transcription[0]}), 200
# @audio_blueprint.route('/transcribe', methods=['GET'])
# def transcribe_audio():
#     # 获取 POST 请求中的音频数据
#     audio_data = request.data
    
#     # 将音频数据转换为 Tensor
#     inputs = processor(audio_data, return_tensors="pt", sampling_rate=16_000).input_values
    
#     # 使用模型进行推理
#     with torch.no_grad():
#         logits = model(inputs).logits
    
#     # 使用 beam search 解码得到最佳文本结果
#     predicted_ids = torch.argmax(logits, dim=-1)
#     transcription = processor.batch_decode(predicted_ids)
    
#     return jsonify({'text': transcription[0]}), 200

# @socketio.on('audio_data')
# def handle_audio_data(audio_data):
#     # 处理接收到的音频数据，并返回转录结果
#     inputs = processor(audio_data, return_tensors="pt", sampling_rate=16_000).input_values
    
#     # 使用模型进行推理
#     with torch.no_grad():
#         logits = model(inputs).logits
    
#     # 使用 beam search 解码得到最佳文本结果
#     predicted_ids = torch.argmax(logits, dim=-1)
#     transcription = processor.batch_decode(predicted_ids)
    
#     socketio.emit('transcription_result', {'text': transcription[0]})
# 实时语音转文字的 WebSocket 接口
# @socketio.on('audio_data')  # 监听来自前端的 'audio_data' 事件
# def handle_audio_data(audio_data):
#     # 处理接收到的音频数据，并返回转录结果
#     # inputs = processor(audio_data, return_tensors="pt", sampling_rate=16_000).input_values
    
#     # # 使用模型进行推理
#     # with torch.no_grad():
#     #     logits = model(inputs).logits
    
#     # # 使用 beam search 解码得到最佳文本结果
#     # predicted_ids = torch.argmax(logits, dim=-1)
#     # transcription = processor.batch_decode(predicted_ids)
#     # 将音频数据转换为NumPy数组
#     audio_data_np = np.array(audio_data)

#     # 调用语音识别管道，并传递NumPy数组作为输入
#     result = pipe(audio_data_np, generate_kwargs={"language": "english"})
#     # 发送转录结果到前端
#     socketio.emit('transcription_result', {'text': result["text"]})



# @socketio.on('audio_data')  # 监听来自前端的 'audio_data' 事件
# def handle_audio_data(audio_data):
#     try:
#         # 假设 audio_data 是字节流，需要先转换为适合模型处理的格式
#         # 这里的转换逻辑依赖于你的具体实现和音频数据格式
#         audio_data_np = np.frombuffer(audio_data, dtype=np.float32)  # 这里的 dtype 取决于模型的输入要求

#         # 调用语音识别管道，并传递NumPy数组作为输入
#         result = pipe(audio_data_np, generate_kwargs={"language": "english"})

#         # 发送转录结果到前端
#         socketio.emit('transcription_result', {'text': result["text"]})
#     except Exception as e:
#         print(f"Error processing audio data: {str(e)}")
#         socketio.emit('error', {'message': 'Failed to process audio data'})


# @socketio.on('audio_data')  # 这里的 'audio_data' 应与前端发送的事件名称一致
# def handle_audio_data(json):
#     audio_data = json['data']
#     try:
#         # 处理数据，假设 audio_data 是音频字节流
#         audio_data_np = np.frombuffer(audio_data, dtype=np.float32)

#         # 调用语音识别管道
#         result = pipe(audio_data_np, generate_kwargs={"language": "english"})

#         # 发送结果回前端
#         emit('transcription_result', {'text': result["text"]})
#     except Exception as e:
#         print(f"Error processing audio data: {str(e)}")
#         emit('error', {'message': 'Failed to process audio data'})



    # return jsonify({'text': result}), 200
# # 上传语音文件转文字的 RESTful API 接口
# @audio_blueprint.route('/upload_1', methods=['POST'])
# def upload_audio_1():
#     # 检查请求中是否包含文件
#     if 'audio' not in request.files:
#         return jsonify({'error': 'No audio file provided'}), 400
    
#     # 获取上传的音频文件
#     audio_file = request.files['audio']


#     # 读取音频文件
#     audio_data, _ = librosa.load(audio_file, sr=16000)

#     # 将音频数据转换为NumPy数组
#     audio_data_np = np.array(audio_data)

#     # 调用语音识别管道，并传递NumPy数组作为输入
#     result = pipe(audio_data_np, generate_kwargs={"language": "english"})

#     return jsonify({'text': result["text"]}), 200
#     # return jsonify({'text': result}), 200


