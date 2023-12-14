from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer

model_name_or_path = "TheBloke/una-cybertron-7B-v2-AWQ"
tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)

model = AutoModelForCausalLM.from_pretrained(
    model_name_or_path, low_cpu_mem_usage=True, device_map="cuda:0"
)

streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)


def query_llm(prompt):
    prompt = f"""Write 5 creative image descriptions. Output should be 5 new line separated descriptions without indexes. 
        Experiment with styles, environment, object, subject and other details. Keep prompts under 30 words. Use `{prompt}` as starting point.
    """

    system_message = "Boss"

    prompt_template = f"""<|im_start|>system
    {system_message}<|im_end|>
    <|im_start|>user
    {prompt}<|im_end|>
    <|im_start|>assistant
    """

    tokens = tokenizer(prompt_template, return_tensors="pt").input_ids.cuda()

    generation_params = {
        "do_sample": True,
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 40,
        "max_new_tokens": 512,
        "repetition_penalty": 1.1,
    }

    generation_output = model.generate(tokens, **generation_params)
    token_output = generation_output[0]
    text_output = tokenizer.decode(token_output)

    return text_output


def clean_result(result):
    start = result.find("<|im_start|>assistant")
    end = result.find("<|im_end|></s>")

    if start == -1 or end == -1:
        return None

    result = result[start:end].replace("<|im_start|>assistant", "")
    result = result.replace("<|im_end|>", "")
    # result = result.replace("\n", "")
    result = result.strip()

    result = result.split("\n")
    result = [r.strip() for r in result if len(r.strip()) > 0]
    result = [r[3:] for r in result]
    result = [r.strip() for r in result if len(r.strip()) > 0]

    return result


def generate_prompts(image_prompt):
    attempt = 1
    while True:
        print("Generating prompts... Attempt", attempt)
        raw_result = query_llm(image_prompt)
        result = clean_result(raw_result)
        if result:
            return result
