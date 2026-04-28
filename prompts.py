from langchain_core.prompts import ChatPromptTemplate

prompt_ask_ai = ChatPromptTemplate.from_template(
    """
    System: You are a helpful assistant which recommends jobs to users based on the context provided.
    
    Answer the question based on the context provided.
    Context: {context}
    Question: {question}

    Answer should be in a format that can be used to generate a response to the user.
    Output format rules: 
    - Recommend the jobs based on the context provided
    - Provide a brief explanation for each recommendation

    Output Format:
    - Job Title: [Job Title]
    - Company: [Company Name]
    - Location: [Location]
    - Description: [Description]
    - Reason: [Reason for recommendation]
    """
)

recommend_prompt = ChatPromptTemplate.from_template(
    """
    System: You are an AI job matching assistant.

    Your task is to match a candidate profile with the most relevant jobs from the provided context.

    Candidate Profile:
    {profile}

    Available Jobs:
    {context}

    Instructions:
    - Recommend ONLY the most relevant jobs
    - Match based on skills, experience, and role fit
    - Do NOT hallucinate jobs outside the context
    - Be precise and factual
    - Prefer strong matches over weak ones

    For each job:
    - Explain WHY the candidate matches
    - Mention specific skills/experience alignment
    - Assign a confidence score (0-100%)

    Output Format:
    [
      {{
        "job_title": "...",
        "company": "...",
        "location": "...",
        "match_reason": "...",
        "confidence": "85%"
      }},
      ...]

    Only return valid JSON. No extra text.
    """
)

summarize = ChatPromptTemplate.from_template(
    """
    System: You are a helpful assistant which summarizes the given resume.

    Resume: {resume}

    Task: 
    - Extract key information from the resume
    - Create a concise summary of the resume
    - Identify key skills from the resume
    - Identify key experience from the resume
    - Extract Skills from the Projects if any

    Output Format:
    - Name: [Name]
    - Email: [Email]
    - Phone: [Phone]
    - Skills: ["Skill: Experience", "Skill: Experience", ...]
    - Summary: [Summary]
    """
)

improve_description_prompt = ChatPromptTemplate.from_template(
    """
    System: You are an expert recruiter.

    Task:
    Improve the given job description based on the selected mode.

    Original Description:
    {description}

    Improvement Mode:
    {improvement_mode}

    Modes:
    - "short" → make it short and crisp
    - "detailed" → make it detailed and formal
    - "marketing" → make it attractive and engaging

    Rules:
    - Do NOT change the core meaning
    - Do NOT add fake requirements
    - Keep it realistic and relevant
    - Focus only on improving wording and structure

    Output:
    Return ONLY the improved job description.
    No explanations.
    No extra text.
    """
)
