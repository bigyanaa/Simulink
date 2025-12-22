import ollama
desiredOllama = 'llama3.1:latest'

def modifyAccordingToParameter(defaultTemplate,student_profile):
    prompt = f"""
Rephrase the following text while preserving its original meaning. Modify the language, style, and phrasing according to the provided user details.

### **User Profile:**
- Favorite Activity: {student_profile['favorite_activity']} 
- Knowledge about this Topic: {student_profile['kinematics_knowledge']} 

### **Text to Paraphrase:**
"{defaultTemplate}"

### **Instructions:**
- Do **not** add any explanations, introductions, or comments.
- Do **not** add any of your Notes.
- Return **ONLY** the paraphrased text with no extra words like "Here is the rewritten version."
- The response should start directly with the reworded text.
- The text should be modified according to the user's data like their favorite activity and knowledge about the topic.
- The paraphrased text should be easy to understand and in a simple language.
- It should be informative like the original Data and should try to connect user details with the text.

Now, paraphrase the text exactly as per these instructions.

"""
    response = ollama.chat(model=desiredOllama, messages=[{'role': 'user', 'content': prompt}])
    return response['message']['content']



