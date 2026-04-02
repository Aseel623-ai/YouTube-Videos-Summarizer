import streamlit as st
from extract_video_data import extract_video_id, extract_metadata, get_transcript
from llm_summerizer import summarizer


st.title('🎬 YouTube AI Video Summarizer')    
url = st.text_input('Enter Youtube URL:')
col1, col2 = st.columns(2)
with col1:
    lang = st.selectbox('select language', ['Arabic', 'English'])
with col2:
    mode = st.radio('summary mode', ['general', 'educational'], horizontal= True) 
           
if st.button('Summarize'):
    if not url:
        st.warning('Please enter a Youtube URL first!')
        
    else:
        with st.spinner('Processing video...'):
            video_id = extract_video_id(url)
            
            if not video_id:
                st.error('Could not extract video ID. Please check the URL.')
                st.stop()
            
            title = extract_metadata(url)
            image_url = f'https://img.youtube.com/vi/{video_id}/hqdefault.jpg'   
            st.image(image=image_url, caption=title, width='stretch')     

            
            transcript = get_transcript(video_id=video_id)
            if not transcript:
                st.error('No transcript available for this video.')
                st.stop()
            
            summary = summarizer(transcript, lang=lang, mode=mode)
            st.markdown("""<style >
                    .rtl-content{
                        direction: rtl;
                        text-align: right;
                        font-family: 'Tajawal', 'Arial', sans-serif;  
                    }
                
                 </style>""", unsafe_allow_html=True)
                            
            if lang == 'Arabic':
                full_summary = ''
                for token in summarizer(transcript, lang=lang, mode=mode):
                   full_summary+=token 
                st.markdown(f"<div class ='rtl-content'>{full_summary}</div>", text_alignment='left', unsafe_allow_html=True)   
            else:
                st.write_stream(summary)
