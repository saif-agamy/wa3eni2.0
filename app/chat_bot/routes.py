from flask import Blueprint, render_template, request
import google.generativeai as genai

chat_bot_b = Blueprint(
    'chat_bot',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/chat_bot/static'
)

# setup ai model
genai.configure(api_key='AIzaSyCNtUb8D_DwVbh-aXgf3kokRAML7XFk7So')
model = genai.GenerativeModel('gemini-2.5-flash-lite')

@chat_bot_b.route('/chatbot/', methods=['GET','POST'])
def chat():
    if request.method == 'POST':
        user_prompt = request.form.get('question')

        prompt = f'Your name is wa3eni student helper chatbot, you know info about students unions in Egypt answer all questions kindly, Answer this student question clearly:{user_prompt}'

        response = model.generate_content(prompt)

        return render_template('chatbot.html', response=response.text, user_prompt=user_prompt)

    return render_template('chatbot.html')