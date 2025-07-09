import httpx

from app.core.config import settings

def summarize_resume(resume_text):
    url = "http://vllm:8000/v1/completions"

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "model": settings.DEFAULT_MODEL,
        "prompt": "Summarize the following resume:\n\n\n```" + resume_text + "```\n\n",
        "max_tokens": 250,
        "temperature": 0
    }

    response = httpx.post(url, headers=headers, json=data, timeout=120)

    return response.json().get('choices')[0]['text']


def query_on_resume(resume_text, query):
    url = "http://vllm:8000/v1/completions"

    headers = {
        "Content-Type": "application/json"
    }

    prompt = ''.join([
        "Considering the following Resume:\n```",
        resume_text,
        "```\n\n",
        'And the following listing position requirements:\n```',
        query,
        '```\n',
        "Explain why this canditade would be, or would not be a good candidate for the position: "
    ])
    print(prompt)

    data = {
        "model": settings.DEFAULT_MODEL,
        "prompt": prompt,
        "max_tokens": 250,
        "temperature": 0
    }

    response = httpx.post(url, headers=headers, json=data, timeout=120)
    print('RESPONSE: \n\n' + response.json().get('choices')[0]['text'])
    return response.json().get('choices')[0]['text']


### Guided completions 
from openai import OpenAI

def guided_completion(prompt, choices):
    client = OpenAI(
        base_url="http://vllm:8000/v1",
        api_key="-",
    )

    completion = client.completions.create(
        model= settings.DEFAULT_MODEL,
        prompt = prompt + "\nChoices:" + ','.join(choices) +  "\nAnswer:",
        extra_body={"guided_choice": choices},
    )
    return completion.choices[0].text

def rate_query_on_resume(resume_text, query, reasoning):
    client = OpenAI(
        base_url="http://vllm:8000/v1",
        api_key="-",
    )

    prompt = ''.join([
        "Considering the following Resume:\n```",
        resume_text,
        "```\n\n",
        'The following listing position requirements:\n```',
        query,
        '```\n',
        'And the reasoning if the candidate is a good match:',
        reasoning,
        "\nRate from 0 to 10, how good does the candidate fits the role requirements:\n"
    ])

    completion = client.completions.create(
        model = settings.DEFAULT_MODEL,
        prompt = prompt,
        extra_body={"guided_choice": [str(x) for x in range(0,10)]},
    )
    return completion.choices[0].text

