import streamlit as st
import tempfile
import os
from core.transcriber import Transcriber
from core.analyzer import MeetingAnalyzer
from core.audio_processor import AudioProcessor
from config import Config

# 页面配置
st.set_page_config(page_title="AI 智能会议纪要助手", layout="wide")
st.title("🎙️ AI 智能会议纪要助手")

# 侧边栏：API 配置
with st.sidebar:
    st.header("⚙️ 配置")
    api_key = st.text_input("OpenAI API Key", type="password", 
                            help="用于 Whisper 语音转写")
    llm_api_key = st.text_input("大模型 API Key (DeepSeek/GPT)", type="password",
                                help="用于智能分析")
    language = st.selectbox("会议语言", ["zh", "en", "ja", "auto"])
    
    if not api_key or not llm_api_key:
        st.warning("请填写 API Key 以使用 AI 功能")
    
    st.divider()
    st.markdown("**支持格式**: MP3, WAV, M4A, FLAC")
    st.markdown("**文件限制**: 25MB (单段) / 不限 (分段处理)")

# 主区域：录音上传
tab1, tab2 = st.tabs(["📤 上传录音", "🔊 在线录制"])

with tab1:
    uploaded_file = st.file_uploader(
        "上传会议录音文件", 
        type=["mp3", "wav", "m4a", "flac"]
    )
    
    if uploaded_file is not None and st.button("🚀 生成纪要"):
        with st.spinner("处理中..."):
            # 保存上传文件
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name
            
            # 步骤1: 音频预处理
            processed_path = AudioProcessor.preprocess(tmp_path)
            
            # 步骤2: 语音转写
            transcriber = Transcriber(api_key)
            transcript = transcriber.transcribe_long(processed_path)
            st.success(f"✅ 转写完成，共 {len(transcript)} 字符")
            
            # 步骤3: 智能分析
            analyzer = MeetingAnalyzer(
                api_key=llm_api_key,
                base_url=Config.LLM_BASE_URL,
                model=Config.LLM_MODEL
            )
            result = analyzer.analyze(transcript)
            
            # 展示结果
            st.divider()
            st.subheader(f"📋 {result.get('title', '会议纪要')}")
            st.caption(f"📅 {result.get('date', '')} ｜👥 {', '.join(result.get('attendees', []))}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**📌 摘要**")
                st.write(result.get('summary', ''))
                st.markdown("**✅ 待办事项**")
                for item in result.get('action_items', []):
                    st.checkbox(f"{item.get('task', '')} - {item.get('assignee', '')}")
            
            with col2:
                st.markdown("**🎯 关键决策**")
                for d in result.get('decisions', []):
                    st.markdown(f"- {d}")
                st.markdown("**📎 后续步骤**")
                for s in result.get('next_steps', []):
                    st.markdown(f"- {s}")
            
            # 显示原始转写（折叠）
            with st.expander("📝 查看原始转写"):
                st.text(transcript)
            
            # 导出功能
            st.download_button(
                "📥 导出纪要 (JSON)",
                data=json.dumps(result, ensure_ascii=False, indent=2),
                file_name="meeting_minutes.json"
            )
            
            # 清理临时文件
            os.unlink(tmp_path)
            os.unlink(processed_path)

with tab2:
    st.warning("⚠️ 浏览器录音功能暂不支持，请使用上传方式")
    st.info("💡 提示：可使用手机录音后上传，或使用电脑外接麦克风录音")
