import os, requests, json, time, sys

def perplexity(prompt: str, model="pplx-7b-online"):
    url = "https://api.perplexity.ai/chat/completions"
    perplexity_api_key = os.environ["PERPLEXITY_API_KEY"]
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        'temperature': 1
    }
    headers = {
        "Authorization": f"Bearer {perplexity_api_key}",
        "accept": "application/json",
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()['choices'][0]['message']['content']

def gpt4(prompt, model="gpt-4-0125-preview"):
    from openai import OpenAI
    client = OpenAI()

    return client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    ).choices[0].message.content


def mixtral(prompt, local=False, print_res=False):
    if "Above are answers to the user query" in prompt:
        print(prompt)
    if local:
        response =  llm(f"Q: {prompt} A: ", max_tokens=500, stop=["Q:", "\n"])
        return response["choices"][0]["text"]
    invoke_url = "https://api.nvcf.nvidia.com/v2/nvcf/pexec/functions/8f4118ba-60a8-4e6b-8574-e38a4067a4a3"
    fetch_url_format = "https://api.nvcf.nvidia.com/v2/nvcf/pexec/status/"
    
    ngc_api_key = os.environ["NGC_API_KEY"]
    headers = {
        "Authorization": f"Bearer {ngc_api_key}",
        "Accept": "application/json",
    }
    
    payload = {
      "messages": [
        {
          "content": prompt,
          "role": "user"
        }
      ],
      "temperature": 0.1,
      "top_p": 0.15,
      "max_tokens": 1024,
      "seed": 42,
      "stream": False
    }
    
    # re-use connections
    t0 = time.time()
    session = requests.Session()
    
    response = session.post(invoke_url, headers=headers, json=payload)
    
    while response.status_code == 202:
        request_id = response.headers.get("NVCF-REQID")
        fetch_url = fetch_url_format + request_id
        response = session.get(fetch_url, headers=headers)
    
    #print(f"DEBUG: {response.content}")
    response.raise_for_status()
    response_body = response.json()

    if print_res:
        print(response_body["choices"][0]["message"]["content"])
    t1 = time.time()
    return response_body["choices"][0]["message"]["content"]
    #except:
    #    return
