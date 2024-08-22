import google.generativeai as genai
from pathlib import Path
import streamlit as st
from googletrans import Translator
from gtts import gTTS
import io
import base64

# Configure GenAI API key
genai.configure(api_key="AIzaSyCy4ZTxt1DiSBeySNHw-pYJey70Nc_uQ3I")

# Function to initialize the model
def initialize_model():
    generation_config = {"temperature": 0.9}
    return genai.GenerativeModel("gemini-1.5-flash", generation_config=generation_config)

# Function to process the image and generate content based on prompts
def generate_content(model, image_path, prompts):
    image_part = {
        "mime_type": "image/jpeg",
        "data": image_path.read_bytes()
    }
    
    results = []
    for prompt_text in prompts:
        prompt_parts = [prompt_text, image_part]
        response = model.generate_content(prompt_parts)
        
        # Extract and return the text content from the response
        if response.candidates:
            candidate = response.candidates[0]
            if candidate.content and candidate.content.parts:
                text_part = candidate.content.parts[0]
                if text_part.text:
                    results.append(f"Prompt: {prompt_text}\nDescription: {text_part.text}\n")
                else:
                    results.append(f"Prompt: {prompt_text}\nDescription: No valid content generated.\n")
            else:
                results.append(f"Prompt: {prompt_text}\nDescription: No content parts found.\n")
        else:
            results.append(f"Prompt: {prompt_text}\nDescription: No candidates found.\n")
    
    return results

# Function to translate text into selected language
def translate_text(text, lang):
    translator = Translator()
    translation = translator.translate(text, dest=lang)
    return translation.text

# Function to convert text to speech and generate an audio file
def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    audio_bytes = io.BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return audio_bytes

# Function to convert audio bytes to base64 for embedding in HTML
def audio_to_base64(audio_bytes):
    return base64.b64encode(audio_bytes.read()).decode('utf-8')

# Streamlit app
def main():
    # Initialize session state for prompts and results
    if "prompts" not in st.session_state:
        st.session_state.prompts = ""
    if "results" not in st.session_state:
        st.session_state.results = []
    if "uploaded_file" not in st.session_state:
        st.session_state.uploaded_file = None

    st.title("Image Description with GenAI Model")

    # Upload an image file
    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file
        # Save the uploaded file
        with open("temp_image.jpg", "wb") as f:
            f.write(uploaded_file.getvalue())
        
        # Initialize the model
        model = initialize_model()
        
        # Input for multiple prompts
        st.write("Enter prompts (one per line):")
        st.session_state.prompts = st.text_area("Prompts", value=st.session_state.prompts)
        
        # Button to generate content
        if st.button("Generate Description"):
            # Split prompts into a list
            prompts = [prompt.strip() for prompt in st.session_state.prompts.split('\n') if prompt.strip()]
            
            if prompts:
                # Generate content based on the uploaded image and user prompts
                image_path = Path("temp_image.jpg")
                st.session_state.results = generate_content(model, image_path, prompts)
            else:
                st.write("Please enter at least one prompt.")
        
        # Optionally remove the temporary file
        Path("temp_image.jpg").unlink()
    
    # Display the uploaded image and previously generated results
    if st.session_state.uploaded_file and st.session_state.results:
        st.image(st.session_state.uploaded_file, caption='Uploaded Image.', use_column_width=True)
        st.write("Generated Descriptions:")
        for description in st.session_state.results:
            st.write(description)

            # Generate and play the audio for each description
            audio_bytes = text_to_speech(description)
            audio_base64 = audio_to_base64(audio_bytes)
            st.audio(audio_bytes, format='audio/mp3')

            # Add translation buttons for Indian regional languages
            if st.button("Translate to Tamil", key=f"translate_tamil_{description}"):
                tamil_translation = translate_text(description, 'ta')
                st.write(tamil_translation)
                tamil_audio_bytes = text_to_speech(tamil_translation)
                tamil_audio_base64 = audio_to_base64(tamil_audio_bytes)
                st.audio(tamil_audio_bytes, format='audio/mp3')
            
            if st.button("Translate to Telugu", key=f"translate_telugu_{description}"):
                telugu_translation = translate_text(description, 'te')
                st.write(telugu_translation)
                telugu_audio_bytes = text_to_speech(telugu_translation)
                telugu_audio_base64 = audio_to_base64(telugu_audio_bytes)
                st.audio(telugu_audio_bytes, format='audio/mp3')
            
            if st.button("Translate to Malayalam", key=f"translate_malayalam_{description}"):
                malayalam_translation = translate_text(description, 'ml')
                st.write(malayalam_translation)
                malayalam_audio_bytes = text_to_speech(malayalam_translation)
                malayalam_audio_base64 = audio_to_base64(malayalam_audio_bytes)
                st.audio(malayalam_audio_bytes, format='audio/mp3')
            
            if st.button("Translate to Kannada", key=f"translate_kannada_{description}"):
                kannada_translation = translate_text(description, 'kn')
                st.write(kannada_translation)
                kannada_audio_bytes = text_to_speech(kannada_translation)
                kannada_audio_base64 = audio_to_base64(kannada_audio_bytes)
                st.audio(kannada_audio_bytes, format='audio/mp3')
            
            if st.button("Translate to Hindi", key=f"translate_hindi_{description}"):
                hindi_translation = translate_text(description, 'hi')
                st.write(hindi_translation)
                hindi_audio_bytes = text_to_speech(hindi_translation)
                hindi_audio_base64 = audio_to_base64(hindi_audio_bytes)
                st.audio(hindi_audio_bytes, format='audio/mp3')

if __name__ == "__main__":
    main()
